const { test, expect } = require('@playwright/test');
const BASE=process.env.BASE_URL||'http://127.0.0.1:4173';
const PAGES=['index.html','products.html','services.html','applications.html','research.html','about.html','news.html','careers.html','contact.html'];

for(const file of PAGES)test(`cross-browser smoke — ${file}`,async({page})=>{
  const errors=[],bad=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('console',m=>{if(m.type()==='error'&&!m.text().includes('favicon'))errors.push(m.text())});
  page.on('response',r=>{if(r.url().startsWith(BASE)&&r.status()>=400)bad.push([r.status(),r.url()])});
  const res=await page.goto(`${BASE}/${file}`,{waitUntil:'networkidle'});
  expect(res&&res.ok()).toBeTruthy();
  await expect(page.locator('h1')).toHaveCount(1);
  await expect(page.locator('body')).toHaveClass(/\bv16\b/);
  expect(errors).toEqual([]);
  expect(bad).toEqual([]);
  const dup=await page.locator('[id]').evaluateAll(es=>{const seen=new Set(),d=[];for(const e of es){if(seen.has(e.id))d.push(e.id);seen.add(e.id)}return d});
  expect(dup).toEqual([]);
  if(file!=='index.html')await expect(page.locator('.v23-context-nav')).toHaveCount(1);
});


test('V26 interaction smoke',async({page})=>{
  await page.setViewportSize({width:1280,height:800});
  await page.goto(BASE+'/index.html',{waitUntil:'domcontentloaded'});
  await expect(page.locator('[data-v25-theatre]')).toBeVisible();
  const exp=page.locator('.v25-experience-toggle');
  await expect(exp).toBeVisible();await exp.click();
  await page.locator('[data-v25-level="still"]').click();
  await expect(page.locator('body')).toHaveClass(/v25-motion-still/);
  await page.locator('.search-button').click();
  await page.locator('#siteSearch').fill('Suresh Kuppuswamy');
  await expect(page.locator('.search-results')).toContainText('Leadership — Suresh Kuppuswamy');
  await page.goto(BASE+'/about.html',{waitUntil:'domcontentloaded'});
  await expect(page.locator('#leadership')).toBeVisible();
  await expect(page.locator('.v26-leadership-milestones>div')).toHaveCount(6);
});
