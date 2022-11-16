import requests #ici nous importons tout d'abord le paquet request qui permettra de recupérer la page web avec une url
from bs4 import BeautifulSoup
import csv
"""ici l'url de notre première page dont nousallons récupérer les infos"""
url="http://books.toscrape.com/catalogue/i-had-a-nice-time-and-other-lies-how-to-find-love-sht-like-that_814/index.html"
reponse=requests.get(url) #récupération de la page

#parser la page en indiquant qu'elle contient les données html
# ceci permettra de pourvoir faire des recherche à l'interieur
page=BeautifulSoup(reponse.text,'html.parser')
#recuperation du titre du livre
#title=page.find('title').string, cette méthode est bonne mais il y a une chaine caractère qui revient (BOOK TO SCRAP....)
#attention la méthode find de l'objet page retourne une chaine de caractère
#alors que la méthode findAll retourne liste de dictionnaire
title=page.findAll(class_="col-sm-6 product_main") #recupération des éléments de l'attribut class_="col-sm-6 product_main"
titre="" #variable qui contiendra le titre de notre livre
for i in title:
    t=i.find('h1') #pour chaque élément de la liste je cherche le bloc  ayant la balise h1
    titre=t.text  #je suis sur de n'avoir qu'un seul élément
print("le titre du livre est: ", titre)
#recupération de la description d'un livre
#description=page.findAll('article',class_="product_page")
des=page.findAll('p')
description=des[3].text# 'p' est le seul critère de selection que j'ai trouvé et je trouve que mon elt recherché est
# en quatrième position position dans la liste des (c'est un du vol mais bon ça marche)
#print (description)

# on recupere la catégorie du livre
cat=page.findAll('ul',class_="breadcrumb")
#print(len(cat))
a=[]
for i in cat:
    x=i.findAll('a')# x est une liste
    a.append(x)
#print(a)# a est une liste d'un seul elt
y=a[0]
categorie=y[2].text
print("la catégorie de ce livre est: ", categorie)


# on recupère l'url de l'image du livre
img=page.findAll('img')# la fonction findAll retourne une liste de dictionaire ayant une clé src
# et la liste n'a qu'un seul élément
m=img[0]['src'] # valeur de m: ../../media/cache/c7/1a/c71a85dbf8c2dbc75cb271026618477c.jpg
#on cherche à remplacer '../..'par '	http://books.toscrape.com')
n=list(m) #conversion de la chaine de caractère en list
k=n[5:]#suppression des cinq premiers éléments de la liste
p=''.join(k)
img_url="http://books.toscrape.com"+p
print(img_url)




# on a le l'url de la page qui est url et le titre du livre dans titre
"""on doit cette fois ci recupérer les autres éléments à savoir les upc"""
#on remarque que sur notre page tout les éléments caractéristique de notre livre sont dans une table
#ayant des lignes et chaque ligne tr possède 2 cellules un th et l'autre td
#on recupere les th et td dans deux liste th et td
#th=page.findAll('th')#on récupere tous les éléments portant th
td=page.findAll('td') # on recupère tous les éléments portant la balise td
#print(th)
#print(td)
#nous allons construire deux listes ayant d'un coté les libellés et l'autre les valeurs
"""libelle=[]
for i in th:
    t=i.text # ici on récupère le text dans les élts de th
    libelle.append(t)
print(libelle)"""

valeur=[]
for i in td:
    p=i.text
    valeur.append(p)


#écriture dans le fichier
with open("infos_livre.csv","w") as fich:
    entete=["product_page_url","universal_ product_code (upc)","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"]
    writer=csv.writer(fich, delimiter=',')
    writer.writerow(entete)
    #ajout et rangement des valeurs dans la liste de valeurs pour respecter le format de la liste entete
    #on ajoute l'url de la page au debut de la liste valeur
    valeur.insert(0,url)
    #on met le titre du livre en troisième position
    valeur[2]=titre
    del valeur[5] # suppression de la valeur de la taxe
    #échanger les valeurs en position 3 et 4 soit price_excluding_tax et price_including_tax et supprimer le caractère
    #A qui s'affiche en debut
    prix_exclu=valeur[3]
    prix_inclu=valeur[4]
    prix_exc=prix_exclu[1:]
    prix_inc=prix_inclu[1:]
    valeur[3]=prix_inc
    valeur[4]=prix_exc
    valeur.insert(6,description)
    valeur.insert(7,categorie)
    valeur.append(img_url)
    #recupération de la description du produit que nous mettrons dans la liste des valeurs
    writer.writerow(valeur)

print(valeur)