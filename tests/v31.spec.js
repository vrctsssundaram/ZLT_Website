const {test,expect}=require('@playwright/test');
const AxeBuilder=require('@axe-core/playwright').default;
const fs=require('fs');
const pages=fs.readdirSync('.').filter(f=>f.endsWith('.html'));
const base=process.env.BASE_URL||'http://127.0.0.1:4173';
for(const size of [{width:1440,height:1000},{width:375,height:812}]){
 test(`all pages render and reflow at ${size.width}`,async({page},testInfo)=>{
  test.setTimeout(180000);await page.setViewportSize(size);const errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const file of pages){await page.goto(`${base}/${file}`,{waitUntil:'networkidle'});await expect(page.locator('h1')).toHaveCount(1);await expect(page.locator('h1')).toBeVisible();expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),file).toBeTruthy();expect(await page.locator('img').evaluateAll(els=>els.every(e=>e.complete&&e.naturalWidth>0)),file).toBeTruthy();}
  expect(errors).toEqual([]);await page.goto(`${base}/index.html`);await page.emulateMedia({reducedMotion:'reduce'});await page.screenshot({path:`test-results/screens/${testInfo.project.name}-${size.width}-home.png`,fullPage:true});
 });
}
test('navigation and application-to-enquiry journey',async({page})=>{
 await page.setViewportSize({width:375,height:812});await page.goto(base+'/');await page.getByRole('button',{name:'Open navigation',exact:true}).click();await page.getByRole('button',{name:'Services',exact:true}).click();await page.getByRole('link',{name:'All services',exact:false}).click();await expect(page).toHaveURL(/services.html/);
 await page.goto(base+'/applications.html');await page.getByLabel('Find an application area').fill('space');await expect(page.locator('[data-application]:visible')).toHaveCount(1);await page.locator('#space').getByRole('link',{name:'Discuss this area'}).click();await expect(page.locator('#enquiry-context')).toContainText('Space & mission');
 await page.goto(base+'/contact.html?type=meeting');await expect(page.locator('#projectType')).toHaveValue('Schedule a meeting');
});
test('hero rotation, pause and reduced motion',async({page})=>{
 await page.goto(base+'/');const before=await page.locator('#hero-title').innerText();await expect(page.locator('#hero-title')).not.toHaveText(before,{timeout:7000});await page.getByRole('button',{name:'Pause introduction rotation'}).click();const paused=await page.locator('#hero-title').innerText();await page.waitForTimeout(5200);await expect(page.locator('#hero-title')).toHaveText(paused);await page.emulateMedia({reducedMotion:'reduce'});await page.reload();await expect(page.getByRole('button',{name:'Resume introduction rotation'})).toBeVisible();
});
async function fillForm(page){await page.getByLabel('Name',{exact:false}).fill('Website QA');await page.getByLabel('Work email').fill('qa@example.com');await page.getByLabel('Organisation').fill('Interface test only');await page.getByLabel('A brief introduction').fill('This is an intercepted interface test; no real enquiry is sent.');await page.locator('[name=consent]').check()}
test('enquiry success requires server acknowledgement',async({page})=>{
 let submitted;await page.route('**/functions/v1/website-enquiry',async route=>{submitted=route.request().postDataJSON();await route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({ok:true,enquiry_id:'mock-test'})})});await page.goto(base+'/contact.html');await fillForm(page);await page.getByRole('button',{name:'Send enquiry'}).click();await expect(page.locator('#form-status')).toHaveClass('success');expect(submitted.technical_requirement).toContain('intercepted');expect(submitted.email).toBe('qa@example.com');await expect(page.locator('#email')).toHaveValue('');
});
test('failed enquiry preserves input and offers manual email fallback',async({page})=>{
 await page.route('**/functions/v1/website-enquiry',r=>r.fulfill({status:503,contentType:'application/json',body:'{"ok":false}'}));await page.goto(base+'/contact.html');await fillForm(page);await page.getByRole('button',{name:'Send enquiry'}).click();await expect(page.locator('#form-status')).toHaveClass('error');await expect(page.locator('#email-fallback')).toBeVisible();await expect(page.locator('#email')).toHaveValue('qa@example.com');await expect(page.locator('#fallback-link')).toHaveAttribute('href',/^mailto:info@zeptologic.com\?subject=/);
});
test('accessibility on primary pages',async({page})=>{
 test.setTimeout(120000);for(const file of ['index.html','services.html','applications.html','about.html','contact.html','careers.html']){await page.goto(base+'/'+file);const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();expect(result.violations,file).toEqual([])}
});
test('narrow and zoomed layout',async({page})=>{
 await page.setViewportSize({width:320,height:900});for(const file of ['index.html','contact.html','applications.html','about.html']){await page.goto(base+'/'+file);expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),file).toBeTruthy()}
 await page.setViewportSize({width:768,height:1024});await page.goto(base+'/');await page.evaluate(()=>document.documentElement.style.fontSize='200%');expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBeTruthy();
});
