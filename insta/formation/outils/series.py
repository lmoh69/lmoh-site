import sys
sys.path.insert(0, '/home/claude')
from engine import build, V, P

F2 = f'{V}/film-2.mov'; F1 = f'{V}/film-1.mov'; R1 = f'{V}/mariage-reel-1.mp4'; R2 = f'{V}/mariage-reel-2.mp4'
M1, M2, M3 = (f'{P}/etranger-marrakech-{i}.jpg' for i in (1, 2, 3))
C1, C3 = f'{P}/etranger-dubai-1.jpg', f'{P}/etranger-dubai-3.jpg'

PRICE = {'say': 'Formation photo, vidéo et IA. À partir de trois cents euros.', 'bg': ('price',)}
CTA = {'say': 'Écris FORMATION en message.', 'bg': ('cta',)}

def T(*lines, hl=()):
    return [{'t': l, 'size': 96, 'hl': list(hl)} for l in lines]

S = {}

S['hook2'] = [
    {'say': 'Ton concurrent ne dort plus.', 'bg': ('vid', F2, 1, 'dark'), 'text': T('TON CONCURRENT', 'NE DORT PLUS', hl=['DORT']), 'y': 760},
    {'say': 'Ses posts sortent tout seuls. Ses réponses partent toutes seules.', 'bg': ('vid', R2, 3, 'warm'), 'text': T('SES POSTS SORTENT', 'TOUT SEULS', hl=['SEULS'])},
    {'say': 'Pendant que toi, tu y passes tes dimanches.', 'bg': ('vid', F1, 0, 'bw'), 'text': T('ET TOI ?', 'TES DIMANCHES', 'Y PASSENT', hl=['DIMANCHES'])},
    {'say': "Ce n'est pas de la magie. Ce sont des automatisations.", 'bg': ('big', 'CE N\'EST PAS DE LA MAGIE', ['Ce sont des', 'automatisations.'], None)},
    {'say': "Je t'apprends à les mettre en place. Sans coder.", 'bg': ('img', M1, 'dim'), 'text': T("JE T'APPRENDS", 'SANS CODER', hl=['SANS', 'CODER']), 'y': 1350},
    PRICE, CTA]

S['hook3'] = [
    {'say': "Voilà ce que l'IA fait pendant que je dors.", 'bg': ('vid', F2, 0, 'dark'), 'text': T("CE QUE L'IA FAIT", 'PENDANT QUE', 'JE DORS', hl=['DORS']), 'y': 700},
    {'say': 'Elle prépare et programme mes publications.', 'bg': ('vid', R2, 8, 'warm'), 'text': T('1. ELLE PROGRAMME', 'MES POSTS', hl=['POSTS'])},
    {'say': "Elle m'envoie un SMS quand un post est publié.", 'bg': ('vid', R1, 2, 'dim'), 'text': T("2. ELLE M'ENVOIE", 'UN SMS', hl=['SMS'])},
    {'say': "Elle m'aide à trier et à monter mes vidéos.", 'bg': ('vid', F2, 12, 'dim'), 'text': T("3. ELLE M'AIDE", 'À MONTER', hl=['MONTER'])},
    {'say': "Toi aussi, tu peux le faire. Pas besoin d'être informaticien.", 'bg': ('big', 'ET TOI ?', ['Pas besoin', "d'être informaticien."], None)},
    PRICE, CTA]

S['hook4'] = [
    {'say': 'Arrête. De tout faire. À la main.', 'bg': ('vid', R1, 1, 'dark'), 'text': T('ARRÊTE', 'DE TOUT FAIRE', 'À LA MAIN', hl=['ARRÊTE']), 'y': 760},
    {'say': 'Poster sur Instagram, Facebook, TikTok. Un par un ?', 'bg': ('vid', F1, 1, 'bw'), 'text': T('INSTA. FACEBOOK.', 'TIKTOK.', 'UN PAR UN ?', hl=['UN', 'PAR']), 'y': 1150},
    {'say': 'Une seule automatisation peut le faire pour toi.', 'bg': ('vid', R2, 10, 'warm'), 'text': T('UNE SEULE', 'AUTOMATISATION', hl=['AUTOMATISATION'])},
    {'say': 'Je te montre comment. Étape par étape.', 'bg': ('img', C3, 'dim'), 'text': T('ÉTAPE', 'PAR ÉTAPE', hl=['ÉTAPE']), 'y': 1350},
    PRICE, CTA]

S['hook5'] = [
    {'say': 'Les agents IA arrivent dans nos métiers. Que tu le veuilles ou non.', 'bg': ('vid', F2, 2, 'dark'), 'text': T('LES AGENTS IA', 'ARRIVENT', 'DANS NOS MÉTIERS', hl=['AGENTS', 'IA']), 'y': 700},
    {'say': "Ceux qui s'y mettent maintenant prennent de l'avance.", 'bg': ('vid', R2, 5, 'warm'), 'text': T("CEUX QUI S'Y METTENT", "PRENNENT DE L'AVANCE", hl=["L'AVANCE"])},
    {'say': 'Les autres vont courir derrière.', 'bg': ('vid', F1, 2, 'bw'), 'text': T('LES AUTRES', 'VONT COURIR', 'DERRIÈRE', hl=['DERRIÈRE'])},
    {'say': 'Dans ma formation, tu apprends à les utiliser pour ton activité.', 'bg': ('img', M1, 'dim'), 'text': T('APPRENDS À', 'LES UTILISER', hl=['UTILISER']), 'y': 1350},
    PRICE,
    {'say': 'Ne reste pas à la traîne. Écris FORMATION en message.', 'bg': ('cta',)}]

S['hook6'] = [
    {'say': 'Trois tâches que tu ne devrais plus faire toi-même.', 'bg': ('big', '3 TÂCHES', ['que tu ne devrais', 'plus faire toi-même'], None)},
    {'say': 'Un. Relancer tes prospects un par un.', 'bg': ('vid', R1, 3, 'dim'), 'text': T('1', 'RELANCER', 'TES PROSPECTS', hl=['1'])},
    {'say': 'Deux. Publier tes posts à la main.', 'bg': ('vid', R2, 12, 'warm'), 'text': T('2', 'PUBLIER', 'À LA MAIN', hl=['2'])},
    {'say': 'Trois. Trier tes rushs pendant des heures.', 'bg': ('vid', F2, 13, 'dim'), 'text': T('3', 'TRIER TES RUSHS', hl=['3'])},
    {'say': "L'IA et les automatisations peuvent t'aider sur les trois.", 'bg': ('img', C1, 'dim'), 'text': T("L'IA PEUT T'AIDER", 'SUR LES 3', hl=['3']), 'y': 1350},
    PRICE, CTA]

S['hook7'] = [
    {'say': 'Tu es photographe. Pas secrétaire.', 'bg': ('vid', R1, 0, 'dark'), 'text': T('TU ES PHOTOGRAPHE.', 'PAS SECRÉTAIRE.', hl=['SECRÉTAIRE.']), 'y': 820},
    {'say': 'Alors pourquoi tu passes plus de temps sur tes mails que derrière ton appareil ?', 'bg': ('vid', F1, 0, 'bw'), 'text': T('PLUS DE MAILS', "QUE DE PHOTOS ?", hl=['MAILS'])},
    {'say': 'Laisse les automatisations gérer le reste.', 'bg': ('vid', R2, 6, 'warm'), 'text': T('LAISSE', "L'IA GÉRER", 'LE RESTE', hl=["L'IA"])},
    {'say': 'Et récupère ton temps pour créer.', 'bg': ('img', M1, 'dim'), 'text': T('RÉCUPÈRE', 'TON TEMPS', 'POUR CRÉER', hl=['CRÉER']), 'y': 1300},
    PRICE, CTA]

S['hook8'] = [
    {'say': 'En deux mille vingt-sept, tu fais encore tout tout seul ?', 'bg': ('vid', F2, 0, 'dark'), 'text': T('EN 2027', 'TU FAIS ENCORE', 'TOUT TOUT SEUL ?', hl=['2027']), 'y': 720},
    {'say': 'Tes futurs clients attendent des réponses rapides.', 'bg': ('vid', R2, 14, 'warm'), 'text': T('TES CLIENTS', 'ATTENDENT', 'DES RÉPONSES', hl=['RÉPONSES'])},
    {'say': 'Une automatisation peut te prévenir pendant que tu shootes.', 'bg': ('vid', R1, 4, 'dim'), 'text': T('ELLE TE PRÉVIENT', 'PENDANT QUE', 'TU SHOOTES', hl=['SHOOTES'])},
    {'say': "Je t'apprends à la créer. Pas à pas.", 'bg': ('img', C3, 'dim'), 'text': T("JE T'APPRENDS", 'PAS À PAS', hl=['PAS']), 'y': 1350},
    PRICE, CTA]

# Tutos : schémas guidés
N1 = ['Google Drive', 'Make', 'Instagram', 'Planning']
S['tuto1'] = [
    {'say': 'Publier automatiquement sur Instagram. Sans coder. En quatre étapes.', 'bg': ('big', 'TUTO EXPRESS', ['Publier sur Instagram', 'automatiquement'], 'EN 4 ÉTAPES')},
    {'say': 'Étape un. Tu ranges ta photo dans un dossier Google Drive.', 'bg': ('step', 'POST INSTAGRAM AUTOMATIQUE', N1, 0, 1, ['Tu ranges ta photo', 'dans un dossier Drive'])},
    {'say': 'Étape deux. Dans Make, tu ajoutes le module qui surveille ce dossier.', 'bg': ('step', 'POST INSTAGRAM AUTOMATIQUE', N1, 1, 2, ['Dans Make, un module', 'surveille ce dossier'])},
    {'say': 'Étape trois. Tu le relies au module Instagram, publier une photo.', 'bg': ('step', 'POST INSTAGRAM AUTOMATIQUE', N1, 2, 3, ['Tu le relies au module', 'Instagram : publier'])},
    {'say': "Étape quatre. Tu choisis le jour et l'heure. Et ton post part tout seul.", 'bg': ('step', 'POST INSTAGRAM AUTOMATIQUE', N1, 3, 4, ["Tu choisis le jour", "et l'heure. C'est tout."])},
    {'say': 'Le pas à pas complet est dans ma formation. À partir de trois cents euros.', 'bg': ('price',)},
    CTA]

N2 = ['Formulaire', 'Make', 'SMS', 'Test']
S['tuto2'] = [
    {'say': 'Recevoir un SMS à chaque nouvelle demande de devis. Sans coder.', 'bg': ('big', 'TUTO EXPRESS', ['Un SMS à chaque', 'demande de devis'], 'EN 4 ÉTAPES')},
    {'say': 'Étape un. Ton formulaire de contact, sur ton site.', 'bg': ('step', 'ALERTE DEVIS PAR SMS', N2, 0, 1, ['Ton formulaire', 'de contact'])},
    {'say': 'Étape deux. Dans Make, un module reçoit chaque demande.', 'bg': ('step', 'ALERTE DEVIS PAR SMS', N2, 1, 2, ['Make reçoit', 'chaque demande'])},
    {'say': 'Étape trois. Tu ajoutes le module SMS avec ton numéro.', 'bg': ('step', 'ALERTE DEVIS PAR SMS', N2, 2, 3, ['Le module SMS', 'avec ton numéro'])},
    {'say': 'Étape quatre. Tu fais un test. Et tu ne rates plus aucun prospect.', 'bg': ('step', 'ALERTE DEVIS PAR SMS', N2, 3, 4, ['Tu testes.', 'Plus aucun prospect raté.'])},
    {'say': 'Je te montre tout, pas à pas, dans ma formation. À partir de trois cents euros.', 'bg': ('price',)},
    CTA]

N3 = ['3 mots', 'IA', 'Relecture']
S['tuto3'] = [
    {'say': "Une légende Instagram écrite avec l'IA. En trois étapes.", 'bg': ('big', 'TUTO EXPRESS', ['Ta légende Instagram', "avec l'IA"], 'EN 3 ÉTAPES')},
    {'say': 'Étape un. Tu donnes trois mots sur ta séance. Le lieu, l’ambiance, le couple.', 'bg': ('step', 'LÉGENDE AVEC L\'IA', N3, 0, 1, ['Tu donnes 3 mots', 'sur ta séance'])},
    {'say': "Étape deux. L'IA écrit une légende dans ton style.", 'bg': ('step', 'LÉGENDE AVEC L\'IA', N3, 1, 2, ["L'IA écrit", 'dans ton style'])},
    {'say': 'Étape trois. Tu relis, tu ajustes, et tu publies.', 'bg': ('step', 'LÉGENDE AVEC L\'IA', N3, 2, 3, ['Tu relis, tu ajustes,', 'tu publies'])},
    {'say': 'Je te montre comment bien le faire dans la formation. À partir de trois cents euros.', 'bg': ('price',)},
    CTA]

if __name__ == '__main__':
    for name in sys.argv[1:]:
        build(name, S[name])

S['video1'] = [
    {'say': 'Il y a deux types de photographes en ce moment.', 'bg': ('vid', F2, 1, 'dark'), 'text': [{'t': 'IL Y A', 'size': 110}, {'t': '2 TYPES', 'size': 190, 'hl': ['2', 'TYPES']}, {'t': 'DE PHOTOGRAPHES', 'size': 84}], 'y': 620},
    {'say': 'Ceux qui passent leurs soirées à trier, retoucher, et répondre aux messages.', 'bg': ('vid', F1, 0, 'bw'), 'text': T('CEUX QUI PASSENT', 'LEURS SOIRÉES À', 'TRIER. RETOUCHER.', 'RÉPONDRE.', hl=['TRIER', 'RETOUCHER', 'RÉPONDRE'])},
    {'say': 'Et ceux qui ont des agents IA qui le font pour eux.', 'bg': ('vid', R2, 2, 'warm'), 'text': T('ET CEUX QUI ONT', 'DES AGENTS IA', hl=['AGENTS', 'IA'])},
    {'say': "Moi, j'automatise mes publications, mes alertes, et une partie de mon montage.", 'bg': ('vid', F2, 12, 'dim'), 'text': T('JE LES AUTOMATISE :', '✓ PUBLICATIONS', '✓ ALERTES', '✓ MONTAGE', hl=['PUBLICATIONS', 'ALERTES', 'MONTAGE']), 'y': 1150},
    {'say': "Et je t'apprends à faire pareil.", 'bg': ('img', M1, 'dim'), 'text': T("ET JE T'APPRENDS", 'À FAIRE PAREIL', hl=['PAREIL']), 'y': 1350},
    PRICE,
    {'say': 'Ne reste pas à la traîne.', 'bg': ('vid', R1, 1, 'dark'), 'text': [{'t': 'NE RESTE PAS', 'size': 120}, {'t': 'À LA TRAÎNE', 'size': 140, 'hl': ['TRAÎNE']}], 'y': 760},
    CTA]

def run_voice(names):
    from engine import build_voice
    for n in names:
        build_voice(n, S[n], f'/home/claude/tts/g/{n}.wav')
