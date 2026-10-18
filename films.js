/* Pages Films et Pro (photo + vidéo), alimentées par media.json et films.json */
(function(){
var bj=document.createElement('script');bj.src='blog.js';document.body.appendChild(bj);
var dd=document.querySelector('#dd ul');if(!dd)return;
var cul=dd.querySelector('a[href="#/culinaire"]');
cul.parentNode.insertAdjacentHTML('beforebegin','<li><a href="#/pro">Pro</a></li>');
dd.insertAdjacentHTML('beforeend','<li><a href="#/films">Films</a></li>');
var anchor=document.querySelector('[data-page="/culinaire"]');
anchor.insertAdjacentHTML('beforebegin',
 '<section class="page top-space pad" data-page="/films"><div class="wrap"><div class="title rv"><span class="kicker">Portfolio</span><h1>Films</h1><p>Des teasers de mariage montés comme de courts films : l’émotion, la musique, le mouvement. À regarder avec le son.</p></div><div class="film-grid films-all" id="filmsAll"></div><div class="cta-band rv"><a class="btn" href="#/contact">Un film pour votre mariage</a></div></div></section>'+
 '<section class="page top-space pad" data-page="/pro"><div class="wrap"><div class="title rv"><span class="kicker">Portfolio</span><h1>Professionnel</h1><p>Marques, créateurs, restaurants et entreprises : des photos et des films soignés pour votre image, vos réseaux et vos campagnes.</p></div>'+
 '<div class="chap-head rv"><span class="num">Vidéo</span><h2>Films de marque</h2></div><div class="film-grid" id="proFilms"></div>'+
 '<div class="chap-head rv" style="margin-top:clamp(4rem,8vw,6rem)"><span class="num">Photo</span><h2>Images de marque</h2></div><div class="grid" id="proPhotos"></div>'+
 '<div class="cta-band rv"><a class="btn" href="#/contact">Demander un devis</a></div></div></section>');
var sel=document.getElementById('t');if(sel&&!/Pro/.test(sel.innerHTML))sel.insertAdjacentHTML('beforeend','<option>Professionnel</option><option>Film</option>');

function slug(v){return v[0].split('/').pop().replace('.mp4','')}
function card(v,lbl){
 var b=document.createElement('button');b.type='button';b.className='rv';
 b.innerHTML='<div class="poster"><img src="'+v[1]+'" alt="" loading="lazy"><span class="play"><span><svg viewBox="0 0 20 24" aria-hidden="true"><path d="M0 0l20 12L0 24z"/></svg></span></span></div><span class="lbl">'+lbl+'</span>';
 b.onclick=function(){var vm=document.querySelector('.vm');if(!vm)return;var x=vm.querySelector('video');x.src=v[0];x.poster=v[1];vm.classList.add('open');x.muted=false;var p=x.play();if(p&&p.catch)p.catch(function(){})};
 return b;
}
function fig(it){var f=document.createElement('figure');f.className='rv';f.innerHTML='<div class="box rvi"><img src="'+it[0].replace(/^photos\//,'thumbs/')+'" data-full="'+it[0]+'" onerror="this.onerror=null;this.src=this.dataset.full" width="'+it[1]+'" height="'+it[2]+'" alt="Photo professionnelle LMOH Photography" loading="lazy" decoding="async"></div>';return f}
function nice(s){return s.replace(/^(film|pro|teaser)-/,'').replace(/-/g,' ').replace(/^./,function(c){return c.toUpperCase()})}
Promise.all([
 fetch('media.json',{cache:'no-cache'}).then(function(r){return r.json()}),
 fetch('films.json',{cache:'no-cache'}).then(function(r){return r.json()}).catch(function(){return {}})
]).then(function(a){
 var m=a[0],c=a[1]||{},L=c.labels||{},hide=c.hide||[];
 var vids=(m.videos||[]).filter(function(v){return hide.indexOf(slug(v))<0});
 var isPro=function(v){var s=slug(v);return /^pro-/.test(s)||(c.proFilms||[]).indexOf(s)>-1};
 var order=c.order||[];
 vids.sort(function(x,y){var i=order.indexOf(slug(x)),j=order.indexOf(slug(y));return (i<0?999:i)-(j<0?999:j)});
 var all=document.getElementById('filmsAll'),pf=document.getElementById('proFilms');
 vids.forEach(function(v){var s=slug(v),lbl=L[s]||nice(s);(isPro(v)?pf:all).appendChild(card(v,lbl))});
 var P=m.photos||{},have={},pp=document.getElementById('proPhotos');
 (P.pro||[]).forEach(function(it){have[it[0]]=1;pp.appendChild(fig(it))});
 var extra=c.proPhotos||[],idx={};
 Object.keys(P).forEach(function(k){P[k].forEach(function(it){idx[it[0]]=it})});
 extra.forEach(function(s){var it=idx['photos/'+s+'.jpg'];if(it&&!have[it[0]])pp.appendChild(fig(it))});
 window.dispatchEvent(new HashChangeEvent('hashchange'));
});
if(/^#\/(films|pro)$/.test(location.hash))window.dispatchEvent(new HashChangeEvent('hashchange'));
})();
