const q=(s,c=document)=>c.querySelector(s),qa=(s,c=document)=>[...c.querySelectorAll(s)];
q('.menu-btn')?.addEventListener('click',()=>{q('.links').classList.toggle('open');q('.menu-btn').setAttribute('aria-expanded',q('.links').classList.contains('open'))});
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible')}),{threshold:.12});qa('.reveal').forEach(e=>io.observe(e));
qa('[data-filter]').forEach(b=>b.addEventListener('click',()=>{qa('[data-filter]').forEach(x=>x.classList.remove('active'));b.classList.add('active');const f=b.dataset.filter;qa('.product-card').forEach(c=>c.classList.toggle('hidden',f!=='all'&&c.dataset.category!==f))}));
q('#contactForm')?.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(e.target);const subject=encodeURIComponent(`[Website enquiry] ${d.get('interest')} — ${d.get('company')||d.get('name')}`);const body=encodeURIComponent(`Name: ${d.get('name')}\nCompany: ${d.get('company')}\nEmail: ${d.get('email')}\nPhone: ${d.get('phone')}\nInterest: ${d.get('interest')}\n\nMessage:\n${d.get('message')}`);location.href=`mailto:info@zeptologic.com?subject=${subject}&body=${body}`;q('.notice').style.display='block'});
q('#year')&&(q('#year').textContent=new Date().getFullYear());

// Persistent dark/light color theme
const themeButton=q('.theme-toggle');
function applyTheme(theme){
  document.documentElement.dataset.theme=theme;
  const light=theme==='light';
  if(themeButton){
    themeButton.setAttribute('aria-pressed',String(light));
    themeButton.setAttribute('aria-label',light?'Switch to dark theme':'Switch to light theme');
    themeButton.querySelector('.theme-icon').textContent=light?'☾':'☀';
    themeButton.querySelector('.theme-label').textContent=light?'Dark':'Light';
  }
  const meta=q('meta[name="theme-color"]');
  if(meta) meta.content=light?'#f4f7fb':'#05070b';
}
applyTheme(document.documentElement.dataset.theme||'dark');
themeButton?.addEventListener('click',()=>{
  const next=document.documentElement.dataset.theme==='light'?'dark':'light';
  localStorage.setItem('zl-theme',next);
  applyTheme(next);
});


// Compact language selector with Google Website Translator fallback.
const languageSelect=q('#languageSelect');
const languageNames={en:'English',ta:'Tamil',hi:'Hindi',ja:'Japanese',ko:'Korean','zh-CN':'Chinese'};
function setLanguageUI(code){
  if(languageSelect) languageSelect.value=code;
  document.documentElement.lang=code==='zh-CN'?'zh-CN':code;
}
function applyWebsiteLanguage(code){
  localStorage.setItem('zl-language',code);
  setLanguageUI(code);
  if(code==='en'){
    document.cookie='googtrans=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;';
    document.cookie='googtrans=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;domain='+location.hostname+';';
    location.reload();
    return;
  }
  document.cookie=`googtrans=/en/${code};path=/`;
  document.cookie=`googtrans=/en/${code};path=/;domain=${location.hostname}`;
  const combo=document.querySelector('.goog-te-combo');
  if(combo){combo.value=code;combo.dispatchEvent(new Event('change'));}
  else location.reload();
}
languageSelect?.addEventListener('change',e=>applyWebsiteLanguage(e.target.value));
setLanguageUI(localStorage.getItem('zl-language')||'en');
window.googleTranslateElementInit=function(){
  if(window.google?.translate){
    new google.translate.TranslateElement({pageLanguage:'en',includedLanguages:'en,ta,hi,ja,ko,zh-CN',autoDisplay:false},'google_translate_element');
  }
};
if(!document.getElementById('google_translate_element')){
  const hidden=document.createElement('div');hidden.id='google_translate_element';hidden.hidden=true;document.body.appendChild(hidden);
  const s=document.createElement('script');s.src='https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';s.async=true;document.body.appendChild(s);
}

// Pause marquees for keyboard users and resume when focus leaves.
qa('.page-marquee,.ecosystem-marquee').forEach(m=>{
  m.addEventListener('focusin',()=>m.querySelector('.marquee-track').style.animationPlayState='paused');
  m.addEventListener('focusout',()=>m.querySelector('.marquee-track').style.animationPlayState='running');
});
