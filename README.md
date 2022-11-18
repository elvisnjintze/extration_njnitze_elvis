#extration_njintze_elvis
ce projet consiste à extraire les données d'un site web.
le contexte est le suivant:
entend qu'employé au service marketing de ma sociéte l'une des taches
qui m'a éte assignée est de consevoir une application qui se chargera d'extraire 
les informations chez un concurrent vendeur aussi des anciens livres
en ligne donc le nom est BOOK TOSCRAPE.
https://books.toscrape.com/ ceci est le lien de ce concurrent.

l'application consiste à aller dans ce site extraire les donnée des livres présents dans ce site
stocker ces données en local (dans deux dossier préalablement crées)

il faut créer et activer l'environnement virtuelle avant toute chose:
commande python3 -venv env, et installer les paquets prèsent dans requirement.txt: commande pip install -r requirements.txt

lorsque vous lancez l'application vous  aurez dans le terminal le mot
"download successful" vous indiquant pour chaque livre que son image a été téléchargée anvec sucès.
n'oubliez pas d'intaller les paquets nécessaires dans requiements.txt

le lien de mon repos github est le suivant: https://github.com/elvisnjintze/extration_njnitze_elvis

nous avons constuit cette application en trois phase:
1- la première phase consiste à aller sur l'url d'un livre chercher des informations sur ce dernier
product_page_url,
universal_ product_code (upc),
title,
price_including_tax,
price_excluding_tax,
number_available,
product_description,
category,
review_rating,
image_url

# ici nous avons produit le code nommé: **_extraction_par_livre.py_**

2- les livres étants rangés par catégorie, pour chaque catégorie
données on parcours chacun des livres de la catégorie et lui inflige
le traitement précedement énoncé

# A cette étape on a le code nomé: **extraction_cat_livre.py**

3- les catégories se trouvent à la racine du site, ici on recupère la liste de ces catégories et
pour chacune de ces catégories on applique le traitement précédent

A la suite nous avons les resultats rengés dans les dossiers 
--images contenants les images pour chaque livres
--dossier_des_livres contenants des fichiers .csv pour chaque catégorie

# le programme pour ceci est: **_tout_extraction.py_**


        MERCI