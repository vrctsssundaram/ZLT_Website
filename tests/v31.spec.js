const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;
const fs = require("node:fs");

const pages = fs.readdirSync(".").filter(file => file.endsWith(".html"));
const base = process.env.BASE_URL || "http://127.0.0.1:4173/ZLT_Website";

async function overflowingElements(page) {
    return page.evaluate(() => [...document.querySelectorAll("body *")].filter(element => {
        const rect = element.getBoundingClientRect();
        return rect.width > 0 && rect.right > innerWidth + 1 && getComputedStyle(element).position !== "absolute";
    }).map(element => element.id || element.className || element.tagName));
}

for (const viewport of [{ width: 1440, height: 1000 }, { width: 375, height: 812 }]) {
    test(`all pages render and reflow at ${viewport.width}px`, async ({ page }, testInfo) => {
        test.setTimeout(180000);
        await page.setViewportSize(viewport);
        const errors = [];
        page.on("pageerror", error => errors.push(error.message));

        for (const file of pages) {
            const response = await page.goto(`${base}/${file}`);
            expect(response.ok(), file).toBeTruthy();
            await expect(page.locator("h1")).toHaveCount(1);
            await expect(page.locator("h1")).toBeVisible();
            await page.evaluate(() => document.fonts.ready.then(() => undefined));
            expect(await overflowingElements(page), file).toEqual([]);
            for (const image of await page.locator("img").all()) {
                await image.scrollIntoViewIfNeeded();
                await expect.poll(() => image.evaluate(node => node.complete && node.naturalWidth > 0), { message: file }).toBeTruthy();
            }
        }
        expect(errors).toEqual([]);
        await page.goto(`${base}/index.html`);
        await page.emulateMedia({ reducedMotion: "reduce" });
        await page.screenshot({ path: `test-results/screens/${testInfo.project.name}-${viewport.width}-home.png`, fullPage: true });
    });
}

test("mobile navigation and service enquiry context", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto(base + "/");
    const toggle = page.getByRole("button", { name: "Open navigation", exact: true });
    await toggle.click();
    const nav = page.getByRole("navigation", { name: "Primary navigation" });
    await expect(nav.getByRole("link", { name: "Services", exact: true })).toBeFocused();
    const disclosure = nav.getByRole("button", { name: "More services pages" });
    await disclosure.click();
    await expect(disclosure).toHaveAttribute("aria-expanded", "true");
    await disclosure.press("Escape");
    await expect(disclosure).toBeFocused();
    await expect(disclosure).toHaveAttribute("aria-expanded", "false");
    await disclosure.press("Escape");
    await expect(toggle).toBeFocused();
    await expect(nav).toBeHidden();

    await toggle.click();
    await nav.getByRole("link", { name: "Services", exact: true }).click();
    await expect(page).toHaveURL(/services\.html$/);
    await toggle.click();
    await expect(nav.getByRole("link", { name: "Services", exact: true })).toHaveAttribute("aria-current", "page");
    await page.getByRole("heading", { name: "Design verification", exact: true }).click();
    await page.getByRole("link", { name: "Ask about this service" }).click();
    await expect(page.locator("#enquiry-context")).toContainText("Design verification");
});

test("application search and enquiry context", async ({ page }) => {
    await page.goto(base + "/applications.html");
    const input = page.getByLabel("Find an application area");
    await input.fill("missing search result");
    await expect(page.locator("#no-applications")).toBeVisible();
    await input.fill("space");
    await expect(page.locator("#application-count")).toHaveText("1 application area");
    await expect(page.locator("[data-application]:visible")).toHaveCount(1);
    await page.locator("#space").getByRole("link", { name: "Discuss this area" }).click();
    await expect(page.locator("#enquiry-context")).toContainText("Space & mission technology");

    await page.goto(base + "/contact.html?type=meeting");
    await expect(page.locator("#projectType")).toHaveValue("Schedule a meeting");
    await expect(page.locator("#enquiry-context")).toContainText("Introductory meeting");

    await page.goto(base + "/contact.html?model=collaboration");
    await expect(page.locator("#projectType")).toHaveValue("Project collaboration");
    await expect(page.locator("#enquiry-context")).toContainText("Joint development");
});

test("reduced motion and homepage links", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto(base + "/");
    await expect(page.locator("h1")).toContainText("Chip design");
    await expect(page.locator("html")).toHaveCSS("scroll-behavior", "auto");
    await page.getByRole("link", { name: "Explore services", exact: true }).click();
    await expect(page).toHaveURL(/#section-2$/);
    await expect(page.getByRole("heading", { name: "Engineering services", exact: true })).toBeInViewport();
});

test("primary journeys work without JavaScript", async ({ browser }) => {
    const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 375, height: 812 } });
    const page = await context.newPage();
    await page.goto(base + "/");
    await page.getByRole("navigation", { name: "Primary navigation" }).getByRole("link", { name: "Applications" }).click();
    await expect(page.locator("[data-application]:visible")).toHaveCount(13);
    await page.getByRole("navigation", { name: "Jump to an application area" }).getByRole("link", { name: "Space & mission technology" }).click();
    await expect(page).toHaveURL(/#space$/);
    await page.locator("#space").getByRole("link", { name: "Discuss this area" }).click();
    await expect(page.locator("#form-unavailable").getByRole("link")).toHaveAttribute("href", "mailto:info@zeptologic.com");
    await expect(page.locator("#technicalEnquiry")).toBeHidden();
    await context.close();
});

async function fillForm(page) {
    await page.getByLabel("Name *", { exact: true }).fill("Website QA");
    await page.getByLabel("Work email").fill("qa@example.com");
    await page.getByLabel("Company or institution").fill("Interface test only");
    await page.getByLabel("A brief project description").fill("This is an intercepted interface test. It does not send a real enquiry.");
    await page.locator("[name=consent]").check();
}

test("enquiry success requires server acknowledgement", async ({ page }) => {
    let submitted;
    await page.route("**/functions/v1/website-enquiry", async route => {
        submitted = route.request().postDataJSON();
        await route.fulfill({ status: 200, json: { ok: true, enquiry_id: "mock-test" } });
    });
    await page.goto(base + "/contact.html?area=compute");
    await fillForm(page);
    await page.getByRole("button", { name: "Send enquiry" }).click();
    await expect(page.locator("#form-status")).toHaveClass("success");
    expect(submitted.email).toBe("qa@example.com");
    expect(submitted.route_context).toBe("Computing & infrastructure");
    expect(submitted.technical_requirement).toContain("intercepted");
    await expect(page.locator("#email")).toHaveValue("");
});

test("unconfirmed delivery preserves input and offers email", async ({ page }) => {
    await page.route("**/functions/v1/website-enquiry", route => route.fulfill({ status: 200, json: { ok: false } }));
    await page.goto(base + "/contact.html");
    await fillForm(page);
    await page.getByRole("button", { name: "Send enquiry" }).click();
    await expect(page.locator("#form-status")).toHaveClass("error");
    await expect(page.locator("#email-fallback")).toBeVisible();
    await expect(page.locator("#email")).toHaveValue("qa@example.com");
    await expect(page.locator("#fallback-link")).toHaveAttribute("href", /^mailto:info@zeptologic.com\?subject=/);
});

test("accessibility on primary pages", async ({ page }) => {
    test.setTimeout(120000);
    for (const file of [
        "index.html", "services.html", "rtl-design-services.html", "applications.html",
        "research.html", "about.html", "engagement-models.html", "contact.html", "careers.html",
    ]) {
        await page.goto(base + "/" + file);
        const result = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa"]).analyze();
        expect(result.violations, file).toEqual([]);
    }
});

test("narrow and zoomed layout", async ({ page }) => {
    await page.setViewportSize({ width: 320, height: 900 });
    for (const file of ["index.html", "contact.html", "applications.html", "about.html"]) {
        await page.goto(base + "/" + file);
        expect(await overflowingElements(page), file).toEqual([]);
    }
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto(base + "/");
    await page.evaluate(() => { document.documentElement.style.fontSize = "200%"; });
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBeTruthy();
});
