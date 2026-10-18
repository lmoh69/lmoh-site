/* Blog intimiste : histoires de mariés (initiales seulement, jamais de date). Contenu dans blog.json. */
(function(){
var l=document.createElement('link');l.rel='stylesheet';l.href='blog.css';document.head.appendChild(l);
var blogPage=document.querySelector('[data-page="/blog"]');if(!blogPage)return;
function T(s){return 'thumbs/'+s+'.jpg'}function F(s){return 'photos/'+s+'.jpg'}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')}
fetch('blog.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(d){
 var st=d.stories||[];if(!st.length)return;
 var intro=blogPage.querySelector('.title p');if(intro)intro.textContent='Des histoires de mariés, racontées depuis les coulisses. Et quelques conseils pour préparer la vôtre.';
 var posts=blogPage.querySelector('.posts');
 var h='<div class="stories">';
 st.forEach(function(s){h+='<a class="story-card rv" href="#/blog/'+s.slug+'"><div class="img zoom"><img src="'+T(s.cover)+'" data-full="'+F(s.cover)+'" alt="'+esc(s.initials)+'" loading="lazy" decoding="async"></div><span class="kicker">Histoire de mariés</span><h3><em>'+esc(s.initials)+'</em> '+esc(s.title)+'</h3><p>'+esc(s.teaser)+'</p></a>'});
 h+='</div><div class="chap-head rv" style="margin:clamp(4rem,8vw,6rem) auto clamp(2rem,4vw,3rem)"><span class="num">Conseils</span><h2>Préparer votre mariage</h2></div>';
 posts.insertAdjacentHTML('beforebegin',h);
 var after=document.querySelector('[data-page="/blog/seance-couple"]')||blogPage;
 st.slice().reverse().forEach(function(s){
  var b='<section class="page top-space pad story" data-page="/blog/'+s.slug+'"><article class="wrap">';
  b+='<a class="back" href="#/blog">Retour au blog</a><div class="story-head"><span class="kicker">Histoire de mariés</span><h1><em>'+esc(s.initials)+'</em><br>'+esc(s.title)+'</h1></div>';
  b+='<figure class="story-cover rv"><img src="'+F(s.cover)+'" alt="'+esc(s.initials)+'" decoding="async"></figure>';
  s.blocks.forEach(function(k){
   if(k.t==='p')b+='<p class="story-p rv">'+esc(k.text)+'</p>';
   else if(k.t==='q')b+='<blockquote class="story-q rv">'+esc(k.text)+'</blockquote>';
   else if(k.t==='img'){b+='<div class="grid story-grid n'+k.src.length+'">';k.src.forEach(function(x){b+='<figure class="rv"><div class="box rvi"><img src="'+(k.src.length>1?T(x):F(x))+'" data-full="'+F(x)+'" onerror="this.onerror=null;this.src=this.dataset.full" alt="'+esc(s.initials)+'" loading="lazy" decoding="async"></div></figure>'});b+='</div>'}
   else if(k.t==='video')b+='<figure class="story-video rv"><video controls playsinline preload="none" poster="'+k.poster+'" src="'+k.src+'"></video>'+(k.caption?'<figcaption>'+esc(k.caption)+'</figcaption>':'')+'</figure>';
  });
  b+='<div class="cta-band rv"><p class="story-end">Vous aussi, vous voulez que je raconte votre histoire ?</p><a class="btn" href="#/contact">Parlons de votre mariage</a></div></article></section>';
  after.insertAdjacentHTML('afterend',b);
 });
 window.dispatchEvent(new HashChangeEvent('hashchange'));
}).catch(function(){});
})();
