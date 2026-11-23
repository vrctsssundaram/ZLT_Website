"use strict";

function setupNavigation() {
    const header = document.querySelector(".site-header");
    const navigation = document.getElementById("primary-nav");
    const toggle = header.querySelector(".menu-toggle");
    const disclosures = [...header.querySelectorAll(".nav-disclosure")];
    const mobile = matchMedia("(max-width: 63rem)");

    function showGroup(button, open) {
        button.setAttribute("aria-expanded", String(open));
        document.getElementById(button.getAttribute("aria-controls")).hidden = !open;
    }

    function closeGroups() {
        disclosures.forEach(button => showGroup(button, false));
    }

    function showNavigation(open) {
        toggle.setAttribute("aria-expanded", String(open));
        toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
        navigation.classList.toggle("is-open", open);
        if (!open) closeGroups();
    }

    for (const button of disclosures) {
        button.addEventListener("click", () => {
            const open = button.getAttribute("aria-expanded") === "false";
            closeGroups();
            showGroup(button, open);
        });
        button.hidden = false;
    }

    toggle.addEventListener("click", () => {
        const open = toggle.getAttribute("aria-expanded") === "false";
        showNavigation(open);
        if (open) navigation.querySelector("a").focus();
    });

    header.addEventListener("focusout", event => {
        if (event.relatedTarget && !header.contains(event.relatedTarget)) showNavigation(false);
    });

    document.addEventListener("click", event => {
        if (!header.contains(event.target)) showNavigation(false);
        else if (!event.target.closest(".nav-group")) closeGroups();
    });

    document.addEventListener("keydown", event => {
        if (event.key !== "Escape") return;
        const group = disclosures.find(button => button.getAttribute("aria-expanded") === "true");
        if (group) {
            showGroup(group, false);
            group.focus();
        } else if (mobile.matches && toggle.getAttribute("aria-expanded") === "true") {
            showNavigation(false);
            toggle.focus();
        }
    });

    mobile.addEventListener("change", () => showNavigation(false));
    header.dataset.enhanced = "true";
    toggle.hidden = false;
}

function setupApplicationSearch() {
    const search = document.getElementById("application-search");
    if (!search) return;

    const count = document.getElementById("application-count");
    const empty = document.getElementById("no-applications");
    const normalise = value => value.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
    const rows = [...document.querySelectorAll("[data-application]")].map(row => ({
        element: row,
        text: normalise(row.dataset.application),
    }));

    function filter() {
        const words = normalise(search.value).split(" ").filter(Boolean);
        let visible = 0;
        for (const row of rows) {
            const matches = words.every(word => row.text.includes(word));
            row.element.hidden = !matches;
            if (matches) visible += 1;
        }
        count.textContent = visible === 1 ? "1 application area" : `${visible} application areas`;
        empty.hidden = visible > 0;
    }

    function resetSearch() {
        search.value = "";
        filter();
    }

    search.addEventListener("input", filter);
    document.querySelector(".application-index").addEventListener("click", event => {
        if (event.target.closest("a")) resetSearch();
    });
    window.addEventListener("hashchange", () => {
        const target = document.getElementById(location.hash.slice(1));
        if (target?.hidden && target.hasAttribute("data-application")) resetSearch();
    });
    document.getElementById("search-controls").hidden = false;
}

function setupEnquiry() {
    const form = document.getElementById("technicalEnquiry");
    if (!form) return;

    const endpoint = "https://nujmuknvhgyoxhxuvscx.supabase.co/functions/v1/website-enquiry";
    const contexts = JSON.parse(document.getElementById("contact-contexts").textContent);
    const params = new URLSearchParams(location.search);
    const enquiryType = params.get("type");
    const contextLine = document.getElementById("enquiry-context");
    const projectType = document.getElementById("projectType");
    const description = document.getElementById("description");
    const name = document.getElementById("name");
    const company = document.getElementById("company");
    const status = document.getElementById("form-status");
    const fallback = document.getElementById("email-fallback");
    const fallbackLink = document.getElementById("fallback-link");
    const button = form.querySelector('button[type="submit"]');
    const buttonLabel = button.querySelector("span");
    const fields = document.getElementById("enquiry-fields");

    const contextValue = key => {
        const value = params.get(key);
        return Object.hasOwn(contexts[key], value) ? contexts[key][value] : "";
    };
    const context = contextValue("area") || contextValue("model") || contextValue("service")
        || (enquiryType === "meeting" ? "Introductory meeting" : "");

    if (Object.hasOwn(contexts.types, enquiryType)) projectType.value = contexts.types[enquiryType];
    else if (params.get("model") === "collaboration") projectType.value = "Project collaboration";
    else if (params.get("service") === "research-to-hardware") projectType.value = "Research collaboration";

    const initialType = projectType.value;
    if (context) {
        contextLine.textContent = `Enquiry topic: ${context}`;
        contextLine.hidden = false;
    }

    function readEnquiry() {
        const data = new FormData(form);
        const value = field => String(data.get(field) ?? "").trim();
        return {
            name: value("name"),
            email: value("email"),
            company: value("company"),
            country: value("country"),
            project_type: value("projectType"),
            engineering_route: "",
            technical_requirement: value("description"),
            nda_requested: data.has("nda"),
            selected_ip: "",
            selected_stage: "",
            selected_outcome: "",
            route_context: context || "direct",
            source_url: location.origin + location.pathname,
            utm: {},
            website: value("website"),
        };
    }

    function setStatus(message, state = "") {
        status.textContent = message;
        status.className = state;
    }

    function prepareEmail() {
        const enquiry = readEnquiry();
        const body = [
            `Name: ${enquiry.name}`,
            `Email: ${enquiry.email}`,
            `Company or institution: ${enquiry.company}`,
            `Country: ${enquiry.country}`,
            `Enquiry type: ${projectType.selectedOptions[0].textContent}`,
            `Topic: ${context || "General enquiry"}`,
            `Confidentiality discussion requested: ${enquiry.nda_requested ? "Yes" : "No"}`,
            "",
            enquiry.technical_requirement,
        ].join("\n");
        fallbackLink.href = `mailto:info@zeptologic.com?subject=${encodeURIComponent(
            `Website enquiry - ${enquiry.company}`
        )}&body=${encodeURIComponent(body)}`;
    }

    [name, company, description].forEach(field => {
        field.addEventListener("input", () => field.setCustomValidity(""));
    });
    fallbackLink.addEventListener("click", prepareEmail);

    form.addEventListener("submit", async event => {
        event.preventDefault();
        if (button.disabled) return;

        const enquiry = readEnquiry();
        name.setCustomValidity(enquiry.name ? "" : "Enter your name.");
        company.setCustomValidity(enquiry.company ? "" : "Enter your company or institution.");
        description.setCustomValidity(enquiry.technical_requirement.length >= 40
            ? "" : "Enter at least 40 characters about your project.");
        if (!form.reportValidity()) return;

        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 15000);
        fields.disabled = true;
        button.disabled = true;
        buttonLabel.textContent = "Sending…";
        setStatus("Sending your enquiry…");
        fallback.hidden = true;

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(enquiry),
                signal: controller.signal,
            });
            const result = await response.json();
            if (!response.ok || result?.ok !== true) throw new Error("Delivery not confirmed");
            form.reset();
            projectType.value = initialType;
            setStatus("Your enquiry has been received. Thank you for getting in touch.", "success");
        } catch {
            setStatus("Delivery is unconfirmed. Your message is still here. Try again or email us.", "error");
            fields.disabled = false;
            prepareEmail();
            fallback.hidden = false;
        } finally {
            clearTimeout(timeout);
            fields.disabled = false;
            button.disabled = false;
            buttonLabel.textContent = "Send enquiry";
        }
    });

    form.hidden = false;
    document.getElementById("form-unavailable").hidden = true;
}

document.querySelector("[data-year]").textContent = new Date().getFullYear();
setupNavigation();
setupApplicationSearch();
setupEnquiry();
