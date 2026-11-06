/* Nouvelles galeries : 3 mariages (page Mariage), Dans le monde, Famille, événements d'entreprise (page Pro).
   Les photos viennent de media.json (catégories cannes, chateau, orthodoxe, monde, famille, seminaire). */
(function(){
var CH=[
 {cat:'cannes',page:'/mariage',num:'Côte d’Azur',title:'Un mariage à Cannes',text:'Robes de soie, chapeau de paille et vue sur la mer : une journée en plein soleil.',alt:'Mariage à Cannes'},
 {cat:'chateau',page:'/mariage',num:'Au château',title:'Un mariage au château',text:'Des préparatifs feutrés, un cortège en vert sauge et la lumière douce du parc.',alt:'Mariage au château'},
 {cat:'orthodoxe',page:'/mariage',num:'Cérémonie',title:'Un mariage orthodoxe',text:'Couronnes, cierges et chants, puis un parc où se promènent les paons.',alt:'Mariage orthodoxe'}
];
function head(c){return '<div class="chap-head rv" style="margin-top:clamp(4rem,8vw,6rem)"><span class="num">'+c.num+'</span><h2>'+c.title+'</h2><p>'+c.text+'</p></div>'}
function addChapters(){
 CH.forEach(function(c){
  var page=document.querySelector('[data-page="'+c.page+'"]');if(!page)return;
  var html='<section class="chap" data-gcat="'+c.cat+'" hidden>'+head(c)+'<div class="grid"></div></section>';
  var cta=page.querySelector('.cta-band');
  if(cta&&c.page==='/mariage')cta.insertAdjacentHTML('beforebegin',html);
  else (page.querySelector('.wrap')||page).insertAdjacentHTML('beforeend',html);
 });
 var cul=document.querySelector('[data-page="/culinaire"]');
 var pages='<section class="page top-space pad" data-page="/famille"><div class="wrap"><div class="title rv"><span class="kicker">Portfolio</span><h1>Famille</h1><p>Une maman et sa fille, un téléphérique, le bord du lac : des séances simples et vraies, pour garder les liens qui comptent.</p></div><section class="chap" data-gcat="famille"><div class="grid"></div></section><div class="cta-band rv"><a class="btn" href="#/contact">Parlons de votre séance</a></div></div></section>'+
 '<section class="page top-space pad" data-page="/monde"><div class="wrap"><div class="title rv"><span class="kicker">Portfolio</span><h1>Dans le monde</h1><p>Mariages, demandes en mariage et séances à l’étranger : je voyage avec vous, là où votre histoire se passe.</p></div>'+
 '<section class="chap" data-gcat="monde"><div class="chap-head rv"><span class="num">Émirats</span><h2>Une demande en mariage à Dubaï</h2><p>Un tipi sur la plage, des lettres lumineuses et la ville qui brille au loin.</p></div><div class="g-film" id="gFilm" hidden></div><div class="grid"></div></section>'+
 '<div class="cta-band rv"><a class="btn" href="#/contact">Parlons de votre projet</a></div></div></section>';
 (cul||document.querySelector('main')).insertAdjacentHTML(cul?'beforebegin':'beforeend',pages);
 var dd=document.querySelector('#dd ul');
 if(dd){dd.insertAdjacentHTML('beforeend','<li><a href="#/famille">Famille</a></li><li><a href="#/monde">Dans le monde</a></li>')}
}
function figure(it,alt){
 if(typeof fig==='function')return fig(it[0],it[1],it[2],alt);
 var f=document.createElement('figure');f.innerHTML='<div class="box"><img src="'+it[0].replace(/^photos\//,'thumbs/')+'" data-full="'+it[0]+'" width="'+it[1]+'" height="'+it[2]+'" alt="'+alt+'" loading="lazy" decoding="async"></div>';return f;
}
var ALT={cannes:'Mariage à Cannes',chateau:'Mariage au château',orthodoxe:'Mariage orthodoxe',seminaire:'Soirée d’entreprise',famille:'Séance famille',monde:'Demande en mariage à Dubaï'};
function fill(m){
 var P=m.photos||{};
 document.querySelectorAll('[data-gcat]').forEach(function(s){
  var cat=s.getAttribute('data-gcat'),items=P[cat]||[],grid=s.querySelector('.grid');
  if(!items.length||!grid||grid.children.length)return;
  items.forEach(function(it){grid.appendChild(figure(it,ALT[cat]||'Photo LMOH Photography'))});
  s.hidden=false;
 });
 var v=(m.videos||[]).filter(function(x){return /monde-/.test(x[0])})[0],gf=document.getElementById('gFilm');
 if(v&&gf){gf.innerHTML='<video controls playsinline preload="none" poster="'+v[1]+'" src="'+v[0]+'"></video>';gf.hidden=false}
 var sv=(m.videos||[]).filter(function(x){return /pro-seminaire/.test(x[0])})[0],gs=document.getElementById('gSem');
 if(sv&&gs&&!gs.innerHTML){gs.innerHTML='<video controls playsinline preload="none" poster="'+sv[1]+'" src="'+sv[0]+'"></video>';gs.hidden=false}
}
/* Page Pro renommée « Entreprise » : événements d'abord, puis films et images de marque */
var MEDIA=null;
function proSetup(n){
 var page=document.querySelector('[data-page="/pro"]'),link=document.querySelector('#dd a[href="#/pro"]');
 if(!page||!link){if((n||0)<60)setTimeout(function(){proSetup((n||0)+1)},100);return}
 link.textContent='Entreprise';
 var t=page.querySelector('.title');
 if(t){var h=t.querySelector('h1');if(h)h.textContent='Entreprise';var p=t.querySelector('p');if(p)p.textContent='Séminaires, soirées d’entreprise, salons, team building, films de marque et photos produit : des images professionnelles pour votre communication, réalisées avec discrétion à Lyon et partout en France.'}
 if(!page.querySelector('[data-gcat="seminaire"]')){
  var html='<section class="chap" data-gcat="seminaire" hidden><div class="chap-head rv"><span class="num">Événement</span><h2>Séminaires et soirées d’entreprise</h2><p>L’énergie de vos équipes, les échanges, la fête : en photo et en vidéo.</p></div><div class="g-film" id="gSem" hidden></div><div class="grid"></div>'+
  '<p class="g-read">À lire : <a href="journal/photographe-seminaire-lyon-checklist/">la checklist de l’organisateur de séminaire</a> · <a href="journal/photographe-evenementiel-entreprise-lyon/">photographe vidéaste événementiel à Lyon</a></p></section>';
  if(t)t.insertAdjacentHTML('afterend',html);else (page.querySelector('.wrap')||page).insertAdjacentHTML('afterbegin',html);
 }
 if(MEDIA)fill(MEDIA);
 if(location.hash==='#/pro')window.dispatchEvent(new HashChangeEvent('hashchange'));
}
window.addEventListener('hashchange',function(){if(location.hash==='#/entreprise')location.replace('#/pro')});
if(location.hash==='#/entreprise')location.replace('#/pro');
addChapters();
proSetup(0);
fetch('media.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(m){
 MEDIA=m;fill(m);
 var r=location.hash.replace(/^#/,'');
 if(['/famille','/monde','/mariage','/pro'].indexOf(r)>-1)window.dispatchEvent(new HashChangeEvent('hashchange'));
}).catch(function(){});
var st=document.createElement('style');st.textContent='.g-read{margin:1.6rem 0 0;font-size:.95rem;color:var(--muted)}.g-read a{color:inherit}.g-film{margin:0 0 2rem}.g-film video{width:100%;max-height:78vh;background:#000;display:block}';document.head.appendChild(st);
})();
