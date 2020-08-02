
#imports necessaires
from bs4 import BeautifulSoup
import re
import requests
from termcolor import colored
from time import sleep


# la description est un str sans retour à la ligne donc tout les 30 mots je mets un \n
def formatText(texte: str):
    mots = texte.split(' ')
    nbMots = len(mots)

    fini = ""

    for i in range(nbMots):
        fini += mots[i] + ' '
        if (i+1) % 24 == 0:
            fini += '\n'

    return fini


#site à scrape
site = 'https://www.torrentmac.net'


#avoir le html du site
r = requests.get(site)
soupePrinc = BeautifulSoup(r.text, 'html.parser')

# barre pricipale des torrent
principale = []
exempleArticle = """
# exemple : [<a class="home-thumb" href="https://www.torrentmac.net/adobe-acrobat-dc-v20-009-20074/"
                            # title="Adobe Acrobat DC v20.009.20074"><noscript><img alt="Adobe Acrobat Pro DC"
                            # class="attachment-post-thumbnail size-post-thumbnail wp-post-image" height="175"
                            #sizes="(max-width: 175px) 100vw, 175px"
                            # src="https://www.torrentmac.net/wp-content/uploads/2016/10/Adobe_Acrobat_PRO_DC_2015_icon-1.jpg"
                            # srcset="https://www.torrentmac.net/wp-content/uploads/2016/10/Adobe_Acrobat_PRO_DC_2015_icon-1.jpg 175w,
                            # https://www.torrentmac.net/wp-content/uploads/2016/10/Adobe_Acrobat_PRO_DC_2015_icon-1-150x150.jpg 150w"
                            # width="175"/></noscript><img alt="Adobe Acrobat Pro DC"
                            # class="lazyload attachment-post-thumbnail size-post-thumbnail wp-post-image"
                            # data-sizes="(max-width: 175px) 100vw, 175px" data-src="https://www.torrentmac.net/wp-content/uploads/2016/10/Adobe_Acrobat_PRO_DC_2015_icon-1.jpg"
                            # data-srcset="https://www.torrentmac.net/wp-content/uploads/2016/10/Adobe_Acrobat_PRO_DC_2015_icon-1.jpg 175w,
                            # https://www.torrentmac.net/wp-content/uploads/2016/10/Adobe_Acrobat_PRO_DC_2015_icon-1-150x150.jpg 150w"
                            # height="175" src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20175%20175%22%3E%3C/svg%3E"
                            # width="175"/></a>, <a href="https://www.torrentmac.net/adobe-acrobat-dc-v20-009-20074/"
                            # rel="bookmark" title="Adobe Acrobat DC v20.009.20074">Adobe Acrobat DC v20.009.20074</a>,
                            # <a href="https://www.torrentmac.net/category/applications/adobe/"
                            # rel="category tag">Adobe</a>, <a href="https://www.torrentmac.net/category/applications/"
                            # rel="category tag">Application</a>]
"""


# ajouter chaques html d'articles dans la liste
for article in soupePrinc.find_all('div', {'class': 'col620 clearfix'}):
    principale.extend(article)

# barre secondaire des torrents
secondaire = [a for a in soupePrinc.find_all('div', {'class': 'sidebar col300 right clearfix'})]

# on parcourt tt les html des articles -1 car le dernier n'est pas un article
for i, elem in enumerate(principale[:-1]):

    # le lien de l'article en cours
    if (res1 := re.search('(class="home-thumb" href=")(.*)(" title=")',
                     str(elem.find_all('a', {'class': 'home-thumb'})))):
        lien = res1.group(2)

        # recherche annexe pour avoir la description complte
        r2 = requests.get(lien)
        s2 = BeautifulSoup(r2.text, 'html.parser')

        if (res2 := re.search('(</h2><p>)(.*?)(\.</p><p>)',
                              str(s2.find_all('section', {'class': 'post_content clearfix'})))):
            descriptionComplete = res2.group(2)
        else:
            descriptionComplete = "PasDeDescription"

        if oTags := re.findall('<[a-zA-Z]*>', descriptionComplete):

            for tag in oTags:
                descriptionComplete = descriptionComplete.replace(tag, ' ')

        if cTags := re.findall('</[a-zA-Z]*>', descriptionComplete):
            for tag in cTags:
                descriptionComplete.replace(tag, ' ')

        if '<br/>' in descriptionComplete:
            descriptionComplete = descriptionComplete.replace('<br/>', '')

    else:
        lien = 'PasDeLien'
        descriptionComplete = 'PasDeDescription'



    # titre de l'article en cours
    if (res3 := re.search('(" title=")(.*)("><noscript><img alt=")',
                      str(elem.find_all('a', {'class': 'home-thumb'})))):
        titre = res3.group(2)
    else:
        titre = 'PasDeTitre'

    # date de l'article en cours
    if res4 := re.search('(\[<time datetime="\d{4}-\d{2}-\d{2}">)(.*)(</time>])', str(elem.find_all('time'))):
        date = res4.group(2)
    else:
        date = "PasDeDate"

    # catégories de l'article en cours
    if (res4 := re.search('(" rel="category tag">)(.*)(</a>, <a href=")(.*)(" rel="category tag">)(.*)(</a>)',
        str(elem.find_all('a', {'rel': 'category tag'})))):

        categorie1, categorie2 = res4.group(2,6)  # str(elem.find_all('a', {'rel': 'category tag'}))

    else:
        categorie1, categorie2 = 'PasDeCatégorie', 'PasDeCatégorie'

    # l'esperluette est désignée grace au marqueur '&amp'
    if '&amp;' in categorie2:
        categorie2.replace('&amp', '&')


    nombres = ['premier', 'deuxième', 'troisième', 'quatrième', 'cinquième', 'sixième', 'septième', 'huitième',
               'neuvième', 'dixième', 'onzième', 'douzième', 'treizième', 'quatorzième', 'quinzième', 'seizième',
               'dix-septième', 'dix-huitième', 'dix-neuvième', 'dernier']


    print(colored('-'*100, 'blue'),
          f"\nLe {nombres[i]} torrent est : {colored(titre, 'red')}:\n",
          colored(f"{formatText(descriptionComplete + '.')}\n", 'yellow'),
          colored(f"Catégories : {categorie1}, {categorie2}\n"),
          colored(f"Le {date}\n", 'cyan'),
          colored('-'*100, 'blue'))


    interet = input('Êtes vous intéressés par ce torrent ? (o/n)   : ')

    if interet == 'o':
        print(f"Lien pour {titre}: {lien}\n\n")
    else:
        print('\n\n\n')

        sleep(5)

