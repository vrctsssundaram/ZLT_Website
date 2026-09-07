const {test,expect}=require('@playwright/test');
const fs=require('fs');const path=require('path');
const ROOT=path.resolve(__dirname,'..'),BASE=process.env.BASE_URL||'http://127.0.0.1:4173';
const ALL_PAGES=fs.readdirSync(ROOT).filter(f=>f.endsWith('.html')).sort();
const KEY=['index.html','products.html','services.html','applications.html','research.html','about.html','news.html','contact.html','careers.html'];
const DEVICES=[
 ['phone-portrait',390,844],['phone-landscape',844,390],
 ['tablet-portrait',768,1024],['tablet-landscape',1024,768],
 ['laptop',1366,768],['desktop',1920,1080]
];
const ZOOMS=[25,50,75,100,125,150,175,200];

async function reveal(page){await page.evaluate(()=>document.querySelectorAll('.reveal-v18').forEach(e=>e.classList.add('is-visible')))}
async function zoom(page,z){await page.evaluate(v=>{document.documentElement.style.zoom=String(v/100)},z);await page.waitForTimeout(15)}
async function layoutHealth(page,label){
 const d=await page.evaluate(()=>{
   const de=document.documentElement,b=document.body,cw=de.clientWidth,visual=window.visualViewport?.width||innerWidth;
   const fixed=[...document.querySelectorAll('header,.mobile-dock,.search-dialog.open')].filter(e=>getComputedStyle(e).display!=='none').map(e=>{const r=e.getBoundingClientRect();return{tag:e.tagName,cls:String(e.className),left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}});
   const clipped=[...document.querySelectorAll('main h1,main h2,.action,.project-link,.menu-toggle,.search-button')].filter(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&(r.width<1||r.height<1||r.right<0||r.left>visual)}).map(e=>(e.textContent||e.className||e.tagName).trim().slice(0,80));
   return{doc:de.scrollWidth,body:b.scrollWidth,cw,visual,fixed,clipped};
 });
 expect(d.doc,`${label}: document overflow`).toBeLessThanOrEqual(d.cw+3);
 expect(d.body,`${label}: body overflow`).toBeLessThanOrEqual(d.cw+3);
 expect(d.clipped,`${label}: clipped critical controls/headings`).toEqual([]);
 for(const f of d.fixed){expect(f.left,`${label}: fixed item left ${JSON.stringify(f)}`).toBeGreaterThanOrEqual(-3);expect(f.right,`${label}: fixed item right ${JSON.stringify(f)}`).toBeLessThanOrEqual(d.visual+3)}
}

test('V28 entire-site device orientation and 25–200% zoom/reflow matrix',async({page})=>{
 test.setTimeout(600000);
 for(const [device,width,height] of DEVICES){
   await page.setViewportSize({width,height});
   for(const z of ZOOMS){
     for(const file of ALL_PAGES){
       const res=await page.goto(`${BASE}/${file}`,{waitUntil:'domcontentloaded'});expect(res&&res.ok(),`${file}/${device}/${z}% HTTP`).toBeTruthy();
       await reveal(page);await zoom(page,z);await layoutHealth(page,`${file}/${device}/${z}%`);
       await page.evaluate(()=>{document.documentElement.style.zoom='1'});
     }
   }
 }
});

test('V28 all internal page and fragment links resolve',async({page})=>{
 test.setTimeout(180000);const failures=[];
 for(const file of ALL_PAGES){
   await page.goto(`${BASE}/${file}`,{waitUntil:'domcontentloaded'});
   const hrefs=await page.locator('a[href]').evaluateAll(as=>[...new Set(as.map(a=>a.getAttribute('href')).filter(Boolean))]);
   for(const href of hrefs){
     if(/^(?:mailto:|tel:|https?:\/\/|javascript:)/i.test(href))continue;
     if(href==='#'){failures.push(`${file}: placeholder #`);continue}
     const u=new URL(href,`${BASE}/${file}`),target=u.pathname.split('/').pop()||'index.html';
     if(target.endsWith('.html')){const p=path.join(ROOT,target);if(!fs.existsSync(p)){failures.push(`${file}: missing ${href}`);continue}}
     if(u.hash){const targetFile=target.endsWith('.html')?target:file;await page.goto(`${BASE}/${targetFile}`,{waitUntil:'domcontentloaded'});if(await page.locator(u.hash).count()!==1)failures.push(`${file}: missing fragment ${href}`)}
   }
 }
 expect(failures).toEqual([]);
});

test('V28 phone number and WhatsApp exist only on Contact page',async({page})=>{
 for(const file of ALL_PAGES){await page.goto(`${BASE}/${file}`,{waitUntil:'domcontentloaded'});const html=await page.content();const has=/(?:96266\s*32233|919626632233|wa\.me\/919626632233)/.test(html);if(file==='contact.html')expect(has,'Contact should retain direct phone').toBeTruthy();else expect(has,`${file} leaked phone`).toBeFalsy()}
});

test('V28 no retired media motion or experience widgets are present',async({page})=>{
 for(const file of ALL_PAGES){await page.goto(`${BASE}/${file}`,{waitUntil:'domcontentloaded'});await expect(page.locator('video,.v25-experience,.motion-toggle,[data-film-toggle],[data-cinematic-toggle]'),file).toHaveCount(0);const text=await page.locator('body').innerText();expect(text,file).not.toContain('MOTION DISABLED');expect(text,file).not.toContain('Full Calm Still');expect(text,file).not.toContain('TEXT SIZE Default Larger');expect(text,file).not.toContain('CONTRAST Standard High')}
});

test('V28 static technical visuals are relevant and minimally animated',async({page})=>{
 const cases=[['index.html','.hero-technical-visual'],['products.html','.v28-visual-ip'],['services.html','.v28-visual-engineering'],['applications.html','.v28-visual-applications'],['research.html','.v28-visual-research']];
 for(const [file,sel] of cases){await page.goto(`${BASE}/${file}`,{waitUntil:'domcontentloaded'});const v=page.locator(sel);await expect(v).toBeVisible();await expect(v.locator('svg')).toHaveCount(1);await expect(v.locator('animate,animateTransform')).toHaveCount(0);const count=await v.locator('.v28-svg-spark').count();expect(count).toBeGreaterThan(0);const anim=await v.locator('.v28-svg-spark').first().evaluate(e=>getComputedStyle(e).animationName);expect(['v28QuietSpark','none']).toContain(anim)}
});

test('V28 screenshots cover portrait landscape laptop desktop and zoom extremes',async({page})=>{
 test.setTimeout(300000);const dir=path.join(ROOT,'test-results','screens','v28');fs.mkdirSync(dir,{recursive:true});
 for(const [device,width,height] of DEVICES){
   await page.setViewportSize({width,height});
   for(const file of KEY){await page.goto(`${BASE}/${file}`,{waitUntil:'domcontentloaded'});await reveal(page);await page.screenshot({animations:'disabled',fullPage:true,path:path.join(dir,`${file.replace('.html','')}-${device}.png`)})}
   for(const z of [25,100,200]){await page.goto(`${BASE}/index.html`,{waitUntil:'domcontentloaded'});await reveal(page);await zoom(page,z);await page.screenshot({animations:'disabled',fullPage:true,path:path.join(dir,`index-${device}-zoom-${z}.png`)});await page.evaluate(()=>{document.documentElement.style.zoom='1'})}
 }
});

test('V28 critical interactive flows survive phone landscape and 200% zoom',async({page})=>{
 await page.setViewportSize({width:844,height:390});await page.goto(`${BASE}/index.html`,{waitUntil:'domcontentloaded'});await zoom(page,200);await page.locator('.menu-toggle').click();await expect(page.locator('.head-links')).toHaveClass(/open/);await page.keyboard.press('Escape');await page.locator('.search-button').click();await expect(page.locator('.search-dialog')).toHaveClass(/open/);await page.keyboard.press('Escape');
 await page.goto(`${BASE}/products.html`,{waitUntil:'domcontentloaded'});await zoom(page,200);await page.locator('.ip-filter[data-filter="interface"]').click();await expect(page.locator('.ip-explorer-count')).toHaveText('4 of 13 blocks');
 await page.goto(`${BASE}/contact.html?service=rtl`,{waitUntil:'domcontentloaded'});await zoom(page,200);await expect(page.locator('#projectType')).toHaveValue('RTL design');await expect(page.locator('#technicalEnquiry')).toBeVisible();await layoutHealth(page,'contact/phone-landscape/200%')
});
