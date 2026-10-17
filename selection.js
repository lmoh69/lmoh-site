/* Sélection de la page d'accueil : 5 ambiances, chacune avec des photos aux couleurs coordonnées. */
(function(){
var THEMES=[
 {name:'Lumière dorée',text:'Golden hour, peaux dorées et verts profonds.',href:'#/couple',img:['portrait/p1077179','portrait/p1287706','couple/p1114280','mariage/m10','couple/p1350242']},
 {name:'Noir & blanc',text:'L’émotion à l’état pur, sans artifice.',href:'#/noir-et-blanc',img:['mariage/m24','nb/p1066154','mariage2/n11','nb/p1347947','nb/p1632337']},
 {name:'Couple',text:'Des portraits à deux, complices et élégants.',href:'#/couple',img:['couple/p1020416','couple/p1057396','couple/p1032947','couple/p1350529','mariage2/n04']},
 {name:'Détails',text:'Dentelles, alliances et fleurs : le soin du détail.',href:'#/mariage',img:['details/p1091438','details/p1010509','mariage2/n27','details/p1019788','couple/p1103825']},
 {name:'Soirée',text:'Quand les lumières baissent et que la fête commence.',href:'#/mariage',img:['soiree/p1352177','soiree/p1352128','soiree/p1352238','soiree/p1077286','soiree/p1352181']}
];
var DUR=9000,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var l=document.createElement('link');l.rel='stylesheet';l.href='selection.css';document.head.appendChild(l);
var intro=document.getElementById('intro');if(!intro)return;
var sec=document.createElement('section');sec.className='wrap sel';sec.id='selection';sec.setAttribute('aria-label','Sélection de photos');
var h='<div class="title"><span class="kicker">La sélection</span><h2>Mes plus belles images</h2></div><div class="sel-tabs" role="tablist">';
THEMES.forEach(function(t,i){h+='<button role="tab" aria-selected="false" data-i="'+i+'">'+t.name+'<i><b></b></i></button>'});
h+='</div><div class="sel-stage">';
THEMES.forEach(function(t,i){h+='<div class="sel-set" data-i="'+i+'">';t.img.forEach(function(s,k){h+='<a href="'+t.href+'" aria-label="'+t.name+'"><img data-src="photos/'+s+'.jpg" alt="'+t.name+'" decoding="async"></a>'});h+='</div>'});
h+='</div><div class="sel-cap"><p></p><a href="#/mariage">Voir la galerie</a></div>';
sec.innerHTML=h;intro.parentNode.insertBefore(sec,intro.nextSibling);
sec.style.setProperty('--dur',DUR/1000+'s');
var tabs=[].slice.call(sec.querySelectorAll('.sel-tabs button')),sets=[].slice.call(sec.querySelectorAll('.sel-set'));
var cap=sec.querySelector('.sel-cap p'),capA=sec.querySelector('.sel-cap a');
var now=new Date(),cur=(now.getFullYear()*12+now.getMonth())%THEMES.length,timer=null,visible=false;
function load(i){sets[i].querySelectorAll('img').forEach(function(im){if(!im.getAttribute('src'))im.src=im.dataset.src})}
function go(i){
 cur=(i+THEMES.length)%THEMES.length;load(cur);load((cur+1)%THEMES.length);
 sets.forEach(function(s,k){s.classList.toggle('on',k===cur)});
 tabs.forEach(function(b,k){b.setAttribute('aria-selected',k===cur?'true':'false');var bar=b.querySelector('b');bar.style.animation='none';bar.offsetWidth;bar.style.animation=''});
 cap.textContent=THEMES[cur].text;capA.href=THEMES[cur].href;
 schedule();
}
function schedule(){clearTimeout(timer);if(!reduce&&visible&&!sec.classList.contains('paused'))timer=setTimeout(function(){go(cur+1)},DUR)}
tabs.forEach(function(b){b.addEventListener('click',function(){go(+b.dataset.i)})});
sec.querySelector('.sel-stage').addEventListener('mouseenter',function(){sec.classList.add('paused');clearTimeout(timer)});
sec.querySelector('.sel-stage').addEventListener('mouseleave',function(){sec.classList.remove('paused');go(cur)});
new IntersectionObserver(function(es){visible=es[0].isIntersecting;if(visible){load(cur);schedule()}else clearTimeout(timer)},{threshold:.25}).observe(sec);
go(cur);
})();
