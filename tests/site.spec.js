const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const ALL_PAGES = fs.readdirSync(ROOT).filter(f => f.endsWith('.html')).sort();
const BASE = process.env.BASE_URL || 'http://127.0.0.1:4173';
const KEY_PAGES = ['index.html','products.html','services.html','research.html','about.html','news.html','contact.html','careers.html'];
const VIEWPORTS = [
  { name:'compact-phone', width:360, height:800 },
  { name:'phone', width:390, height:844 },
  { name:'large-phone', width:430, height:932 },
  { name:'tablet-portrait', width:768, height:1024 },
  { name:'tablet-large', width:820, height:1180 },
  { name:'laptop', width:1280, height:800 },
  { name:'desktop', width:1440, height:900 },
  { name:'wide', width:1920, height:1080 },
];

function rgb(value){
  const m = value && value.match(/rgba?\((\d+)[, ]+\s*(\d+)[, ]+\s*(\d+)(?:[, /]+\s*([\d.]+))?\)/i);
  if(!m) return null;
  return { r:+m[1], g:+m[2], b:+m[3], a:m[4]===undefined?1:+m[4] };
}
function luminance({r,g,b}){
  const f = c => { c/=255; return c<=.04045 ? c/12.92 : Math.pow((c+.055)/1.055,2.4); };
  return .2126*f(r)+.7152*f(g)+.0722*f(b);
}

async function assertNoDarkSurfaces(page, label){
  const offenders = await page.locator('body *').evaluateAll(nodes => nodes.map(el => {
    const s=getComputedStyle(el),r=el.getBoundingClientRect();
    return {tag:el.tagName,cls:el.className||'',bg:s.backgroundColor,display:s.display,visibility:s.visibility,w:r.width,h:r.height};
  }).filter(x=>x.display!=='none'&&x.visibility!=='hidden'&&x.w>20&&x.h>20));
  const dark = offenders.filter(x=>{ const c=rgb(x.bg); return c && c.a>.85 && luminance(c)<.08; });
  expect(dark.slice(0,12), `${label}: dark background surfaces found`).toEqual([]);
}

async function assertNoOverflow(page, label){
  const dims = await page.evaluate(() => ({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,bw:document.body.scrollWidth}));
  expect(dims.sw, `${label}: document horizontal overflow`).toBeLessThanOrEqual(dims.cw+2);
  expect(dims.bw, `${label}: body horizontal overflow`).toBeLessThanOrEqual(dims.cw+2);
}

for(const vp of VIEWPORTS){
  test.describe(`viewport ${vp.name}`,()=>{
    test.use({ viewport:{width:vp.width,height:vp.height} });
    for(const file of KEY_PAGES){
      test(`${file} renders cleanly`, async ({page})=>{
        const errors=[]; page.on('pageerror',e=>errors.push(String(e))); page.on('console',m=>{if(m.type()==='error') errors.push(m.text())});
        await page.goto(`${BASE}/${file}`,{waitUntil:'networkidle'});
        await expect(page.locator('h1')).toHaveCount(1);
        await assertNoOverflow(page,`${vp.name}/${file}`);
        await assertNoDarkSurfaces(page,`${vp.name}/${file}`);
        expect(errors.filter(x=>!x.includes('favicon'))).toEqual([]);
      });
    }
  });
}

test.describe('all-page structural browser smoke',()=>{
  for(const viewport of [{width:390,height:844},{width:1440,height:900}]){
    for(const file of ALL_PAGES){
      test(`${file} @ ${viewport.width}`,async({page})=>{
        await page.setViewportSize(viewport);
        const response=await page.goto(`${BASE}/${file}`,{waitUntil:'domcontentloaded'});
        expect(response && response.ok(),`${file}: HTTP response`).toBeTruthy();
        await expect(page.locator('body')).toBeVisible();
        await assertNoOverflow(page,`${file}/${viewport.width}`);
        const brokenImages=await page.locator('img').evaluateAll(imgs=>imgs.filter(i=>i.offsetParent!==null&&!i.complete||i.offsetParent!==null&&i.naturalWidth===0).map(i=>i.getAttribute('src')));
        expect(brokenImages,`${file}: broken visible images`).toEqual([]);
      });
    }
  }
});

test('mobile navigation is touch-safe and closes after navigation',async({page})=>{
  await page.setViewportSize({width:390,height:844}); await page.goto(`${BASE}/index.html`);
  const menu=page.locator('.menu-toggle'); await expect(menu).toBeVisible();
  const box=await menu.boundingBox(); expect(box.height).toBeGreaterThanOrEqual(44); expect(box.width).toBeGreaterThanOrEqual(44);
  await menu.click(); await expect(page.locator('.head-links')).toHaveClass(/open/);
  await page.locator('.head-links a[href="products.html"]').click(); await expect(page).toHaveURL(/products\.html/);
});

test('search opens, filters and closes',async({page})=>{
  await page.setViewportSize({width:1440,height:900}); await page.goto(`${BASE}/index.html`);
  await page.locator('.search-button').click(); await expect(page.locator('.search-dialog')).toHaveClass(/open/);
  await page.locator('#siteSearch').fill('floating point'); await expect(page.locator('.search-results')).toContainText('Floating-point IP');
  await page.locator('.search-close').click(); await expect(page.locator('.search-dialog')).not.toHaveClass(/open/);
});

test('IP explorer exposes the 9 + 4 portfolio cleanly',async({page})=>{
  await page.goto(`${BASE}/products.html`,{waitUntil:'networkidle'});
  await expect(page.locator('.ip-explorer-tools')).toBeVisible();
  await page.locator('.ip-filter[data-filter="interface"]').click();
  const visibleInterfaces=await page.locator('.listing-row[data-ip-category="interface"]').evaluateAll(rows=>rows.filter(r=>getComputedStyle(r).display!=='none').length);
  expect(visibleInterfaces).toBe(4);
  await page.locator('.ip-filter[data-filter="arithmetic"]').click();
  const visibleArithmetic=await page.locator('.listing-row[data-ip-category="arithmetic"]').evaluateAll(rows=>rows.filter(r=>getComputedStyle(r).display!=='none').length);
  expect(visibleArithmetic).toBe(9);
});

test('contact context prefills from IP and service routes',async({page})=>{
  await page.goto(`${BASE}/contact.html?ip=fp-multiplier`);
  await expect(page.locator('#projectType')).toHaveValue('IP licensing / evaluation');
  await expect(page.locator('#service')).toHaveValue('Semiconductor IP');
  await expect(page.locator('.route-context')).toContainText('FP Multiplier');
  await page.goto(`${BASE}/contact.html?service=verification`);
  await expect(page.locator('#projectType')).toHaveValue('Verification / coverage closure');
  await expect(page.locator('#service')).toHaveValue('UVM verification');
});

test('contact validation rejects free email and short technical context',async({page})=>{
  await page.goto(`${BASE}/contact.html`);
  await page.locator('#name').fill('Test Engineer'); await page.locator('#email').fill('test@gmail.com'); await page.locator('#company').fill('Example Labs');
  await page.locator('#projectType').selectOption({label:'RTL design'}); await page.locator('#description').fill('This is deliberately longer than forty characters for the email validation test.');
  await page.locator('input[name="consent"]').check(); await page.locator('button[type="submit"]').click();
  await expect(page.locator('.form-error')).toContainText('work or institutional email');
  await page.locator('#email').fill('engineer@example.com'); await page.locator('#description').fill('too short'); await page.locator('button[type="submit"]').click();
  await expect(page.locator('.form-error')).toContainText('technical context');
});

test('contact successful submission contract redirects without writing a real lead',async({page})=>{
  await page.route('**/functions/v1/website-enquiry',route=>route.fulfill({status:201,contentType:'application/json',body:JSON.stringify({ok:true,enquiry_id:'ci-test'})}));
  await page.goto(`${BASE}/contact.html?service=rtl&utm_source=ci`);
  await page.locator('#name').fill('CI Engineer'); await page.locator('#email').fill('ci@example.com'); await page.locator('#company').fill('CI Semiconductor');
  await page.locator('#projectType').selectOption({label:'RTL design'}); await page.locator('#description').fill('We need synthesizable RTL for a bounded digital block with verification collateral and FPGA integration evidence.');
  await page.locator('input[name="consent"]').check(); await page.locator('button[type="submit"]').click();
  await expect(page).toHaveURL(/enquiry-received\.html\?id=ci-test/);
});

test('important mobile controls meet 44px enhanced target guidance',async({page})=>{
  await page.setViewportSize({width:390,height:844}); await page.goto(`${BASE}/contact.html`);
  const failures=await page.locator('button:visible,input:visible,select:visible,textarea:visible,.action:visible,.mobile-dock a:visible').evaluateAll(els=>els.map(e=>{const r=e.getBoundingClientRect();return {name:e.getAttribute('aria-label')||e.textContent.trim().slice(0,35)||e.getAttribute('name'),w:r.width,h:r.height}}).filter(x=>x.w<44||x.h<44));
  expect(failures).toEqual([]);
});

for(const file of ['index.html','products.html','services.html','contact.html']){
  test(`WCAG serious/critical smoke — ${file}`,async({page})=>{
    await page.setViewportSize({width:1440,height:900}); await page.goto(`${BASE}/${file}`,{waitUntil:'networkidle'});
    const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']).analyze();
    const severe=result.violations.filter(v=>['serious','critical'].includes(v.impact));
    expect(severe.map(v=>({id:v.id,impact:v.impact,targets:v.nodes.slice(0,4).map(n=>n.target)}))).toEqual([]);
  });
}

test('capture responsive review artifacts',async({page})=>{
  fs.mkdirSync(path.join(ROOT,'test-results','screens'),{recursive:true});
  for(const vp of [{name:'phone',width:390,height:844},{name:'tablet',width:768,height:1024},{name:'desktop',width:1440,height:900},{name:'wide',width:1920,height:1080}]){
    await page.setViewportSize({width:vp.width,height:vp.height});
    for(const file of ['index.html','products.html','services.html','contact.html']){
      await page.goto(`${BASE}/${file}`,{waitUntil:'networkidle'});
      await page.screenshot({path:path.join(ROOT,'test-results','screens',`${file.replace('.html','')}-${vp.name}.png`),fullPage:true});
    }
  }
});
