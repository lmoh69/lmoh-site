/* Site LMOH v2 : les galeries, le teaser d'accueil et la mise en page se renouvellent chaque mois.
   Les nouvelles photos arrivent du Drive via le robot (media.json). */
(function(){
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var now=new Date(),SEED=now.getFullYear()*12+now.getMonth();
function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function shuffle(arr,salt){var r=rng(SEED*97+(salt||0)),a=arr.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(r()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}
var CFG={
 labels:{'teaser-court':'Le grand jour','teaser-camille':'Château et bougies','teaser-1mn':'Au bord de l’eau','teaser-reseau':'Élégance','teaser-black':'Les détails'},
 heroExclude:['teaser-black'],
 proFilms:['teaser-black'],
 mariage2:['n01','n02','n03','n04','n05','n11','n12','n13','n14','n15','n18','n19','n20','n21','n22','n23','n24','n25','n26','n27'],
 pages:{couple:'/couple',nb:'/noir-et-blanc',portrait:'/portrait',culinaire:'/culinaire',grossesse:'/naissance'}
};
document.head.insertAdjacentHTML('beforeend','<link rel="stylesheet" href="v2.css">');
document.body.classList.add('lay-'+['a','b','c'][SEED%3]);
var sj=document.createElement('script');sj.src='selection.js';document.body.appendChild(sj);
var fj=document.createElement('script');fj.src='films.js';document.body.appendChild(fj);

/* --- Structure ajoutée : onglet Naissance, section Films, mariage au bord du lac --- */
var ddList=document.querySelector('#dd ul');
ddList.insertAdjacentHTML('beforeend','<li><a href="#/naissance">Naissance</a></li>');
var cul=document.querySelector('[data-page="/culinaire"]');
cul.insertAdjacentHTML('beforebegin','<section class="page top-space pad" data-page="/naissance"><div class="wrap"><div class="title rv"><span class="kicker">Portfolio</span><h1>Naissance</h1><p>Les premiers jours, la douceur d’une peau neuve, les petites mains : des images tendres et lumineuses à garder pour toujours.</p></div><div class="grid" data-cat="grossesse"></div><div class="cta-band rv"><a class="btn" href="#/contact">Réserver une séance</a></div></div></section>');
var quote=document.querySelector('[data-page="/"] .quote');
quote.insertAdjacentHTML('beforebegin','<div class="wrap films" id="films"><div class="title rv"><span class="kicker">Films</span><h2>Vos images, en mouvement</h2><p>Quelques teasers de mariages, à regarder avec le son.</p></div><div class="film-grid" id="filmGrid"></div></div>');
var mcta=document.querySelector('[data-page="/mariage"] .cta-band');
mcta.insertAdjacentHTML('beforebegin','<section class="chap" id="c6"><div class="chap-head rv"><span class="num">Et aussi</span><h2>Un mariage au bord du lac</h2><p>Une autre histoire, entre mairie, palace et balade en bateau.</p></div><div class="grid" id="lac"></div></section><section class="chap" id="c7" hidden><div class="chap-head rv"><span class="num">Nouveau</span><h2>Derniers mariages</h2><p>Les images les plus récentes, ajoutées ce mois-ci.</p></div><div class="grid" id="newMariage"></div></section>');
var cn=document.querySelector('.chap-nav');if(cn)cn.insertAdjacentHTML('beforeend','<a href="#/mariage" data-to="c6">Au bord du lac</a>');

var pages=[].slice.call(document.querySelectorAll('.page'));
var links=[].slice.call(document.querySelectorAll('nav.main a'));
var hdr=document.getElementById('hdr'),nav=document.getElementById('nav'),burger=document.getElementById('burger'),dd=document.getElementById('dd'),ddBtn=document.getElementById('ddBtn');
var folio=['/mariage','/couple','/noir-et-blanc','/portrait','/naissance','/pro','/culinaire','/films'];
var current=null;
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.05});
function watch(p){p.querySelectorAll('.rv,.rvi').forEach(function(el){if(reduce){el.classList.add('in')}else if(!el.classList.contains('in')){io.observe(el)}})}
function fig(src,w,h,alt){var f=document.createElement('figure');f.className='rv';f.innerHTML='<div class="box rvi"><img src="'+src+'" width="'+w+'" height="'+h+'" alt="'+(alt||'Photo LMOH Photography')+'" loading="lazy" decoding="async"></div>';return f}

/* --- Bandeau qui défile --- */
var track=document.getElementById('track');
/* Bandeau : des séquences de photos cohérentes (même ambiance, même preset couleur) */
var STRIP=[
 ['Blanc & lumière',['mariage/m05','mariage/m07','mariage/m09','portrait/p1117317','portrait/p1066260','couple/p1103825','mariage2/n27']],
 ['Vert & nature',['couple/p1057396','couple/p1350242','details/p1010509','mariage/m12','mariage/m13','mariage/m15','mariage2/n04']],
 ['Lumière dorée',['couple/p1077148','portrait/p1077179','portrait/p1287706','couple/p1350698','couple/p1114280','mariage/m10','mariage/m31']],
 ['Détails intimistes',['couple/p1352972','details/p1091438','details/p1048523','details/p1048334','details/p1005105']],
 ['Soirée',['soiree/p1352128','soiree/p1352177','soiree/p1352181','soiree/p1352186','soiree/p1352238','soiree/p1077286']],
 ['Noir & blanc',['nb/p1066154','mariage2/n11','nb/p1347947','mariage/m24','nb/p1632337','nb/p1505331','nb/p1020416']]
];
function buildStrip(){
 var start=SEED%STRIP.length,seq=[];
 for(var k=0;k<STRIP.length;k++){var g=STRIP[(start+k)%STRIP.length];seq.push({label:g[0]});shuffle(g[1],31+k).forEach(function(s){seq.push({src:'photos/'+s+'.jpg'})})}
 track.innerHTML='';
 seq.concat(seq).forEach(function(it,n){
  if(it.label){var d=document.createElement('div');d.className='strip-label';d.innerHTML='<span>'+it.label+'</span>';track.appendChild(d)}
  else{var i=document.createElement('img');i.src=it.src;i.alt='';if(n>12)i.loading='lazy';i.decoding='async';track.appendChild(i)}
 });
 track.style.animationDuration=(seq.length*5)+'s';
}
buildStrip();

/* --- Hero : diaporama, remplacé par le teaser du mois --- */
var hero=document.getElementById('hero'),slides=[].slice.call(document.querySelectorAll('#slides .slide')),si=0,timer=null;
function prep(n){var im=slides[n].querySelector('img');if(im.dataset.src&&!im.getAttribute('src'))im.src=im.dataset.src}
slides[0].classList.add('on');prep(1);
if(!reduce)timer=setInterval(function(){slides[si].classList.remove('on');si=(si+1)%slides.length;prep(si);slides[si].classList.add('on');prep((si+1)%slides.length)},6500);
function heroVideo(src,poster){
 var c=navigator.connection||{};if(reduce||c.saveData||/2g/.test(c.effectiveType||''))return;
 var v=document.createElement('video');v.muted=true;v.loop=true;v.autoplay=true;v.playsInline=true;v.setAttribute('playsinline','');v.setAttribute('muted','');v.preload='auto';v.poster=poster;v.src=src;v.style.opacity='0';v.style.transition='opacity 1.6s ease';
 v.addEventListener('playing',function(){v.style.opacity='1';if(timer){clearInterval(timer);timer=null}var s=document.getElementById('sound');s.style.display='block'},{once:true});
 hero.insertBefore(v,hero.querySelector('.center'));
 var p=v.play();if(p&&p.catch)p.catch(function(){});
 var s=document.getElementById('sound');s.onclick=function(){v.muted=!v.muted;s.textContent=v.muted?'Activer le son':'Couper le son'};
}
document.getElementById('cue').addEventListener('click',function(e){e.preventDefault();document.getElementById('intro').scrollIntoView({behavior:reduce?'auto':'smooth'})});
document.addEventListener('click',function(e){var a=e.target.closest('[data-to]');if(!a)return;e.preventDefault();var t=document.getElementById(a.dataset.to);if(t)t.scrollIntoView({behavior:reduce?'auto':'smooth'})});

/* --- Films --- */
var vm=document.createElement('div');vm.className='vm';vm.innerHTML='<video controls playsinline preload="none"></video><button type="button">Fermer</button>';document.body.appendChild(vm);
var vmv=vm.querySelector('video');
function closeVm(){vm.classList.remove('open');vmv.pause()}
vm.querySelector('button').onclick=closeVm;vm.addEventListener('click',function(e){if(e.target===vm)closeVm()});
function label(src){var k=src.split('/').pop().replace('.mp4','');return CFG.labels[k]||k.replace(/^teaser-/,'').replace(/-/g,' ').replace(/^./,function(c){return c.toUpperCase()})}
function isPro(v){var k=v[0].split('/').pop().replace('.mp4','');return /^pro-/.test(k)||CFG.proFilms.indexOf(k)>-1}
function fillFilms(videos){
 var g=document.getElementById('filmGrid');g.innerHTML='';
 videos=videos.filter(function(v){return !isPro(v)});
 shuffle(videos,3).slice(0,6).forEach(function(v){
  var b=document.createElement('button');b.type='button';b.className='rv';
  b.innerHTML='<div class="poster"><img src="'+v[1]+'" alt="" loading="lazy"><span class="play"><span><svg viewBox="0 0 20 24" aria-hidden="true"><path d="M0 0l20 12L0 24z"/></svg></span></span></div><span class="lbl">'+label(v[0])+'</span>';
  b.onclick=function(){vmv.src=v[0];vmv.poster=v[1];vm.classList.add('open');vmv.muted=false;var p=vmv.play();if(p&&p.catch)p.catch(function(){})};
  g.appendChild(b);
 });
 if(!videos.length)document.getElementById('films').hidden=true;
 if(!document.getElementById('allFilms'))g.insertAdjacentHTML('afterend','<div class="cta-band" id="allFilms"><a class="btn line" href="#/films">Voir tous les films</a></div>');
}

/* --- Galeries : ordre renouvelé chaque mois + nouvelles photos du Drive --- */
function present(){var s={};document.querySelectorAll('.page img').forEach(function(i){var a=i.getAttribute('src')||i.dataset.src;if(a)s[a]=1});return s}
function refreshGrid(grid,items,salt){
 var have=present();
 (items||[]).forEach(function(it){if(!have[it[0]])grid.appendChild(fig(it[0],it[1],it[2]))});
 var figs=[].slice.call(grid.children);shuffle(figs,salt).forEach(function(f){grid.appendChild(f)});
}
function applyMedia(m){
 var P=m.photos||{};
 Object.keys(CFG.pages).forEach(function(cat,k){
  var page=document.querySelector('[data-page="'+CFG.pages[cat]+'"]');if(!page)return;
  var grid=page.querySelector('.grid');if(grid)refreshGrid(grid,P[cat],11+k);
 });
 var lac=document.getElementById('lac');
 (P.mariage2||[]).forEach(function(it){var n=it[0].split('/').pop().replace('.jpg','');if(CFG.mariage2.indexOf(n)>-1)lac.appendChild(fig(it[0],it[1],it[2],'Mariage au bord du lac'))});
 var fresh=(P.mariage||[]).filter(function(it){return !/\/m\d+b?\.jpg$/.test(it[0])});
 if(fresh.length){document.getElementById('c7').hidden=false;refreshGrid(document.getElementById('newMariage'),fresh,5)}
 var c2=document.querySelector('#c2 .grid'),c5=document.querySelector('#c5 .grid'),have=present();
 (P.details||[]).forEach(function(it){if(!have[it[0]]&&c2.children.length<9)c2.appendChild(fig(it[0],it[1],it[2],'Détail de mariage'))});
 (P.soiree||[]).forEach(function(it){if(!have[it[0]]&&c5.children.length<9)c5.appendChild(fig(it[0],it[1],it[2],'Soirée de mariage'))});
 /* Couvertures de l'accueil et bandeau du mois */
 var covers={'/mariage':P.mariage,'/couple':P.couple,'/noir-et-blanc':P.nb,'/portrait':P.portrait};
 document.querySelectorAll('.cats a').forEach(function(a,k){var pool=(covers[a.getAttribute('href').slice(1)]||[]).filter(function(it){return it[2]>=it[1]*1.2||k===0});if(pool.length){var pick=shuffle(pool,21+k)[0];a.querySelector('img').src=pick[0]}});
 var vids=m.videos||[];fillFilms(vids);
 var heroes=vids.filter(function(v){return !isPro(v)&&CFG.heroExclude.indexOf(v[0].split('/').pop().replace('.mp4',''))<0});
 if(heroes.length){var h=heroes[SEED%heroes.length];heroVideo(h[0],h[1])}
 if(current)watch(document.querySelector('.page.show'));
}
Promise.all([fetch('media.json',{cache:'no-cache'}).then(function(r){return r.json()}),fetch('films.json',{cache:'no-cache'}).then(function(r){return r.json()}).catch(function(){return {}})]).then(function(a){var c=a[1]||{};Object.keys(c.labels||{}).forEach(function(k){CFG.labels[k]=c.labels[k]});CFG.proFilms=CFG.proFilms.concat(c.proFilms||[]);CFG.heroExclude=CFG.heroExclude.concat(c.hide||[],c.heroExclude||[]);applyMedia(a[0])}).catch(function(){});

/* --- Navigation --- */
function onScroll(){var y=window.scrollY;hdr.classList.toggle('compact',y>40);document.body.classList.toggle('onhero',current==='/'&&y<hero.offsetHeight-90)}
window.addEventListener('scroll',onScroll,{passive:true});
function route(){
 var r=(location.hash.replace(/^#/,'')||'/');
 pages=[].slice.call(document.querySelectorAll('.page'));
 var hit=pages.filter(function(p){return p.dataset.page===r})[0]||pages[0];
 current=hit.dataset.page;
 pages.forEach(function(p){p.classList.toggle('show',p===hit)});
 watch(hit);
 links=[].slice.call(document.querySelectorAll('nav.main a'));
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

/* --- Visionneuse photo --- */
var lb=document.getElementById('lb'),lbImg=document.getElementById('lbImg'),list=[],idx=0;
function show(i){idx=(i+list.length)%list.length;lbImg.src=list[idx].src;lbImg.alt=list[idx].alt}
document.addEventListener('click',function(e){var f=e.target.closest('.grid figure');if(!f)return;var im=f.querySelector('img');if(!im)return;list=[].slice.call(f.closest('.page').querySelectorAll('.grid img'));show(list.indexOf(im));lb.classList.add('open')});
function close(){lb.classList.remove('open')}
document.getElementById('lbX').addEventListener('click',close);
document.getElementById('lbP').addEventListener('click',function(){show(idx-1)});
document.getElementById('lbN').addEventListener('click',function(){show(idx+1)});
lb.addEventListener('click',function(e){if(e.target===lb)close()});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){close();closeVm()}if(!lb.classList.contains('open'))return;if(e.key==='ArrowLeft')show(idx-1);if(e.key==='ArrowRight')show(idx+1)});
var tx=null;lb.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
lb.addEventListener('touchend',function(e){if(tx===null)return;var dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)show(idx+(dx<0?1:-1));tx=null});

/* --- Contact --- */
document.getElementById('contactForm').addEventListener('submit',function(ev){
 ev.preventDefault();var g=function(i){return document.getElementById(i).value.trim()};var m=document.getElementById('msg');
 if(!g('n')||!/^\S+@\S+\.\S+$/.test(g('e'))){m.textContent='Indiquez votre nom et un e-mail valide.';return}
 var body='Nom : '+g('n')+'\nE-mail : '+g('e')+'\nProjet : '+g('t')+'\nDate : '+(g('d')||'à définir')+'\nLieu : '+(g('l')||'à définir')+'\nBudget : '+g('b')+'\n\n'+g('m');
 location.href='mailto:contact@lmohphotography.com?subject='+encodeURIComponent('Demande '+g('t')+' – '+g('n'))+'&body='+encodeURIComponent(body);
 m.textContent='Votre messagerie s\u2019ouvre avec la demande pré-remplie.';
});
})();
