/* Formulaires : Recevoir des offres, fiche mariage (lien privé), confidentialité.
   Les envois arrivent dans le Google Sheet « Fichier clients LMOH » via Make. */
(function(){
var HOOK='https://hook.eu1.make.com/6nnxb98n0ytnw2abjia5s9o5bq1ugxd7';
var css=document.createElement('link');css.rel='stylesheet';css.href='forms.css';document.head.appendChild(css);
function ok(e){return /^\S+@\S+\.\S+$/.test(e)}
function send(data){return fetch(HOOK,{method:'POST',mode:'no-cors',body:new URLSearchParams(data)})}
function val(f,n){var el=f.elements[n];return el?String(el.value||'').trim():''}
function checks(f,n){return [].slice.call(f.querySelectorAll('input[name="'+n+'"]:checked')).map(function(i){return i.value}).join(', ')}
var PRIV='<a href="#/confidentialite">Confidentialité</a>';
var PRESTA=[['lieu','Lieu de réception','Nom du contact sur place'],['planner','Wedding planner, organisation','Nom'],['traiteur','Traiteur','Nom'],['fleuriste','Fleuriste','Nom'],['deco','Décorateur, scénographie','Nom'],['patissier','Pâtissier, pièce montée','Nom'],['dj','DJ, musiciens, animation','Nom'],['coiffure','Coiffure','Nom'],['maquillage','Maquillage','Nom'],['robe','Robe, costume (créateur ou boutique)','Nom'],['negafa','Négafa','Nom'],['autre','Autre prestataire','Nom et métier']];
function insta(v){v=String(v||'').trim();if(!v)return '';v=v.replace(/^https?:\/\/(www\.)?instagram\.com\//i,'').replace(/[\/?#].*/,'').replace(/^@+/,'').replace(/\s+/g,'');return v?'@'+v:''}
function prestas(f){return PRESTA.map(function(p){return {type:p[1],nom:val(f,'p_'+p[0]+'_nom'),tel:val(f,'p_'+p[0]+'_tel'),instagram:insta(val(f,'p_'+p[0]+'_ig'))}}).filter(function(p){return p.nom||p.tel||p.instagram})}
var CHIPS=[['mariage','Mariage'],['naissance','Grossesse et naissance'],['famille','Famille'],['couple','Couple'],['entreprise','Entreprise et événements'],['tableau','Tableau photo interactif']];

var offres='<section class="page top-space pad" data-page="/offres"><div class="wrap lf-offers">'+
'<div class="lf-mosaic" aria-hidden="true"><img class="lf-tall" src="thumbs/grossesse/g04.jpg" alt=""><img src="thumbs/grossesse/f8518a7e-0873-42c8-aa3b-6b0384f2e65f-1-102-o.jpg" alt=""><img src="thumbs/couple/p1020416.jpg" alt=""></div>'+
'<div class="lf-col"><h1>Les offres, avant tout le monde.</h1>'+
'<p class="lf-intro">Séances naissance et famille à tarif de saison, dates de mini-séances, nouveautés comme le tableau qui joue votre film : inscrivez-vous et choisissez ce qui vous intéresse. Je n’écris que lorsque j’ai quelque chose à vous proposer.</p>'+
'<form class="lf-form" id="lfOffres" novalidate>'+
'<div class="row2"><div><label for="lfp">Prénom</label><input id="lfp" name="prenom" autocomplete="given-name" required></div><div><label for="lfe">E-mail</label><input id="lfe" name="email" type="email" autocomplete="email" required></div></div>'+
'<div class="row2"><div><label for="lft">Téléphone (facultatif)</label><input id="lft" name="tel" type="tel" autocomplete="tel"></div><div><label for="lfd">Date prévue (mariage, naissance… facultatif)</label><input id="lfd" name="date" type="month"></div></div>'+
'<fieldset class="lf-set"><legend>Ce qui vous intéresse</legend><div class="lf-chips">'+
CHIPS.map(function(c){return '<label class="lf-chip"><input type="checkbox" name="interet" value="'+c[0]+'"><span>'+c[1]+'</span></label>'}).join('')+'</div></fieldset>'+
'<div class="lf-hp" aria-hidden="true"><label for="lfs">Ne pas remplir</label><input id="lfs" name="site" tabindex="-1" autocomplete="off"></div>'+
'<label class="lf-consent"><input type="checkbox" name="consent"><span>J’accepte de recevoir les offres et nouveautés de LMOH Photography par e-mail, et par SMS si j’ai indiqué mon numéro.</span></label>'+
'<p class="lf-err" role="alert"></p><button class="btn" type="submit">M’inscrire</button>'+
'<p class="lf-legal">Vos informations servent uniquement à LMOH Photography pour vous envoyer ses offres. Elles ne sont jamais revendues ni partagées. Vous pouvez vous désinscrire à tout moment, en un simple message. '+PRIV+'</p></form>'+
'<div class="lf-done" role="status"><h2>Merci, c’est noté.</h2><p>Vous serez parmi les premiers prévenus des prochaines offres.</p></div></div></div></section>';

var fiche='<section class="page top-space pad" data-page="/fiche-mariage"><div class="wrap lf-fiche">'+
'<div class="title"><span class="kicker">Votre mariage est réservé</span><h1>Votre fiche mariage</h1><p>Merci de votre confiance. Ces informations me permettent de préparer votre journée dans les moindres détails. Comptez dix minutes, et n’hésitez pas à compléter plus tard par message.</p></div>'+
'<form class="lf-form" id="lfFiche" novalidate>'+
'<h2 class="lf-part">Vous deux</h2>'+
'<div class="row2"><div><label for="fn1">Prénom et nom</label><input id="fn1" name="nom1" required></div><div><label for="fn2">Prénom et nom</label><input id="fn2" name="nom2" required></div></div>'+
'<div class="row2"><div><label for="fe">E-mail</label><input id="fe" name="email" type="email" autocomplete="email" required></div><div><label for="ft">Téléphone</label><input id="ft" name="tel" type="tel" autocomplete="tel" required></div></div>'+
'<label for="fa">Adresse postale (pour l’envoi de vos tirages ou de votre album)</label><input id="fa" name="adresse" autocomplete="street-address">'+
'<h2 class="lf-part">Votre mariage</h2>'+
'<div class="row2"><div><label for="fd">Date</label><input id="fd" name="date" type="date" required></div><div><label for="fi">Nombre d’invités (environ)</label><input id="fi" name="invites" type="number" min="0" step="10"></div></div>'+
'<div class="row2"><div><label for="fc">Lieu de la cérémonie (nom et ville)</label><input id="fc" name="ceremonie"></div><div><label for="fr">Lieu de la réception (nom)</label><input id="fr" name="reception"></div></div>'+
'<label for="fra">Adresse du lieu de réception</label><input id="fra" name="reception_adresse" autocomplete="off">'+
'<fieldset class="lf-set"><legend>Prestation réservée</legend><div class="lf-chips">'+
'<label class="lf-chip"><input type="radio" name="formule" value="photo"><span>Photo</span></label><label class="lf-chip"><input type="radio" name="formule" value="vidéo"><span>Vidéo</span></label><label class="lf-chip"><input type="radio" name="formule" value="photo et vidéo"><span>Photo et vidéo</span></label></div></fieldset>'+
'<h2 class="lf-part">Le jour J</h2>'+
'<div class="row2"><div><label for="fcn">Contact sur place (témoin, organisateur)</label><input id="fcn" name="contact_nom"></div><div><label for="fct">Son téléphone</label><input id="fct" name="contact_tel" type="tel"></div></div>'+
'<label for="fdr">Le déroulé prévu (préparatifs, cérémonie, cocktail, dîner…)</label><textarea id="fdr" name="deroule" rows="4"></textarea>'+
'<label for="fg">Les photos de groupe indispensables</label><textarea id="fg" name="groupes" rows="3"></textarea>'+
'<h2 class="lf-part">Pour mieux vous connaître</h2>'+
'<label for="fv">Ce qui compte le plus pour vous ce jour-là</label><textarea id="fv" name="envies" rows="3"></textarea>'+
'<div class="row2"><div><label for="fig">Vos comptes Instagram (facultatif)</label><input id="fig" name="instagram" placeholder="@…"></div><div><label for="fso">Comment m’avez-vous connu ?</label><select id="fso" name="source"><option value="">Choisir</option><option>Instagram</option><option>Google</option><option>Bouche-à-oreille</option><option>Un lieu de réception</option><option>Un salon du mariage</option><option>Autre</option></select></div></div>'+
'<h2 class="lf-part">Vos accords</h2>'+
'<label class="lf-consent"><input type="checkbox" name="image"><span>Nous autorisons LMOH Photography à publier une sélection de nos photos et vidéos sur son site et ses réseaux, sans nos noms.</span></label>'+
'<label class="lf-consent"><input type="checkbox" name="offres"><span>Nous acceptons de recevoir les offres de LMOH Photography (anniversaire de mariage, naissance, tableau photo interactif…) par e-mail ou SMS.</span></label>'+
'<div class="lf-hp" aria-hidden="true"><label for="fs">Ne pas remplir</label><input id="fs" name="site" tabindex="-1" autocomplete="off"></div>'+
'<p class="lf-err" role="alert"></p><button class="btn" type="submit">Envoyer ma fiche</button>'+
'<p class="lf-legal">Ces informations restent chez LMOH Photography. Elles servent à préparer votre mariage et, si vous l’avez accepté, à vous envoyer des offres. Elles ne sont jamais revendues ni partagées, et vous pouvez demander leur suppression à tout moment. '+PRIV+'</p></form>'+
'<div class="lf-done" role="status"><h2>Merci, votre fiche est bien arrivée.</h2><p>Je reviens vers vous très vite pour préparer la suite.</p></div></div></section>';

var conf='<section class="page top-space pad" data-page="/confidentialite"><div class="wrap lf-text">'+
'<div class="title"><h1>Confidentialité</h1><p>Comment vos informations sont utilisées et protégées.</p></div>'+
'<h2>Qui est responsable</h2><p>LMOH Photography, joignable à <a href="mailto:contact@lmohphotography.com">contact@lmohphotography.com</a>.</p>'+
'<h2>Les informations collectées</h2><p>Celles que vous indiquez vous-même dans les formulaires du site : le formulaire de contact, la fiche mariage (vos coordonnées et les informations sur votre journée) et l’inscription aux offres (prénom, e-mail, téléphone si vous le donnez, centres d’intérêt).</p>'+
'<h2>À quoi elles servent</h2><p>À répondre à vos demandes, à préparer et réaliser les prestations réservées, et, uniquement si vous l’avez accepté, à vous envoyer des offres et nouveautés. La fiche mariage repose sur l’exécution de votre réservation ; les offres reposent sur votre consentement, que vous pouvez retirer à tout moment.</p>'+
'<h2>Combien de temps</h2><p>Les informations des clients sont conservées pendant la relation, puis trois ans après le dernier contact. Celles des personnes inscrites aux offres, trois ans après le dernier contact, ou jusqu’à leur désinscription.</p>'+
'<h2>Qui y a accès</h2><p>Uniquement LMOH Photography. Les informations sont stockées sur Google Drive et transmises par un outil d’automatisation (Make), qui agissent comme prestataires techniques. Elles ne sont jamais vendues ni partagées à des fins commerciales.</p>'+
'<h2>Vos photos</h2><p>Une sélection de vos images n’est publiée que si vous l’avez autorisé, et sans vos noms.</p>'+
'<h2>Vos droits</h2><p>Vous pouvez demander à consulter, corriger ou supprimer vos informations, vous opposer à leur utilisation ou vous désinscrire des offres, en écrivant à <a href="mailto:contact@lmohphotography.com">contact@lmohphotography.com</a>. Vous pouvez aussi adresser une réclamation à la CNIL (cnil.fr).</p>'+
'<h2>Cookies</h2><p>Ce site n’utilise pas de cookies publicitaires ni de suivi.</p></div></section>';

var band='<section class="lf-band" aria-labelledby="lfbT"><div class="wrap lf-band-in"><div><h2 id="lfbT">Offres et nouveautés</h2><p>Mini-séances, offres de saison, nouveaux produits : soyez prévenus en premier.</p></div>'+
'<div><form class="lf-mini" id="lfMini" novalidate><input type="email" name="email" placeholder="Votre e-mail" autocomplete="email" aria-label="Votre e-mail"><div class="lf-hp" aria-hidden="true"><input name="site" tabindex="-1" autocomplete="off" aria-label="Ne pas remplir"></div><button class="btn" type="submit">Je m’inscris</button>'+
'<p class="lf-legal">En vous inscrivant, vous acceptez de recevoir les offres de LMOH Photography. Désinscription à tout moment. '+PRIV+'</p><p class="lf-err" role="alert"></p></form>'+
'<div class="lf-done" role="status"><h2>Merci, c’est noté.</h2><p>À très vite.</p></div></div></div></section>';

var main=document.querySelector('main');
main.insertAdjacentHTML('beforeend',offres+fiche+conf);
var footer=document.querySelector('footer');footer.insertAdjacentHTML('beforebegin',band);
var navUl=document.querySelector('nav.main > ul');
if(navUl){var last=navUl.lastElementChild;last.insertAdjacentHTML('beforebegin','<li><a href="#/offres">Recevoir des offres</a></li>')}
var fnav=footer.querySelector('nav');if(fnav){var ig=fnav.querySelector('a[href*="instagram"]');(ig?ig:fnav.lastChild).insertAdjacentHTML('beforebegin','<a href="#/offres">Offres</a><a href="#/confidentialite">Confidentialité</a>')}

function wire(id,build,check){
  var f=document.getElementById(id);if(!f)return;var box=f.parentNode,err=f.querySelector('.lf-err');
  f.addEventListener('submit',function(ev){ev.preventDefault();
    var msg=check(f);if(msg){err.textContent=msg;return}
    err.textContent='';var b=f.querySelector('button');b.disabled=true;
    send(build(f)).then(function(){box.classList.add('lf-sent');if(id==='lfFiche'||id==='lfOffres')window.scrollTo(0,box.offsetTop-90)})
    .catch(function(){b.disabled=false;err.textContent='L’envoi n’a pas fonctionné. Réessayez, ou écrivez-moi à contact@lmohphotography.com.'});
  });
}
wire('lfOffres',function(f){return {type:'offres',prenom:val(f,'prenom'),email:val(f,'email'),tel:val(f,'tel'),date:val(f,'date'),interets:checks(f,'interet'),consent:'oui',provenance:'page Offres',site:val(f,'site')}},
 function(f){if(!val(f,'prenom'))return 'Indiquez votre prénom.';if(!ok(val(f,'email')))return 'Indiquez une adresse e-mail valide.';if(!f.elements.consent.checked)return 'Cochez la case pour accepter de recevoir les offres.';return ''});
wire('lfMini',function(f){return {type:'offres',prenom:'',email:val(f,'email'),consent:'oui',provenance:'bas de page',site:val(f,'site')}},
 function(f){return ok(val(f,'email'))?'':'Indiquez une adresse e-mail valide.'});
wire('lfFiche',function(f){return {type:'mariage',nom1:val(f,'nom1'),nom2:val(f,'nom2'),email:val(f,'email'),tel:val(f,'tel'),adresse:val(f,'adresse'),date:val(f,'date'),invites:val(f,'invites'),ceremonie:val(f,'ceremonie'),reception:val(f,'reception'),formule:checks(f,'formule'),contact_nom:val(f,'contact_nom'),contact_tel:val(f,'contact_tel'),deroule:val(f,'deroule'),groupes:val(f,'groupes'),envies:val(f,'envies'),instagram:val(f,'instagram'),source:val(f,'source'),image:f.elements.image.checked?'oui':'non',offres:f.elements.offres.checked?'oui':'non',site:val(f,'site')}},
 function(f){if(!val(f,'nom1')||!val(f,'nom2'))return 'Indiquez vos deux prénoms et noms.';if(!ok(val(f,'email')))return 'Indiquez une adresse e-mail valide.';if(!val(f,'tel'))return 'Indiquez un numéro de téléphone.';if(!val(f,'date'))return 'Indiquez la date du mariage.';return ''});

/* Bouton flottant WhatsApp « Une question ? » */
var wa=document.createElement('a');wa.className='lf-wa';wa.target='_blank';wa.rel='noopener';
wa.href='https://wa.me/33651287900?text='+encodeURIComponent('Bonjour Lmoh, j’ai une question : ');
wa.setAttribute('aria-label','Une question ? Écrivez-moi sur WhatsApp');
wa.innerHTML='<span class="lf-wa-ico" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3.2c-4.9 0-8.8 3.5-8.8 7.9 0 2.3 1.1 4.4 2.9 5.9l-.9 3.6 3.8-2.1c.9.3 1.9.4 3 .4 4.9 0 8.8-3.5 8.8-7.8S16.9 3.2 12 3.2z" fill="none" stroke="#fff" stroke-width="1.7" stroke-linejoin="round"/><circle cx="8.3" cy="11.1" r="1.1" fill="#fff"/><circle cx="12" cy="11.1" r="1.1" fill="#fff"/><circle cx="15.7" cy="11.1" r="1.1" fill="#fff"/></svg></span><span class="lf-wa-txt">Une question ?</span>';
document.body.appendChild(wa);
var lbEl=document.getElementById('lb');if(lbEl&&'MutationObserver' in window){new MutationObserver(function(){wa.classList.toggle('lf-wa-off',lbEl.classList.contains('open'))}).observe(lbEl,{attributes:true,attributeFilter:['class']})}

var r=location.hash.replace(/^#/,'');
if(r==='/offres'||r==='/fiche-mariage'||r==='/confidentialite'){window.dispatchEvent(new HashChangeEvent('hashchange'))}
})();
