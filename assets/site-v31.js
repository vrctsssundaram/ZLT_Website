'use strict';
(()=>{
 const q=(s,c=document)=>c.querySelector(s),qa=(s,c=document)=>[...c.querySelectorAll(s)];
 qa('[data-year]').forEach(n=>n.textContent=new Date().getFullYear());
 const nav=q('#primary-nav'),toggle=q('.menu-toggle');
 const closeMenus=()=>qa('.nav-group.open').forEach(g=>{g.classList.remove('open');q('button',g).setAttribute('aria-expanded','false')});
 const setMenu=open=>{toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close navigation':'Open navigation');nav.classList.toggle('open',open);document.body.classList.toggle('nav-open',open);if(!open)closeMenus()};
 toggle.addEventListener('click',()=>setMenu(toggle.getAttribute('aria-expanded')!=='true'));
 qa('.nav-disclosure').forEach(b=>b.addEventListener('click',()=>{const open=b.getAttribute('aria-expanded')!=='true';closeMenus();b.setAttribute('aria-expanded',String(open));b.parentElement.classList.toggle('open',open)}));
 document.addEventListener('click',e=>{if(!e.target.closest('.nav-group'))closeMenus()});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'){const active=q('.nav-group.open button');closeMenus();if(toggle.getAttribute('aria-expanded')==='true'){setMenu(false);toggle.focus()}else active?.focus()}});
 addEventListener('resize',()=>{if(innerWidth>960)setMenu(false)},{passive:true});
 const current=location.pathname.split('/').filter(Boolean).pop()||'index.html';
 qa('#primary-nav a').filter(a=>a.getAttribute('href')===current).forEach(a=>{a.setAttribute('aria-current','page');const parent=a.closest('.nav-group');if(parent&&!qa('#primary-nav > a').some(link=>link.getAttribute('href')===current))q('.nav-disclosure',parent).setAttribute('data-current','true')});
 // Progressive hero rotation: keyboard controls, explicit pause, and reduced-motion support.
 const title=q('#hero-title'),desc=q('#hero-description');
 if(title){
  const slides=[['Bring the challenge.','We make it work.','Engineering conversations that turn an open question into a considered next step.'],['Unlocking possibilities.','Through collaboration.','Service and consultancy discussions shaped around your programme, priorities and working context.'],['From an early idea.','To the next stage.','Explore feasibility, development support and research collaboration around a defined requirement.']];
  const reduce=matchMedia('(prefers-reduced-motion: reduce)'),hero=q('.home-hero'),pause=q('#pause-hero');let index=0,paused=reduce.matches,timer=null,hover=false,focused=false;
  function show(i){index=i;title.replaceChildren(document.createTextNode(slides[i][0]),document.createElement('br'));const span=document.createElement('span');span.textContent=slides[i][1];title.append(span);desc.textContent=slides[i][2];qa('[data-slide]').forEach((b,n)=>{b.classList.toggle('active',n===i);b.setAttribute('aria-pressed',String(n===i))});const copy=q('.hero-copy');copy.classList.remove('switching');requestAnimationFrame(()=>copy.classList.add('switching'))}
  function sync(){clearInterval(timer);pause.setAttribute('aria-pressed',String(paused));pause.setAttribute('aria-label',paused?'Resume introduction rotation':'Pause introduction rotation');pause.textContent=paused?'▶':'Ⅱ';if(!paused&&!hover&&!focused&&!document.hidden)timer=setInterval(()=>show((index+1)%slides.length),5000)}
  qa('[data-slide]').forEach(b=>b.addEventListener('click',()=>{show(Number(b.dataset.slide));paused=true;sync()}));
  pause.addEventListener('click',()=>{paused=!paused;sync()});hero.addEventListener('mouseenter',()=>{hover=true;sync()});hero.addEventListener('mouseleave',()=>{hover=false;sync()});hero.addEventListener('focusin',()=>{focused=true;sync()});hero.addEventListener('focusout',()=>{requestAnimationFrame(()=>{focused=hero.contains(document.activeElement);sync()})});document.addEventListener('visibilitychange',sync);reduce.addEventListener('change',()=>{paused=reduce.matches;sync()});sync();
 }
 const search=q('#application-search');if(search){search.addEventListener('input',()=>{const term=search.value.trim().toLowerCase();let n=0;qa('[data-application]').forEach(row=>{row.hidden=!row.dataset.application.toLowerCase().includes(term);if(!row.hidden)n++});q('#application-count').textContent=`${n} application area${n===1?'':'s'}`;q('#no-applications').hidden=n>0});qa('.application-index a').forEach(a=>a.addEventListener('click',()=>{search.value='';search.dispatchEvent(new Event('input'))}))}
 const form=q('#technicalEnquiry');if(form){
  const params=new URLSearchParams(location.search),type=params.get('type'),area=params.get('area'),model=params.get('model'),status=q('#form-status'),fallback=q('#email-fallback');
  const areas={'compute':'Computing & infrastructure','security':'Security & trusted communications','quantum':'Quantum technology & control','edge-ai':'Edge AI & semiconductor products','industrial':'Industrial systems & mobility','autonomous':'Autonomous & embedded systems','space':'Space & mission technology','networks':'Networks & communications','instrumentation':'Sensing & instrumentation','financial':'Financial technology infrastructure','processors':'Processors & open architectures','engineering':'Engineering & design organisations','institutions':'Research & public programmes'};
  const models={consultancy:'Consultancy',project:'Defined work packages',collaboration:'Co-development',ongoing:'Ongoing engineering support'};
  if(type==='meeting')q('#projectType').value='Schedule a meeting';
  const context=areas[area]||models[model]||(type==='meeting'?'Introductory meeting':'');if(context){q('#enquiry-context').textContent='Discussion area: '+context;q('#enquiry-context').hidden=false}
  form.addEventListener('submit',async e=>{
   e.preventDefault();if(form.dataset.submitting)return;if(!form.reportValidity())return;
   const d=new FormData(form),requirement=String(d.get('description')||'').trim();
   if(requirement.length<40){q('#description').setCustomValidity('Please provide at least 40 characters of non-confidential context.');q('#description').reportValidity();return}
   const payload={name:String(d.get('name')).trim(),email:String(d.get('email')).trim(),company:String(d.get('company')).trim(),country:String(d.get('country')||'').trim(),project_type:String(d.get('projectType')),engineering_route:'',technical_requirement:requirement,nda_requested:Boolean(d.get('nda')),selected_ip:'',selected_stage:'',selected_outcome:'',route_context:context||'direct',source_url:location.origin+location.pathname,utm:{},website:String(d.get('website')||'')};
   if(!payload.name||!payload.company){status.textContent='Please enter your name and organisation.';status.className='error';return}
   const button=q('button[type=submit]',form);form.dataset.submitting='true';button.disabled=true;button.textContent='Sending…';status.textContent='Submitting your enquiry…';status.className='';fallback.hidden=true;
   const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),15000);
   try{const r=await fetch('https://nujmuknvhgyoxhxuvscx.supabase.co/functions/v1/website-enquiry',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),signal:controller.signal});const out=await r.json().catch(()=>({}));if(!r.ok||!out.ok)throw new Error('Delivery not confirmed');status.textContent='Your enquiry has been received. Thank you for introducing your requirement.';status.className='success';form.reset();}
   catch(_){status.textContent='Delivery could not be confirmed. Your message is still here. You can try again or prepare an email below.';status.className='error';const body=`Name: ${payload.name}\nEmail: ${payload.email}\nOrganisation: ${payload.company}\nCountry: ${payload.country}\nDiscussion: ${payload.project_type}\nContext: ${context||'General enquiry'}\nConfidentiality discussion requested: ${payload.nda_requested?'Yes':'No'}\n\n${requirement}`;q('#fallback-link').href='mailto:info@zeptologic.com?subject='+encodeURIComponent('Website enquiry — '+payload.company)+'&body='+encodeURIComponent(body);fallback.hidden=false;}
   finally{clearTimeout(timeout);delete form.dataset.submitting;button.disabled=false;button.innerHTML='Send enquiry <span aria-hidden="true">↗</span>'}
  });q('#description').addEventListener('input',()=>q('#description').setCustomValidity(''));
 }
})();
