const q=(s,c=document)=>c.querySelector(s);const qa=(s,c=document)=>[...c.querySelectorAll(s)];

// Mobile navigation
q('.menu-btn')?.addEventListener('click',()=>{const links=q('.links');links?.classList.toggle('open');q('.menu-btn')?.setAttribute('aria-expanded',String(links?.classList.contains('open')))});

// Lightweight reveal motion
if('IntersectionObserver'in window){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}}),{threshold:.08});qa('.reveal').forEach(e=>io.observe(e))}else{qa('.reveal').forEach(e=>e.classList.add('visible'))}

// Persistent theme
const themeButton=q('.theme-toggle');
function applyTheme(theme){document.documentElement.dataset.theme=theme;const dark=theme==='dark';if(themeButton){themeButton.setAttribute('aria-pressed',String(dark));themeButton.setAttribute('aria-label',dark?'Switch to light theme':'Switch to dark theme');themeButton.querySelector('.theme-icon')&&(themeButton.querySelector('.theme-icon').textContent=dark?'☀':'◐')}const meta=q('meta[name="theme-color"]');if(meta)meta.content=dark?'#0b1113':'#f3f4ef'}
applyTheme(document.documentElement.dataset.theme||'light');themeButton?.addEventListener('click',()=>{const next=document.documentElement.dataset.theme==='dark'?'light':'dark';localStorage.setItem('zl-theme',next);applyTheme(next)});

// Product filtering
qa('[data-filter]').forEach(btn=>btn.addEventListener('click',()=>{qa('[data-filter]').forEach(x=>x.classList.remove('active'));btn.classList.add('active');const target=btn.dataset.filter;qa('.spec-row[data-category]').forEach(row=>row.classList.toggle('hidden',target!=='all'&&row.dataset.category!==target))}));

// Search: static and dependency-free for GitHub Pages.
const SITE_INDEX=[
 {title:'IP Portfolio',url:'products.html',text:'13 FPGA validated semiconductor IP cores floating point IEEE 754 UART SPI I2C arithmetic interface soft IP'},
 {title:'Floating-point IP',url:'floating-point-ip.html',text:'floating point IP IEEE 754 FP32 multiplier divider square root inverse square root MAC complex matrix soft IP'},
 {title:'RTL Design Services',url:'rtl-design-services.html',text:'RTL design outsourcing India Verilog SystemVerilog VHDL microarchitecture lint CDC synthesis integration'},
 {title:'Verification & Coverage Closure',url:'verification-coverage-closure.html',text:'UVM verification coverage closure regression constrained random assertions formal verification readiness audit'},
 {title:'FPGA Prototyping Services',url:'fpga-prototyping-services.html',text:'FPGA prototyping services India AMD Xilinx Zynq UltraScale Alveo timing bring up bitstream'},
 {title:'IP Quality Audit',url:'ip-quality-audit.html',text:'IP quality audit RTL lint CDC RDC code quality readiness integration synthesis audit'},
 {title:'Cryptographic Hardware Acceleration',url:'cryptographic-hardware-acceleration.html',text:'zk-SNARK hardware accelerator cryptography post quantum PQC FPGA proof generation modular arithmetic'},
 {title:'Research to Hardware',url:'research-to-hardware.html',text:'academic research industrial hardening RTL verification FPGA validation technology transfer'},
 {title:'Semiconductor Design Partner India',url:'semiconductor-design-partner-india.html',text:'semiconductor design company India partner indigenous programme Coimbatore Tamil Nadu RTL verification FPGA'},
 {title:'Services',url:'services.html',text:'architecture RTL design verification UVM lint CDC RDC FPGA prototyping IP quality services'},
 {title:'Research & Development',url:'research.html',text:'zk-SNARK hardware cryptography post quantum secure edge computing perovskite research programmes'},
 {title:'Company',url:'about.html',text:'Zepto Logic Coimbatore fabless semiconductor DPIIT recognised C-DOT CDIIC Tamil Nadu'},
 {title:'Newsroom',url:'news.html',text:'C-DOT Samarth Tamil Nadu Government memorandum DPIIT TNRPF CDIIC land allotment'},
 {title:'Careers',url:'careers.html',text:'VLSI RTL verification FPGA engineering careers Coimbatore internship'},
 {title:'Contact',url:'contact.html',text:'technical enquiry semiconductor IP RTL verification FPGA research collaboration contact'}
];
const searchDialog=q('.search-dialog');const searchInput=q('#siteSearch');const searchResults=q('.search-results');
function renderSearch(term=''){if(!searchResults)return;const tokens=term.trim().toLowerCase().split(/\s+/).filter(Boolean);if(!tokens.length){searchResults.innerHTML='<p class="muted">Search IP, RTL, verification, FPGA, research or company information.</p>';return}const matches=SITE_INDEX.filter(x=>{const haystack=(x.title+' '+x.text).toLowerCase();return tokens.every(token=>haystack.includes(token))}).slice(0,10);searchResults.innerHTML=matches.length?matches.map(x=>`<a class="search-result" href="${x.url}"><strong>${x.title}</strong><small>${x.text.split(' ').slice(0,12).join(' ')}…</small></a>`).join(''):'<p class="muted">No direct match. Try a shorter technical term.</p>'}
function openSearch(){searchDialog?.classList.add('open');searchDialog?.setAttribute('aria-hidden','false');setTimeout(()=>searchInput?.focus(),50)}function closeSearch(){searchDialog?.classList.remove('open');searchDialog?.setAttribute('aria-hidden','true')}
q('.search-toggle')?.addEventListener('click',openSearch);q('.search-close')?.addEventListener('click',closeSearch);searchDialog?.addEventListener('click',e=>{if(e.target===searchDialog)closeSearch()});document.addEventListener('keydown',e=>{if(e.key==='Escape')closeSearch()});searchInput?.addEventListener('input',e=>renderSearch(e.target.value));

// Analytics hooks. GTM/GA/Clarity can be connected later without changing CTA markup.
function track(name,detail={}){window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:name,...detail})}
qa('[data-track]').forEach(el=>el.addEventListener('click',()=>track(el.dataset.track,{page:location.pathname,label:el.textContent.trim().slice(0,80)})));

// Query-string prefill for contextual technical-enquiry links.
const params=new URLSearchParams(location.search);const project=q('#projectType');const service=q('#service');
const mapProject={ip:'IP licensing / evaluation',services:'General technical enquiry',research:'Research collaboration'};
const mapService={verification:'UVM verification','verification-audit':'UVM verification',rtl:'RTL design',fpga:'FPGA prototyping','ip-quality':'IP quality audit'};
const serviceToProject={verification:'Verification / coverage closure','verification-audit':'Verification / coverage closure',rtl:'RTL design',fpga:'FPGA prototyping','ip-quality':'IP quality / readiness audit'};
if(project&&params.get('type')&&mapProject[params.get('type')])project.value=mapProject[params.get('type')];if(service&&params.get('service')&&mapService[params.get('service')])service.value=mapService[params.get('service')];if(project&&params.get('service')&&serviceToProject[params.get('service')])project.value=serviceToProject[params.get('service')];if(project&&params.get('ip'))project.value='IP licensing / evaluation';if(service&&params.get('ip'))service.value='Semiconductor IP';

// Technical enquiry validation and mail fallback until production lead-routing backend is connected.
const FREE_DOMAINS=['gmail.com','yahoo.com','outlook.com','hotmail.com','icloud.com','proton.me','protonmail.com','rediffmail.com'];const form=q('#technicalEnquiry');
form?.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(form);const email=String(d.get('email')||'').trim().toLowerCase();const domain=email.split('@')[1]||'';const err=q('.form-error',form);const notice=q('.notice',form);if(FREE_DOMAINS.includes(domain)){if(err){err.style.display='block';err.textContent='A work email helps us route technical enquiries correctly. If you do not have one, email info@zeptologic.com and include your organisation or project affiliation.'}return}if(err)err.style.display='none';const description=String(d.get('description')||'').trim();if(description.length<40){if(err){err.style.display='block';err.textContent='Please add a little more technical context (at least 40 characters) so the enquiry can be routed usefully.'}return}const routeContext=params.get('ip')||params.get('service')||params.get('type')||'direct';const subject=encodeURIComponent(`[Website technical enquiry] ${d.get('projectType')} — ${d.get('company')}`);const body=encodeURIComponent(`Name: ${d.get('name')}\nWork email: ${email}\nCompany: ${d.get('company')}\nCountry: ${d.get('country')}\nProject type: ${d.get('projectType')}\nRequired service: ${d.get('service')}\nRoute context: ${routeContext}\nNDA requested: ${d.get('nda')?'Yes':'No'}\n\nTechnical description:\n${description}`);track('qualified_enquiry_form_submit',{page:location.pathname,project_type:d.get('projectType'),service:d.get('service'),route_context:routeContext});if(notice){notice.style.display='block';notice.textContent='Your email client will open with the technical enquiry prepared. Secure server-side routing and document upload will replace this fallback when the production intake backend is connected.'}location.href=`mailto:info@zeptologic.com?subject=${subject}&body=${body}`});

// Year
qa('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
