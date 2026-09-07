/* Zepto Logic Website — V27 Executive Precision runtime.
   Purposeful interaction only: navigation, search, IP filtering, contact
   routing, engineering stages, responsive navigation,
   performance sampling and light reveal/navigation ergonomics. */
'use strict';

const $=(s,c=document)=>c.querySelector(s);
const $$=(s,c=document)=>[...c.querySelectorAll(s)];
const safeSession={get(k){try{return sessionStorage.getItem(k)}catch(_){return null}},set(k,v){try{sessionStorage.setItem(k,v)}catch(_){}},remove(k){try{sessionStorage.removeItem(k)}catch(_){}}};
const reduce=matchMedia('(prefers-reduced-motion: reduce)');
const dataLayer=window.dataLayer=window.dataLayer||[];
function track(event,detail={}){dataLayer.push({event,page:location.pathname,...detail})}

/* ---------------------------------------------------------------------
   Global page identity, year, viewport and header
   --------------------------------------------------------------------- */
(function base(){
  const raw=(location.pathname.split('/').pop()||'index.html').replace(/\.html$/,'').toLowerCase();
  const page=raw==='index'||raw===''?'home':raw.replace(/[^a-z0-9]+/g,'-');
  document.body.classList.add('page-'+page,'v27','v28');
  document.documentElement.classList.add('v27','v28');
  $$('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
  const viewport=()=>{const w=innerWidth;document.documentElement.dataset.viewport=w<=430?'compact-phone':w<=760?'phone':w<=980?'tablet':w<=1199?'laptop':w>=1600?'wide-desktop':'desktop'};
  viewport();addEventListener('resize',viewport,{passive:true});

  const head=$('.site-head');
  const syncHead=()=>head?.classList.toggle('scrolled',scrollY>18);
  syncHead();addEventListener('scroll',syncHead,{passive:true});
})();

/* ---------------------------------------------------------------------
   Primary navigation
   --------------------------------------------------------------------- */
const primaryNav=$('.head-links'),menuToggle=$('.menu-toggle');
if(primaryNav&&!primaryNav.id)primaryNav.id='primaryNavigation';
if(menuToggle){
  menuToggle.setAttribute('aria-controls','primaryNavigation');
  const setMenu=open=>{
    menuToggle.setAttribute('aria-expanded',String(open));
    primaryNav?.classList.toggle('open',open);
    document.body.classList.toggle('nav-open',open);
    menuToggle.textContent=open?'Close':'Menu';
  };
  menuToggle.addEventListener('click',()=>setMenu(menuToggle.getAttribute('aria-expanded')!=='true'));
  primaryNav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));
  addEventListener('resize',()=>{if(innerWidth>980)setMenu(false)},{passive:true});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menuToggle.getAttribute('aria-expanded')==='true'){setMenu(false);menuToggle.focus()}});
}

/* ---------------------------------------------------------------------
   Executive command palette / search
   --------------------------------------------------------------------- */
const searchDialog=$('.search-dialog'),siteSearch=$('#siteSearch'),searchResults=$('.search-results');
const searchIndex=[
 ['Semiconductor IP','products.html','semiconductor IP floating point arithmetic UART SPI I2C license evaluate reusable portfolio'],
 ['Applications','applications.html','compute signal processing embedded communications security edge research hardware workloads'],
 ['Floating-point IP','floating-point-ip.html','IEEE 754 add subtract multiplier divider reciprocal square root MAC complex matrix'],
 ['Engineering','services.html','architecture RTL UVM verification FPGA lint CDC RDC engineering'],
 ['RTL Design','rtl-design-services.html','Verilog SystemVerilog VHDL microarchitecture datapath control'],
 ['Verification','verification-coverage-closure.html','UVM coverage regression assertions verification lint CDC RDC'],
 ['FPGA Prototyping','fpga-prototyping-services.html','AMD Xilinx Zynq prototype timing bring-up constraints'],
 ['IP Quality','ip-quality-audit.html','lint CDC RDC reuse readiness RTL audit review'],
 ['Cryptographic Hardware','cryptographic-hardware-acceleration.html','zk SNARK PQC cryptography accelerator secure compute'],
 ['Research to Hardware','research-to-hardware.html','research co-creation collaboration co-development architecture FPGA'],
 ['C-DOT Samarth','cdot-samarth-zksnark.html','C-DOT Samarth zk SNARK zero knowledge FPGA'],
 ['Company','about.html','Zepto Logic company Coimbatore semiconductor fabless'],
 ['Leadership — Suresh Kuppuswamy','about.html#leadership','CEO managing director co-founder Suresh Kuppuswamy Harvard AMP 206 leadership'],
 ['Applied R&D','research.html','research secure hardware cryptography acceleration collaboration co-creation'],
 ['Insights','news.html','news C-DOT Tamil Nadu company milestones'],
 ['Careers','careers.html','VLSI RTL verification FPGA careers internship'],
 ['Contact','contact.html','technical enquiry phone WhatsApp email partnership collaboration']
];
let previousFocus=null,selectedSearch=-1;
function searchLinks(){return searchResults?$$('.search-result',searchResults):[]}
function renderSearch(query=''){
  if(!searchResults)return;
  selectedSearch=-1;
  const terms=query.toLowerCase().trim().split(/\s+/).filter(Boolean);
  if(!terms.length){searchResults.innerHTML='<p>Search IP, engineering, applications, R&amp;D, leadership or company information.</p>';return}
  const found=searchIndex.filter(([title,,keys])=>terms.every(t=>(title+' '+keys).toLowerCase().includes(t))).slice(0,9);
  searchResults.innerHTML=found.length?found.map(([title,href])=>`<a class="search-result" href="${href}"><strong>${title}</strong><span>Open →</span></a>`).join(''):'<p>No direct match. <a href="contact.html">Contact Zepto Logic →</a></p>';
}
function searchHints(){
  if(!searchDialog||searchDialog.querySelector('.v26-command-hint'))return;
  searchDialog.classList.add('v26-command');
  const row=document.createElement('div');row.className='v26-command-hint';row.setAttribute('aria-label','Quick routes');
  [['IP','IP'],['RTL','RTL'],['Verification','Verification'],['FPGA','FPGA'],['CEO','Suresh Kuppuswamy'],['Contact','Contact']].forEach(([label,q])=>{
    const b=document.createElement('button');b.type='button';b.textContent=label;b.addEventListener('click',()=>{siteSearch.value=q;renderSearch(q);siteSearch.focus()});row.append(b);
  });
  const hint=document.createElement('span');hint.className='v26-search-shortcut';hint.textContent='Ctrl/⌘ K · /';row.append(hint);
  siteSearch?.closest('.search-row')?.after(row);
}
function openSearch(){
  if(!searchDialog)return;
  previousFocus=document.activeElement;searchHints();selectedSearch=-1;
  searchDialog.classList.add('open');searchDialog.setAttribute('aria-hidden','false');searchDialog.setAttribute('role','dialog');searchDialog.setAttribute('aria-modal','true');searchDialog.setAttribute('aria-label','Search Zepto Logic');
  document.body.style.overflow='hidden';setTimeout(()=>{siteSearch?.focus();siteSearch?.select()},30);
}
function closeSearch(){
  const wasOpen=searchDialog?.classList.contains('open');searchDialog?.classList.remove('open');searchDialog?.setAttribute('aria-hidden','true');selectedSearch=-1;
  if(!document.body.classList.contains('nav-open'))document.body.style.overflow='';
  if(wasOpen&&previousFocus instanceof HTMLElement)setTimeout(()=>previousFocus.focus(),0);
}
function moveSearch(delta){
  const links=searchLinks();if(!links.length)return;
  selectedSearch=(selectedSearch+delta+links.length)%links.length;
  links.forEach((a,i)=>a.classList.toggle('v26-selected',i===selectedSearch));links[selectedSearch]?.scrollIntoView({block:'nearest'});
}
$$('.search-button').forEach(b=>{b.title='Search · Ctrl/⌘ K';b.addEventListener('click',openSearch)});
$('.search-close')?.addEventListener('click',closeSearch);
searchDialog?.addEventListener('click',e=>{if(e.target===searchDialog)closeSearch()});
siteSearch?.addEventListener('input',e=>renderSearch(e.target.value));
siteSearch?.addEventListener('keydown',e=>{if(e.key==='ArrowDown'){e.preventDefault();moveSearch(1)}else if(e.key==='ArrowUp'){e.preventDefault();moveSearch(-1)}else if(e.key==='Enter'&&selectedSearch>=0){e.preventDefault();searchLinks()[selectedSearch]?.click()}});
document.addEventListener('keydown',e=>{
  const editable=/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName||'');
  if(e.key==='Escape'&&searchDialog?.classList.contains('open'))closeSearch();
  if(((e.key.toLowerCase()==='k'&&(e.metaKey||e.ctrlKey))||(e.key==='/'&&!editable))&&!e.altKey){e.preventDefault();openSearch()}
  if(e.key==='Tab'&&searchDialog?.classList.contains('open')){
    const f=$$('a[href],button:not([disabled]),input:not([disabled]),[tabindex]:not([tabindex="-1"])',searchDialog).filter(x=>x.offsetParent!==null);
    if(f.length){const first=f[0],last=f[f.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}
  }
});

/* ---------------------------------------------------------------------
   Page-local context navigation — simple, no animated chapter dots
   --------------------------------------------------------------------- */
(function contextNav(){
  if(document.body.classList.contains('page-home'))return;
  const main=$('main');if(!main||$('.v23-context-nav'))return;
  const sections=$$('main>section').filter(s=>!s.classList.contains('z-cta'));
  if(sections.length<2)return;
  const links=[];
  sections.forEach((s,i)=>{
    if(!s.id)s.id='section-'+(i+1);
    const eyebrow=s.querySelector('.eyebrow')?.textContent?.trim();
    const heading=s.querySelector('h1,h2')?.textContent?.trim();
    links.push({id:s.id,label:(eyebrow||heading||`Section ${i+1}`).slice(0,34)});
  });
  const nav=document.createElement('nav');nav.className='v23-context-nav';nav.setAttribute('aria-label','On this page');
  nav.innerHTML='<div class="wrap"><span>On this page</span><div class="v23-context-links">'+links.map(x=>`<a href="#${x.id}">${x.label}</a>`).join('')+'</div></div>';
  sections[0].after(nav);
})();

/* ---------------------------------------------------------------------
   Light scroll progress and restrained reveals
   --------------------------------------------------------------------- */
(function progressiveEnhancement(){
  if(!$('.scroll-progress'))document.body.insertAdjacentHTML('afterbegin','<div class="scroll-progress" aria-hidden="true"><i></i></div>');
  const bar=$('.scroll-progress i');let ticking=false;
  const sync=()=>{const max=document.documentElement.scrollHeight-innerHeight,ratio=max>0?Math.min(1,Math.max(0,scrollY/max)):0;bar?.style.setProperty('transform',`scaleX(${ratio})`);ticking=false};
  addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(sync)}},{passive:true});sync();
  const targets=$$('main .z-head,main .z-card,main .z-app,main .z-flow article,main .z-feature-story,main .listing-row,main .contact-shell');
  targets.forEach(el=>el.classList.add('reveal-v18'));
  if(!reduce.matches&&'IntersectionObserver'in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target)}}),{threshold:.06,rootMargin:'0px 0px -3% 0px'});targets.forEach(el=>io.observe(el))}else targets.forEach(el=>el.classList.add('is-visible'));
})();

/* ---------------------------------------------------------------------
   IP explorer — 13 public blocks, filtered without changing source claims
   --------------------------------------------------------------------- */
(function ipExplorer(){
  if(!document.body.classList.contains('page-products'))return;
  const rows=$$('.listing-row');if(!rows.length)return;
  rows.forEach(row=>{const label=row.closest('.z-section')?.querySelector('.eyebrow')?.textContent?.toLowerCase()||'';row.dataset.ipCategory=label.includes('interface')?'interface':'arithmetic'});
  const first=$('.listing');if(!first)return;
  const tools=document.createElement('div');tools.className='ip-explorer-tools';tools.innerHTML='<div class="ip-filter-group" aria-label="Filter IP portfolio"><button class="ip-filter active" type="button" data-filter="all" aria-pressed="true">All</button><button class="ip-filter" type="button" data-filter="arithmetic" aria-pressed="false">Arithmetic</button><button class="ip-filter" type="button" data-filter="interface" aria-pressed="false">Interfaces</button></div><label class="ip-search-field"><span class="sr-only">Search IP portfolio</span><input class="ip-search" type="search" placeholder="Search IP blocks"></label><span class="ip-explorer-count">13 of 13 blocks</span>';
  first.before(tools);
  const filters=$$('.ip-filter',tools),input=$('.ip-search',tools),count=$('.ip-explorer-count',tools);let category='all';
  const apply=()=>{const q=(input?.value||'').trim().toLowerCase();let shown=0;rows.forEach(r=>{const passCat=category==='all'||r.dataset.ipCategory===category,passText=!q||r.textContent.toLowerCase().includes(q),show=passCat&&passText;r.style.display=show?'':'none';if(show)shown++});count.textContent=`${shown} of ${rows.length} blocks`};
  filters.forEach(b=>b.addEventListener('click',()=>{category=b.dataset.filter;filters.forEach(x=>{const on=x===b;x.classList.toggle('active',on);x.setAttribute('aria-pressed',String(on))});apply()}));input?.addEventListener('input',apply);apply();
})();

/* ---------------------------------------------------------------------
   Contact route context, prefilling and secure submission
   --------------------------------------------------------------------- */
(function contact(){
  const form=$('#technicalEnquiry');if(!form)return;
  const params=new URLSearchParams(location.search);
  const ipMap={
    'fp-add-sub':'FP Adder / Subtractor','fp-multiplier':'FP Multiplier','fp-divider':'FP Divider','fp-reciprocal':'FP Reciprocal','fp-sqrt':'FP Square Root','fp-invsqrt':'FP Inverse Square Root','fp-mac':'FP Multiply-Accumulate','fp-complex':'FP Complex Multiplier','fp-matrix':'FP Complex Matrix Multiplier N×N',uart:'UART Controller',spi:'SPI Controller',i2c:'I²C Controller','i2c-master':'I²C Master'
  };
  const project=$('#projectType'),service=$('#service'),stage=$('#stage'),outcome=$('#outcome'),description=$('#description');
  const choose=(select,label)=>{if(!select||!label)return;const opt=[...select.options].find(o=>o.text.trim()===label);if(opt)select.value=opt.value};
  const ip=params.get('ip'),svc=params.get('service'),type=params.get('type');
  if(ip){choose(project,'IP licensing / evaluation');choose(service,'Semiconductor IP')}
  if(svc==='rtl'){choose(project,'RTL design');choose(service,'RTL design')}
  if(svc==='verification'){choose(project,'Verification / coverage closure');choose(service,'UVM verification')}
  if(svc==='fpga'){choose(project,'FPGA prototyping');choose(service,'FPGA prototyping')}
  if(svc==='architecture'){choose(project,'Architecture / specification');choose(service,'Architecture assessment')}
  if(type==='ip')choose(project,'IP licensing / evaluation');
  if(type==='research')choose(project,'Research collaboration');
  if(type==='partnership')choose(project,'Technology partnership');
  if(params.get('stage'))choose(stage,params.get('stage'));
  if(params.get('outcome'))choose(outcome,params.get('outcome'));
  const context=ip?(ipMap[ip]||ip):svc?({rtl:'RTL design',verification:'Verification',fpga:'FPGA prototyping',architecture:'Architecture'}[svc]||svc):type?({ip:'IP evaluation',research:'Applied R&D / co-creation',partnership:'Technology partnership'}[type]||type):'';
  if(context){const box=document.createElement('div');box.className='route-context';box.textContent='Enquiry context: '+context;form.prepend(box)}

  if(!$('[name="website"]',form))form.insertAdjacentHTML('afterbegin','<div aria-hidden="true" class="hp-field"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>');
  if(description){
    const field=description.closest('.field'),help=$('.form-help',field);if(help&&!help.id)help.id='descriptionHelp';
    let counter=$('.field-counter',field);if(!counter){counter=document.createElement('span');counter.className='field-counter';counter.id='descriptionCounter';field.append(counter)}
    description.setAttribute('aria-describedby',[description.getAttribute('aria-describedby'),help?.id,counter.id].filter(Boolean).join(' '));
    const update=()=>{const n=description.value.trim().length,ready=n>=40;counter.classList.toggle('ready',ready);counter.textContent=ready?`${n} characters · ready to send`:`${n}/40 minimum`};description.addEventListener('input',update);update();
  }

  const utm={};['utm_source','utm_medium','utm_campaign','utm_content','utm_term'].forEach(k=>{const v=params.get(k)||safeSession.get('zl_'+k);if(v){utm[k]=v;safeSession.set('zl_'+k,v)}});
  const ENDPOINT='https://nujmuknvhgyoxhxuvscx.supabase.co/functions/v1/website-enquiry';
  function fallback(d,requirement){
    const subject=encodeURIComponent(`[Website enquiry] ${d.get('projectType')} — ${d.get('company')}`);
    const body=encodeURIComponent(`Name: ${d.get('name')}\nEmail: ${d.get('email')}\nCompany: ${d.get('company')}\nCountry: ${d.get('country')||'Not specified'}\nRequirement: ${d.get('projectType')}\nEngineering route: ${d.get('service')||'Not specified'}\nCurrent stage: ${d.get('stage')||'Not specified'}\nNeeded next: ${d.get('outcome')||'Not specified'}\nSelected IP: ${ip?(ipMap[ip]||ip):'n/a'}\nNDA requested: ${d.get('nda')?'Yes':'No'}\n\nTechnical requirement:\n${requirement}`);
    location.href=`mailto:info@zeptologic.com?subject=${subject}&body=${body}`;
  }
  let submitting=false;
  form.addEventListener('submit',async e=>{
    e.preventDefault();if(submitting)return;
    const d=new FormData(form),err=$('.form-error',form),notice=$('.notice',form),btn=$('button[type="submit"]',form),requirement=String(d.get('description')||'').trim();
    if(err){err.style.display='none';err.setAttribute('tabindex','-1')}if(notice)notice.textContent='';
    if(requirement.length<40){if(err){err.textContent='Please provide at least 40 characters of technical context.';err.style.display='block';err.focus()}return}
    const payload={name:String(d.get('name')||''),email:String(d.get('email')||''),company:String(d.get('company')||''),country:String(d.get('country')||''),project_type:String(d.get('projectType')||''),engineering_route:String(d.get('service')||''),technical_requirement:requirement,nda_requested:Boolean(d.get('nda')),selected_ip:ip?(ipMap[ip]||ip):'',selected_stage:String(d.get('stage')||params.get('stage')||''),selected_outcome:String(d.get('outcome')||params.get('outcome')||''),route_context:ip||svc||type||'direct',source_url:location.href,utm,website:String(d.get('website')||'')};
    const old=btn?.textContent||'Send enquiry';submitting=true;if(btn){btn.disabled=true;btn.textContent='Sending…'}if(notice)notice.textContent='Sending securely…';
    try{const r=await fetch(ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}),out=await r.json().catch(()=>({}));if(!r.ok||!out.ok)throw new Error(out.error||`HTTP ${r.status}`);track('technical_enquiry_submitted',{project_type:payload.project_type,engineering_route:payload.engineering_route,...utm});const next=new URL('enquiry-received.html',location.href);if(out.enquiry_id)next.searchParams.set('id',out.enquiry_id);location.href=next.toString()}
    catch(ex){console.error(ex);if(err){err.textContent='Secure delivery could not be confirmed. Your email application will open with the enquiry prepared.';err.style.display='block'}fallback(d,requirement)}
    finally{submitting=false;if(btn){btn.disabled=false;btn.textContent=old}}
  });
})();

/* ---------------------------------------------------------------------
   Five-stage engineering path — retained, visually simplified in V27
   --------------------------------------------------------------------- */
(function engineeringPath(){
  const theatre=$('[data-v25-theatre]');if(!theatre)return;
  const cards=$$('[data-v25-step]',theatre),core=$('[data-v25-core]',theatre),kicker=$('[data-v25-kicker]',theatre),title=$('[data-v25-title]',theatre),copy=$('[data-v25-copy]',theatre),progress=$('[data-v25-progress]',theatre),bar=$('.v25-story-progress i b',theatre);
  const data={
    define:{core:'SPEC',k:'01 / DEFINE',title:'Start with the boundary.',copy:'Capture interfaces, clocks, resets, data movement, target platform and the evidence needed for the next engineering decision.'},
    architect:{core:'ARCH',k:'02 / ARCHITECT',title:'Shape the hardware.',copy:'Partition datapaths, control, memory, interfaces and implementation assumptions around the system requirement.'},
    implement:{core:'RTL',k:'03 / IMPLEMENT',title:'Build synthesizable logic.',copy:'Implement bounded datapaths, control, protocols and integration logic with reviewable RTL outputs.'},
    verify:{core:'UVM',k:'04 / VERIFY',title:'Turn behaviour into evidence.',copy:'Use assertions, regression, coverage, lint and CDC/RDC engineering to strengthen implementation confidence.'},
    prove:{core:'FPGA',k:'05 / PROVE',title:'Take it into hardware.',copy:'Move through constraints, timing closure, board bring-up and repeatable FPGA evidence where required.'}
  };
  let index=Math.max(0,cards.findIndex(c=>c.getAttribute('aria-pressed')==='true'));
  function activate(i,focus=false){index=(i+cards.length)%cards.length;cards.forEach((c,n)=>{const on=n===index;c.classList.toggle('active',on);c.setAttribute('aria-pressed',String(on));if(on&&focus)c.focus()});const d=data[cards[index]?.dataset.v25Step];if(d){if(core)core.textContent=d.core;if(kicker)kicker.textContent=d.k;if(title)title.textContent=d.title;if(copy)copy.textContent=d.copy}if(progress)progress.textContent=String(index+1).padStart(2,'0')+' / '+String(cards.length).padStart(2,'0');if(bar)bar.style.width=((index+1)/cards.length*100)+'%';track('engineering_stage_selected',{stage:cards[index]?.dataset.v25Step})}
  cards.forEach((c,i)=>{c.addEventListener('click',()=>activate(i));c.addEventListener('keydown',e=>{if(!['ArrowRight','ArrowDown','ArrowLeft','ArrowUp','Home','End'].includes(e.key))return;e.preventDefault();if(e.key==='Home')activate(0,true);else if(e.key==='End')activate(cards.length-1,true);else activate(i+(['ArrowRight','ArrowDown'].includes(e.key)?1:-1),true)})});
  $('[data-v25-next]',theatre)?.addEventListener('click',()=>activate(index+1));$('[data-v25-prev]',theatre)?.addEventListener('click',()=>activate(index-1));activate(index);
})();

/* ---------------------------------------------------------------------
   Static technical visuals require no media or motion-control runtime.
   --------------------------------------------------------------------- */

/* ---------------------------------------------------------------------
   Quick mobile contact and interaction tracking
   --------------------------------------------------------------------- */
$$('a[href*="contact.html"]').forEach(a=>{if(!a.dataset.track)a.dataset.track='contact_intent'});
if(!$('.mobile-dock'))document.body.insertAdjacentHTML('beforeend','<div class="mobile-dock" aria-label="Quick enquiry"><a href="contact.html" data-track="mobile_enquire">Start enquiry →</a></div>');
document.addEventListener('click',e=>{const a=e.target.closest('[data-track]');if(a)track(a.dataset.track,{href:a.getAttribute('href')||''})});

/* ---------------------------------------------------------------------
   Local performance instrumentation — no third-party request
   --------------------------------------------------------------------- */
(function performanceSample(){
  const sample={event:'site_performance_sample',page:location.pathname,ts:Date.now()};
  addEventListener('DOMContentLoaded',()=>{sample.dom_content_loaded=Math.round(performance.now())},{once:true});
  addEventListener('load',()=>{sample.load=Math.round(performance.now());dataLayer.push(sample)},{once:true});
  if('PerformanceObserver'in window){
    try{new PerformanceObserver(list=>{const e=list.getEntries().at(-1);if(e)sample.lcp=Math.round(e.startTime)}).observe({type:'largest-contentful-paint',buffered:true})}catch(_){}
    try{let cls=0;new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)cls+=e.value;sample.cls=Number(cls.toFixed(4))}).observe({type:'layout-shift',buffered:true})}catch(_){}
  }
})();
