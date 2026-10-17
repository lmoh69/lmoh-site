/* Teaser : mettre ici le chemin de la vidéo (ex. "video/teaser.mp4") une fois déposée dans le dépôt. */
var TEASER="";
(function(){
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var pages=[].slice.call(document.querySelectorAll('.page'));
var links=[].slice.call(document.querySelectorAll('nav.main a'));
var hdr=document.getElementById('hdr'),nav=document.getElementById('nav'),burger=document.getElementById('burger'),dd=document.getElementById('dd'),ddBtn=document.getElementById('ddBtn');
var folio=['/mariage','/couple','/noir-et-blanc','/portrait','/culinaire'];
var current=null;
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.05});
function watch(p){p.querySelectorAll('.rv,.rvi').forEach(function(el){if(reduce){el.classList.add('in')}else if(!el.classList.contains('in')){io.observe(el)}})}
/* Bandeau qui défile */
var track=document.getElementById('track');
var strip=['photos/mariage/m09.jpg','photos/couple/p1032947.jpg','photos/details/p1091438.jpg','photos/couple/p1505330.jpg','photos/nb/p1043230.jpg','photos/mariage/m32.jpg','photos/couple/p1288184.jpg','photos/portrait/p1077179.jpg','photos/soiree/p1352238.jpg','photos/mariage/m11.jpg'];
strip.concat(strip).forEach(function(s){var i=document.createElement('img');i.src=s;i.alt='';i.loading='lazy';i.decoding='async';track.appendChild(i)});
/* Hero : teaser vidéo ou diaporama */
var hero=document.getElementById('hero'),slides=[].slice.call(document.querySelectorAll('#slides .slide')),si=0;
function prep(n){var im=slides[n].querySelector('img');if(im.dataset.src&&!im.getAttribute('src'))im.src=im.dataset.src}
if(TEASER){
document.getElementById('slides').remove();
var v=document.createElement('video');v.src=TEASER;v.autoplay=true;v.muted=true;v.loop=true;v.playsInline=true;v.setAttribute('playsinline','');v.poster='photos/couple/p1020416.jpg';
hero.insertBefore(v,hero.firstChild);
var s=document.getElementById('sound');s.style.display='block';
s.addEventListener('click',function(){v.muted=!v.muted;s.textContent=v.muted?'Activer le son':'Couper le son'});
}else{
slides[0].classList.add('on');prep(1);
if(!reduce)setInterval(function(){slides[si].classList.remove('on');si=(si+1)%slides.length;prep(si);slides[si].classList.add('on');prep((si+1)%slides.length)},6500);
}
document.getElementById('cue').addEventListener('click',function(e){e.preventDefault();document.getElementById('intro').scrollIntoView({behavior:reduce?'auto':'smooth'})});
document.addEventListener('click',function(e){var a=e.target.closest('[data-to]');if(!a)return;e.preventDefault();var t=document.getElementById(a.dataset.to);if(t)t.scrollIntoView({behavior:reduce?'auto':'smooth'})});
function onScroll(){
var y=window.scrollY;
hdr.classList.toggle('compact',y>40);
document.body.classList.toggle('onhero',current==='/'&&y<hero.offsetHeight-90);
}
window.addEventListener('scroll',onScroll,{passive:true});
function route(){
var r=(location.hash.replace(/^#/,'')||'/');
var hit=pages.filter(function(p){return p.dataset.page===r})[0]||pages[0];
current=hit.dataset.page;
pages.forEach(function(p){p.classList.toggle('show',p===hit)});
watch(hit);
links.forEach(function(a){var h=a.getAttribute('href');a.classList.toggle('on',h==='#'+current||(h==='#/blog'&&current.indexOf('/blog')===0))});
ddBtn.classList.toggle('on',folio.indexOf(current)>-1);
nav.classList.remove('open');burger.setAttribute('aria-expanded','false');dd.classList.remove('open');ddBtn.setAttribute('aria-expanded','false');
window.scrollTo(0,0);onScroll();
var h1=hit.querySelector('h1');document.title=(h1&&current!=='/'?h1.textContent+' | ':'')+'LMOH Photography, photographe de mariage à Lyon';
}
window.addEventListener('hashchange',route);route();
burger.addEventListener('click',function(){var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o)});
ddBtn.addEventListener('click',function(){var o=dd.classList.toggle('open');ddBtn.setAttribute('aria-expanded',o)});
document.addEventListener('click',function(e){if(!dd.contains(e.target)){dd.classList.remove('open');ddBtn.setAttribute('aria-expanded','false')}});
/* Visionneuse plein écran */
var lb=document.getElementById('lb'),lbImg=document.getElementById('lbImg'),list=[],idx=0;
function show(i){idx=(i+list.length)%list.length;lbImg.src=list[idx].src;lbImg.alt=list[idx].alt}
document.addEventListener('click',function(e){
var f=e.target.closest('.grid figure');if(!f)return;var im=f.querySelector('img');if(!im)return;
list=[].slice.call(f.closest('.page').querySelectorAll('.grid img'));show(list.indexOf(im));lb.classList.add('open');
});
function close(){lb.classList.remove('open')}
document.getElementById('lbX').addEventListener('click',close);
document.getElementById('lbP').addEventListener('click',function(){show(idx-1)});
document.getElementById('lbN').addEventListener('click',function(){show(idx+1)});
lb.addEventListener('click',function(e){if(e.target===lb)close()});
document.addEventListener('keydown',function(e){if(!lb.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(idx-1);if(e.key==='ArrowRight')show(idx+1)});
var tx=null;lb.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
lb.addEventListener('touchend',function(e){if(tx===null)return;var dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)show(idx+(dx<0?1:-1));tx=null});
document.getElementById('contactForm').addEventListener('submit',function(ev){
ev.preventDefault();var g=function(i){return document.getElementById(i).value.trim()};var m=document.getElementById('msg');
if(!g('n')||!/^\S+@\S+\.\S+$/.test(g('e'))){m.textContent='Indiquez votre nom et un e-mail valide.';return}
var body='Nom : '+g('n')+'\nE-mail : '+g('e')+'\nProjet : '+g('t')+'\nDate : '+(g('d')||'à définir')+'\nLieu : '+(g('l')||'à définir')+'\nBudget : '+g('b')+'\n\n'+g('m');
location.href='mailto:contact@lmohphotography.com?subject='+encodeURIComponent('Demande '+g('t')+' – '+g('n'))+'&body='+encodeURIComponent(body);
m.textContent='Votre messagerie s\u2019ouvre avec la demande pré-remplie.';
});
})();
