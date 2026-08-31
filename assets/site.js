const $=(s,c=document)=>c.querySelector(s);const $$=(s,c=document)=>[...c.querySelectorAll(s)];
const header=$('.site-head'),menuBtn=$('.menu-toggle'),nav=$('.head-links');

/* One global navigation taxonomy across legacy and V16 pages. */
function pageGroup(){const p=(location.pathname.split('/').pop()||'index.html').toLowerCase();if(/products|floating-point/.test(p))return'ip';if(/services|rtl-design|verification-coverage|fpga-prototyping|ip-quality|semiconductor-design-partner/.test(p))return'eng';if(/applications/.test(p))return'app';if(/research|cryptographic-hardware|cdot-samarth/.test(p))return'rnd';if(/about/.test(p))return'company';if(/news/.test(p))return'insights';return p==='index.html'||p===''?'technology':''}
function normalizeShell(){if(nav){const current=pageGroup(),items=[['Technology','index.html#technology','technology'],['IP','products.html','ip'],['Engineering','services.html','eng'],['Applications','applications.html','app'],['R&D','research.html','rnd'],['Company','about.html','company'],['Insights','news.html','insights']];nav.innerHTML=items.map(([t,u,g])=>`<a href="${u}"${current===g?' aria-current="page"':''}>${t}</a>`).join('')}const brandP=$('.foot-brand p');if(brandP)brandP.textContent='Digital semiconductor IP, front-end engineering and applied hardware R&D.';const footTitle=$('.foot-top h2');if(footTitle&&/Indian|indigenous/i.test(footTitle.textContent))footTitle.textContent='Semiconductor IP and engineering for advanced hardware systems.'}
normalizeShell();
function setMenu(open){if(!nav||!menuBtn)return;if(!nav.id)nav.id='primaryNavigation';menuBtn.setAttribute('aria-controls',nav.id);nav.classList.toggle('open',open);document.body.classList.toggle('nav-open',open);menuBtn.setAttribute('aria-expanded',String(open));menuBtn.setAttribute('aria-label',open?'Close navigation':'Open navigation');menuBtn.textContent=open?'Close':'Menu'}
menuBtn?.addEventListener('click',()=>setMenu(!nav.classList.contains('open')));nav?.addEventListener('click',e=>{if(e.target.closest('a'))setMenu(false)});matchMedia('(min-width:981px)').addEventListener?.('change',e=>{if(e.matches)setMenu(false)});const syncHeader=()=>header?.classList.toggle('scrolled',scrollY>8);syncHeader();addEventListener('scroll',syncHeader,{passive:true});

/* Permanently retired experimental UI. */
$$('.nexus-bar,.nexus-console,.ecosystem-section,.silicon-workbench,.intent-lab,.ui-disclosures,.engagement-path,.service-flow').forEach(el=>el.remove());sessionStorage.removeItem('zl_audience');

/* V18 compact conversion dock. */
if(document.body.classList.contains('v16')&&!$('#v16RuntimeStyle')){document.head.insertAdjacentHTML('beforeend','<style id="v16RuntimeStyle">.hp-field{position:absolute!important;left:-10000px!important;width:1px!important;height:1px!important;overflow:hidden!important}.mobile-dock{display:none}@media(max-width:760px){body.v16{padding-bottom:72px}.mobile-dock{position:fixed;z-index:130;left:max(12px,env(safe-area-inset-left));right:max(12px,env(safe-area-inset-right));bottom:max(10px,env(safe-area-inset-bottom));display:grid;grid-template-columns:.72fr 1.28fr;gap:4px;padding:4px;border-radius:999px;background:rgba(5,14,32,.94);border:1px solid rgba(255,255,255,.16);box-shadow:0 16px 42px rgba(3,10,24,.28);backdrop-filter:blur(18px)}.mobile-dock a{min-height:50px;display:flex;align-items:center;justify-content:center;border-radius:999px;font-size:12px;font-weight:800;color:#edf4ff}.mobile-dock a+ a{background:linear-gradient(115deg,#ffd246,#ff8a37 58%,#ff6b4a);color:#071426}}</style>')}

function track(event,detail={}){window.dataLayer=window.dataLayer||[];window.dataLayer.push({event,...detail})}function wireTracking(){$$('[data-track]').forEach(el=>{if(el.dataset.trackBound)return;el.dataset.trackBound='1';el.addEventListener('click',()=>track(el.dataset.track,{page:location.pathname,label:el.textContent.trim().slice(0,100)}))})}

/* Search */
let lastSearchFocus=null;const searchIndex=[['Semiconductor IP','products.html','semiconductor IP floating point arithmetic UART SPI I2C license evaluate reusable'],['Applications','applications.html','compute signal processing embedded control communications security edge research hardware'],['Floating-point IP','floating-point-ip.html','IEEE 754 add subtract multiplier divider reciprocal square root MAC complex matrix'],['RTL Design','rtl-design-services.html','Verilog SystemVerilog VHDL microarchitecture RTL design'],['Verification','verification-coverage-closure.html','UVM coverage regression assertions verification'],['FPGA Prototyping','fpga-prototyping-services.html','AMD Xilinx Zynq Alveo prototype timing bring-up'],['IP Quality','ip-quality-audit.html','lint CDC RDC reuse readiness RTL audit'],['Cryptographic Hardware','cryptographic-hardware-acceleration.html','zk SNARK PQC cryptography accelerator FPGA'],['Research to Hardware','research-to-hardware.html','research co-development architecture FPGA hardware'],['C-DOT Samarth','cdot-samarth-zksnark.html','C-DOT Samarth zk SNARK zero knowledge FPGA Stage II grant'],['Company','about.html','Zepto Logic company Coimbatore semiconductor'],['R&D','research.html','research secure hardware cryptography acceleration'],['Insights','news.html','news C-DOT Tamil Nadu TNRPF company milestones'],['Careers','careers.html','VLSI RTL verification FPGA careers internship'],['Contact','contact.html','technical enquiry phone WhatsApp email']];const dialog=$('.search-dialog'),input=$('#siteSearch'),results=$('.search-results');function openSearch(){setMenu(false);lastSearchFocus=document.activeElement;dialog?.classList.add('open');dialog?.setAttribute('aria-hidden','false');dialog?.setAttribute('role','dialog');dialog?.setAttribute('aria-modal','true');dialog?.setAttribute('aria-label','Search Zepto Logic');document.body.style.overflow='hidden';setTimeout(()=>input?.focus(),40)}function closeSearch(){const wasOpen=dialog?.classList.contains('open');dialog?.classList.remove('open');dialog?.setAttribute('aria-hidden','true');if(!document.body.classList.contains('nav-open'))document.body.style.overflow='';if(wasOpen&&lastSearchFocus instanceof HTMLElement)setTimeout(()=>lastSearchFocus.focus(),0)}function runSearch(v=''){if(!results)return;const terms=v.toLowerCase().trim().split(/\s+/).filter(Boolean);if(!terms.length){results.innerHTML='<p>Search semiconductor IP, engineering, applications, R&D or company information.</p>';return}const found=searchIndex.filter(([t,,x])=>terms.every(term=>(t+' '+x).toLowerCase().includes(term))).slice(0,9);results.innerHTML=found.length?found.map(([t,u])=>`<a class="search-result" href="${u}"><strong>${t}</strong><span>Open →</span></a>`).join(''):'<p>No direct match. <a href="contact.html">Contact Zepto Logic →</a></p>'}$$('.search-button').forEach(b=>{b.setAttribute('aria-label','Search site');b.addEventListener('click',openSearch)});$('.search-close')?.addEventListener('click',closeSearch);dialog?.addEventListener('click',e=>{if(e.target===dialog)closeSearch()});input?.addEventListener('input',e=>runSearch(e.target.value));document.addEventListener('keydown',e=>{if(e.key==='Escape'){setMenu(false);closeSearch()}if(e.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName||'')){e.preventDefault();openSearch()}if(e.key==='Tab'&&dialog?.classList.contains('open')){const focusable=$$('a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])',dialog).filter(x=>x.offsetParent!==null);if(focusable.length){const first=focusable[0],last=focusable[focusable.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}}});

/* IP catalogue filter — no injected FAQ or qualification copy. */
if(location.pathname.endsWith('products.html')||location.pathname.endsWith('/products/')){const listings=$$('.listing'),rows=$$('.listing-row');listings.forEach((listing,i)=>$$('.listing-row',listing).forEach(r=>r.dataset.ipCategory=i===0?'arithmetic':'interface'));const first=listings[0];if(first&&rows.length){const tools=document.createElement('div');tools.className='ip-explorer-tools';tools.setAttribute('role','region');tools.setAttribute('aria-label','IP portfolio filter');tools.innerHTML='<div class="ip-filter-group" role="group" aria-label="Filter IP by category"><button type="button" class="ip-filter active" data-filter="all" aria-pressed="true">All</button><button type="button" class="ip-filter" data-filter="arithmetic" aria-pressed="false">Arithmetic</button><button type="button" class="ip-filter" data-filter="interface" aria-pressed="false">Interfaces</button></div><label class="ip-search-field"><span class="sr-only">Search IP portfolio</span><input class="ip-search" type="search" aria-label="Search IP portfolio" placeholder="Search the portfolio"></label><span class="ip-explorer-count" role="status" aria-live="polite"></span>';first.closest('.z-section,.section')?.querySelector('.z-head,.section-head')?.after(tools);let filter='all';const search=$('.ip-search',tools),count=$('.ip-explorer-count',tools);function apply(){const q=(search.value||'').trim().toLowerCase();let visible=0;rows.forEach(r=>{const show=(filter==='all'||r.dataset.ipCategory===filter)&&(!q||r.textContent.toLowerCase().includes(q));r.hidden=!show;r.style.display=show?'':'none';if(show)visible++});count.textContent=`${visible} of ${rows.length} blocks`}$$('.ip-filter',tools).forEach(b=>b.addEventListener('click',()=>{filter=b.dataset.filter;$$('.ip-filter',tools).forEach(x=>{const active=x===b;x.classList.toggle('active',active);x.setAttribute('aria-pressed',String(active))});apply();track('ip_portfolio_filtered',{filter})}));search.addEventListener('input',apply);apply()}}

/* Enquiry prefill + protected backend submission. */
const params=new URLSearchParams(location.search),project=$('#projectType'),service=$('#service'),description=$('#description');const projectMap={ip:'IP licensing / evaluation',research:'Research collaboration',services:'General technical enquiry',partnership:'Strategic partnership'};const serviceMap={rtl:'RTL design',verification:'UVM verification','verification-audit':'UVM verification',fpga:'FPGA prototyping','ip-quality':'IP quality audit',architecture:'Architecture assessment'};const projectByService={rtl:'RTL design',verification:'Verification / coverage closure','verification-audit':'Verification / coverage closure',fpga:'FPGA prototyping','ip-quality':'IP quality / readiness audit',architecture:'Architecture / specification'};const ipMap={'fp-add-sub':'FP Adder / Subtractor','fp-multiplier':'FP Multiplier','fp-divider':'FP Divider','fp-reciprocal':'FP Reciprocal','fp-sqrt':'FP Square Root','fp-invsqrt':'FP Inverse Square Root','fp-mac':'FP Multiply-Accumulate','fp-complex':'FP Complex Multiplier','fp-matrix':'FP Complex Matrix Multiplier N×N','uart':'UART Controller','spi':'SPI Controller','i2c':'I²C Controller','i2c-master':'I²C Master'};if(project&&projectMap[params.get('type')])project.value=projectMap[params.get('type')];if(service&&serviceMap[params.get('service')])service.value=serviceMap[params.get('service')];if(project&&projectByService[params.get('service')])project.value=projectByService[params.get('service')];if(project&&params.get('ip'))project.value='IP licensing / evaluation';if(service&&params.get('ip'))service.value='Semiconductor IP';const context=[];if(params.get('ip'))context.push(`IP: ${ipMap[params.get('ip')]||params.get('ip')}`);if(params.get('service'))context.push(`Workstream: ${serviceMap[params.get('service')]||params.get('service')}`);if(context.length&&description&&!$('.route-context')){const box=document.createElement('div');box.className='route-context';box.setAttribute('role','note');box.innerHTML=`<strong>Selected context</strong><br>${context.map(x=>x.replace(/[<>]/g,'')).join(' · ')}`;description.closest('form')?.prepend(box)}
const utmKeys=['utm_source','utm_medium','utm_campaign','utm_term','utm_content'],utm={};utmKeys.forEach(k=>{const v=params.get(k)||sessionStorage.getItem(`zl_${k}`);if(v){utm[k]=v;sessionStorage.setItem(`zl_${k}`,v)}});const form=$('#technicalEnquiry');if(form&&!$('[name="website"]',form))form.insertAdjacentHTML('afterbegin','<div aria-hidden="true" class="hp-field"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>');if(description){const field=description.closest('.field'),help=$('.form-help',field);if(help&&!help.id)help.id='descriptionHelp';let counter=$('.field-counter',field);if(!counter){counter=document.createElement('span');counter.className='field-counter';counter.id='descriptionCounter';field.append(counter)}description.setAttribute('aria-describedby',[description.getAttribute('aria-describedby'),help?.id,counter.id].filter(Boolean).join(' '));const updateCounter=()=>{const n=description.value.trim().length,ready=n>=40;counter.classList.toggle('ready',ready);counter.textContent=ready?`${n} characters · ready to send`:`${n}/40 minimum`};description.addEventListener('input',updateCounter);updateCounter()}
const ENDPOINT='https://nujmuknvhgyoxhxuvscx.supabase.co/functions/v1/website-enquiry';function emailFallback(d,requirement){const subject=encodeURIComponent(`[Website enquiry] ${d.get('projectType')} — ${d.get('company')}`),body=encodeURIComponent(`Name: ${d.get('name')}\nEmail: ${d.get('email')}\nCompany: ${d.get('company')}\nCountry: ${d.get('country')||'Not specified'}\nRequirement: ${d.get('projectType')}\nEngineering route: ${d.get('service')||'Not specified'}\nCurrent stage: ${d.get('stage')||'Not specified'}\nNeeded next: ${d.get('outcome')||'Not specified'}\nSelected IP: ${params.get('ip')?(ipMap[params.get('ip')]||params.get('ip')):'n/a'}\nNDA requested: ${d.get('nda')?'Yes':'No'}\n\nTechnical requirement:\n${requirement}`);location.href=`mailto:info@zeptologic.com?subject=${subject}&body=${body}`}
form?.addEventListener('submit',async e=>{e.preventDefault();const d=new FormData(form),err=$('.form-error',form),notice=$('.notice',form),btn=$('button[type="submit"]',form),requirement=String(d.get('description')||'').trim(),email=String(d.get('email')||'').trim().toLowerCase(),domain=email.split('@')[1]||'';if(err){err.style.display='none';err.setAttribute('tabindex','-1')}if(notice)notice.textContent='';if(requirement.length<40){if(err){err.textContent='Please provide at least 40 characters of technical context.';err.style.display='block';err.focus()}return}const payload={name:String(d.get('name')||''),email:String(d.get('email')||''),company:String(d.get('company')||''),country:String(d.get('country')||''),project_type:String(d.get('projectType')||''),engineering_route:String(d.get('service')||''),technical_requirement:requirement,nda_requested:Boolean(d.get('nda')),selected_ip:params.get('ip')?(ipMap[params.get('ip')]||params.get('ip')):'',selected_stage:String(d.get('stage')||params.get('stage')||''),selected_outcome:String(d.get('outcome')||params.get('outcome')||''),route_context:params.get('ip')||params.get('service')||params.get('type')||'direct',source_url:location.href,utm,website:String(d.get('website')||'')},old=btn?.textContent||'Send enquiry';if(btn){btn.disabled=true;btn.textContent='Sending…'}if(notice)notice.textContent='Sending securely…';try{const r=await fetch(ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}),out=await r.json().catch(()=>({}));if(!r.ok||!out.ok)throw new Error(out.error||`HTTP ${r.status}`);track('technical_enquiry_submitted',{project_type:payload.project_type,engineering_route:payload.engineering_route,...utm});const next=new URL('enquiry-received.html',location.href);if(out.enquiry_id)next.searchParams.set('id',out.enquiry_id);location.href=next.toString()}catch(ex){console.error(ex);if(err){err.textContent='Secure delivery could not be confirmed. Your email application will open with the enquiry prepared.';err.style.display='block'}emailFallback(d,requirement)}finally{if(btn){btn.disabled=false;btn.textContent=old}}});

$$('a[href*="contact.html"]').forEach(a=>{if(!a.dataset.track)a.dataset.track='contact_intent'});if(!$('.mobile-dock'))document.body.insertAdjacentHTML('beforeend','<div class="mobile-dock" aria-label="Quick contact"><a href="tel:+919626632233" data-track="mobile_call">Call</a><a href="contact.html" data-track="mobile_enquire">Start enquiry →</a></div>');function viewportMode(){const w=innerWidth;document.documentElement.dataset.viewport=w<=430?'compact-phone':w<=760?'phone':w<=980?'tablet':w<=1199?'laptop':w>=1600?'wide-desktop':'desktop'}viewportMode();addEventListener('resize',viewportMode,{passive:true});$$('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());wireTracking();

/* V18 — colour, motion and interaction layer. Vanilla JS; progressive enhancement only. */
(function v18Experience(){
  const reduce=matchMedia('(prefers-reduced-motion: reduce)');
  const fine=matchMedia('(hover:hover) and (pointer:fine)');
  const raw=(location.pathname.split('/').pop()||'index.html').replace(/\.html$/,'').toLowerCase();
  const page=raw==='index'||raw===''?'home':raw.replace(/[^a-z0-9]+/g,'-');
  document.body.classList.add('page-'+page);
  document.documentElement.classList.add('v18');
  if(!reduce.matches)document.body.classList.add('motion-ready');

  if(!document.querySelector('.scroll-progress'))document.body.insertAdjacentHTML('afterbegin','<div class="scroll-progress" aria-hidden="true"><i></i></div>');
  const progress=document.querySelector('.scroll-progress');
  let scrollTick=false;
  const syncProgress=()=>{const max=document.documentElement.scrollHeight-innerHeight,ratio=max>0?Math.min(1,Math.max(0,scrollY/max)):0;progress?.style.setProperty('--scroll',ratio.toFixed(4));scrollTick=false};
  addEventListener('scroll',()=>{if(!scrollTick){scrollTick=true;requestAnimationFrame(syncProgress)}},{passive:true});syncProgress();

  const revealTargets=[...document.querySelectorAll('main .z-head,main .z-card,main .z-app,main .z-topic,main .z-flow article,main .z-feature-story,main .listing-row,main .contact-shell')];
  revealTargets.forEach((el,i)=>{el.classList.add('reveal-v18');el.style.transitionDelay=(i%4)*55+'ms'});
  if(!reduce.matches&&'IntersectionObserver'in window){
    const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target)}}),{threshold:.09,rootMargin:'0px 0px -5% 0px'});
    revealTargets.forEach(el=>io.observe(el));
  }else revealTargets.forEach(el=>el.classList.add('is-visible'));

  if(fine.matches&&!reduce.matches){
    document.querySelectorAll('.z-card[href],.z-app[href]').forEach(card=>{
      card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect();card.style.setProperty('--mx',((e.clientX-r.left)/r.width*100).toFixed(1)+'%');card.style.setProperty('--my',((e.clientY-r.top)/r.height*100).toFixed(1)+'%')},{passive:true});
    });
    const stage=document.querySelector('.silicon-scene');
    stage?.addEventListener('pointermove',e=>{const r=stage.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;stage.style.transform='perspective(900px) rotateX('+(-y*4).toFixed(2)+'deg) rotateY('+(x*5).toFixed(2)+'deg)'},{passive:true});
    stage?.addEventListener('pointerleave',()=>stage.style.transform='');

    document.querySelectorAll('.magnetic,.project-link').forEach(el=>{
      el.addEventListener('pointermove',e=>{const r=el.getBoundingClientRect(),x=e.clientX-r.left-r.width/2,y=e.clientY-r.top-r.height/2;el.style.transform='translate('+(x*.08).toFixed(1)+'px,'+(y*.08).toFixed(1)+'px) translateY(-2px)'},{passive:true});
      el.addEventListener('pointerleave',()=>el.style.transform='');
    });

    if(document.body.classList.contains('v16')&&!document.querySelector('.cursor-glow')){
      const glow=document.createElement('div');glow.className='cursor-glow';glow.setAttribute('aria-hidden','true');document.body.append(glow);
      let px=innerWidth/2,py=innerHeight/2,gx=px,gy=py,raf=0;
      const animate=()=>{gx+=(px-gx)*.12;gy+=(py-gy)*.12;glow.style.transform='translate3d('+gx+'px,'+gy+'px,0)';raf=requestAnimationFrame(animate)};
      addEventListener('pointermove',e=>{px=e.clientX;py=e.clientY;glow.classList.add('on');if(!raf)animate()},{passive:true});
      addEventListener('pointerleave',()=>glow.classList.remove('on'),{passive:true});
    }
  }

  if(!reduce.matches&&'IntersectionObserver'in window){
    const metrics=[...document.querySelectorAll('[data-count]')];
    const counterIO=new IntersectionObserver(entries=>entries.forEach(entry=>{
      if(!entry.isIntersecting)return;
      const el=entry.target,target=Number(el.dataset.count)||0,start=performance.now(),duration=850;
      const tick=now=>{const p=Math.min(1,(now-start)/duration),eased=1-Math.pow(1-p,3);el.textContent=String(Math.round(target*eased));if(p<1)requestAnimationFrame(tick)};
      requestAnimationFrame(tick);counterIO.unobserve(el);
    }),{threshold:.7});
    metrics.forEach(el=>counterIO.observe(el));
  }
})();


/* V19 — original hero film controls, energy-aware playback and conversion beacon. */
(function v19CinematicMotion(){
  const film=document.querySelector('[data-hero-film]');
  const toggle=document.querySelector('[data-film-toggle]');
  const hero=document.querySelector('.v19-hero');
  const beacon=document.querySelector('[data-project-beacon]');
  if(!hero)return;
  const reduce=matchMedia('(prefers-reduced-motion: reduce)');
  const fine=matchMedia('(hover:hover) and (pointer:fine)');
  const saveData=Boolean(navigator.connection&&navigator.connection.saveData);
  let userPaused=reduce.matches||saveData;
  let inView=true;

  function setFilmState(running){
    if(!film)return;
    const shouldRun=running&&!reduce.matches&&inView&&!document.hidden;
    if(shouldRun){
      const p=film.play();
      if(p&&p.catch)p.catch(()=>{document.body.classList.add('film-static')});
      film.dataset.motion='running';
      document.body.classList.remove('film-static');
    }else{
      film.pause();
      film.dataset.motion='paused';
      document.body.classList.add('film-static');
    }
    if(toggle){
      toggle.setAttribute('aria-pressed',String(!running));
      toggle.innerHTML=running?'<span aria-hidden="true">Ⅱ</span> Pause motion':'<span aria-hidden="true">▶</span> Play motion';
    }
  }

  setFilmState(!userPaused);
  toggle?.addEventListener('click',()=>{
    userPaused=!userPaused;
    setFilmState(!userPaused);
    window.dataLayer=window.dataLayer||[];
    window.dataLayer.push({event:'hero_motion_toggle',state:userPaused?'paused':'playing',page:location.pathname});
  });

  if('IntersectionObserver'in window&&film){
    const io=new IntersectionObserver(entries=>{
      const entry=entries[0]; inView=Boolean(entry&&entry.isIntersecting);
      setFilmState(!userPaused);
    },{threshold:.08});
    io.observe(hero);
  }
  document.addEventListener('visibilitychange',()=>setFilmState(!userPaused));
  reduce.addEventListener?.('change',e=>{if(e.matches)userPaused=true;setFilmState(!userPaused)});

  if(fine.matches&&!reduce.matches){
    hero.addEventListener('pointermove',e=>{
      const r=hero.getBoundingClientRect();
      const x=((e.clientX-r.left)/r.width-.5)*-14;
      const y=((e.clientY-r.top)/r.height-.5)*-9;
      hero.style.setProperty('--film-x',x.toFixed(1)+'px');
      hero.style.setProperty('--film-y',y.toFixed(1)+'px');
    },{passive:true});
    hero.addEventListener('pointerleave',()=>{hero.style.setProperty('--film-x','0px');hero.style.setProperty('--film-y','0px')},{passive:true});
  }

  if(beacon){
    let ticking=false;
    const syncBeacon=()=>{
      const threshold=Math.max(520,hero.offsetHeight*.72);
      beacon.classList.toggle('show',scrollY>threshold&&scrollY<document.documentElement.scrollHeight-innerHeight-520);
      ticking=false;
    };
    addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(syncBeacon)}},{passive:true});
    syncBeacon();
  }
})();


/* V20 — prism interactions, capability playground and section navigation. */
(function v20PrismSystem(){
  if(!document.body.classList.contains('v20'))return;
  const reduce=matchMedia('(prefers-reduced-motion: reduce)');
  const fine=matchMedia('(hover:hover) and (pointer:fine)');

  /* Give each major section a restrained colour chapter and visible index. */
  const tones=['cyan','violet','coral','mint','cyan','violet','coral','mint'];
  const sections=[...document.querySelectorAll('main>section')].filter(s=>!s.classList.contains('tech-marquee')&&!s.classList.contains('v20-color-rail')&&!s.classList.contains('z-proofline'));
  sections.forEach((s,i)=>{
    if(!s.dataset.v20Tone)s.dataset.v20Tone=tones[i%tones.length];
    const head=s.querySelector('.z-head>div:first-child,.motion-story-head>div:first-child,.v20-playground-head>div:first-child');
    if(head&&!head.querySelector('.v20-section-index')){
      const badge=document.createElement('span');badge.className='v20-section-index';badge.textContent=String(i+1).padStart(2,'0');head.prepend(badge);
    }
  });

  const playground=document.querySelector('[data-playground]');
  if(playground){
    const data={
      ip:{a:'#27e6ff',b:'#3c67ff',stat:'13',label:'FPGA-validated blocks',kicker:'LICENSE',title:'Reuse a proven function.',copy:'Evaluate arithmetic or interface IP before committing time to rebuilding the same function inside your programme.',href:'products.html',link:'Explore the IP portfolio →'},
      rtl:{a:'#8c5cff',b:'#ff4fa3',stat:'RTL',label:'Architecture to synthesizable logic',kicker:'IMPLEMENT',title:'Build the differentiating logic.',copy:'Translate a bounded requirement into microarchitecture, datapaths, control, interfaces and integration-ready RTL.',href:'contact.html?service=rtl',link:'Discuss RTL engineering →'},
      verify:{a:'#ff4fa3',b:'#ff9b43',stat:'UVM',label:'Assertions · regression · coverage',kicker:'VERIFY',title:'Turn behavior into engineering evidence.',copy:'Strengthen new or inherited RTL with assertions, regression, coverage, lint and CDC/RDC work appropriate to the block.',href:'contact.html?service=verification',link:'Discuss verification →'},
      fpga:{a:'#49efbb',b:'#27e6ff',stat:'FPGA',label:'Timing · bring-up · repeatable proof',kicker:'PROVE',title:'Take the design onto hardware.',copy:'Move RTL through constraints, implementation, timing closure, platform bring-up and repeatable hardware evidence.',href:'contact.html?service=fpga',link:'Discuss FPGA proof →'}
    };
    const tabs=[...playground.querySelectorAll('[data-play]')];
    const stat=playground.querySelector('[data-play-stat]'),label=playground.querySelector('[data-play-stat-label]'),kicker=playground.querySelector('[data-play-kicker]'),title=playground.querySelector('[data-play-title]'),copy=playground.querySelector('[data-play-copy]'),link=playground.querySelector('[data-play-link]');
    function activate(key,focus=false){
      const d=data[key];if(!d)return;
      playground.style.setProperty('--play-a',d.a);playground.style.setProperty('--play-b',d.b);
      tabs.forEach(t=>{const on=t.dataset.play===key;t.classList.toggle('active',on);t.setAttribute('aria-selected',String(on));if(on&&focus)t.focus()});
      if(stat)stat.textContent=d.stat;if(label)label.textContent=d.label;if(kicker)kicker.textContent=d.kicker;if(title)title.textContent=d.title;if(copy)copy.textContent=d.copy;if(link){link.href=d.href;link.textContent=d.link}
      window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'capability_playground_selected',route:key,page:location.pathname});
    }
    tabs.forEach((tab,i)=>{
      tab.addEventListener('click',()=>activate(tab.dataset.play));
      tab.addEventListener('keydown',e=>{if(!['ArrowDown','ArrowUp','ArrowRight','ArrowLeft'].includes(e.key))return;e.preventDefault();const delta=['ArrowDown','ArrowRight'].includes(e.key)?1:-1;const next=tabs[(i+delta+tabs.length)%tabs.length];activate(next.dataset.play,true)});
    });
  }

  /* Desktop chapter dots — a compact navigation aid, not a second primary nav. */
  if(document.body.classList.contains('page-home')&&innerWidth>980){
    const nav=document.createElement('aside');nav.className='v20-section-nav';nav.setAttribute('aria-label','Homepage sections');
    const navSections=[...document.querySelectorAll('main>section[id],main>section.v20-prism-playground,main>section.technology-section,main>section.applications-spectrum,main>section.research-spectrum,main>section.trust-reasons')].filter((s,i,a)=>a.indexOf(s)===i);
    navSections.slice(0,8).forEach((s,i)=>{
      if(!s.id)s.id='section-'+(i+1);
      const heading=s.querySelector('h1,h2');const label=(heading?.textContent||'Section '+(i+1)).trim().slice(0,58);
      const b=document.createElement('button');b.type='button';b.dataset.label=label;b.setAttribute('aria-label','Go to '+label);b.addEventListener('click',()=>s.scrollIntoView({behavior:reduce.matches?'auto':'smooth',block:'start'}));nav.append(b);
    });
    document.body.append(nav);
    if('IntersectionObserver'in window){
      const buttons=[...nav.querySelectorAll('button')];
      const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){buttons.forEach(b=>b.classList.remove('active'));const idx=navSections.slice(0,8).indexOf(e.target);if(buttons[idx])buttons[idx].classList.add('active')}}),{threshold:.32,rootMargin:'-16% 0px -52% 0px'});
      navSections.slice(0,8).forEach(s=>io.observe(s));
    }
  }

  /* Restrained 3D tilt on interactive surfaces. */
  if(fine.matches&&!reduce.matches){
    const tilt=[...document.querySelectorAll('.v20-bento-card,.motion-pipeline a,.z-card[href],.z-app[href]')];
    tilt.forEach(el=>{
      el.classList.add('v20-tilt');
      el.addEventListener('pointermove',e=>{const r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;el.style.setProperty('--tilt-y',(x*3.3).toFixed(2)+'deg');el.style.setProperty('--tilt-x',(-y*3.0).toFixed(2)+'deg')},{passive:true});
      el.addEventListener('pointerleave',()=>{el.style.setProperty('--tilt-x','0deg');el.style.setProperty('--tilt-y','0deg')});
    });
  }

  /* Small tactile ripple on major CTA surfaces. */
  document.querySelectorAll('.action.primary,.project-link,.v20-core-link').forEach(el=>{
    el.classList.add('v20-ripple-host');
    el.addEventListener('pointerdown',e=>{
      if(reduce.matches)return;
      const r=el.getBoundingClientRect(),sp=document.createElement('span');sp.className='v20-ripple';sp.style.left=(e.clientX-r.left)+'px';sp.style.top=(e.clientY-r.top)+'px';el.append(sp);setTimeout(()=>sp.remove(),700);
    });
  });
})();
