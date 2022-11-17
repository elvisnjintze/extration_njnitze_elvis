import requests
import csv
from bs4 import BeautifulSoup
url_cat="http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html"#on recupère l'url sur le
#catologue

rep=requests.get(url_cat)
pag=BeautifulSoup(rep.content,'html.parser')
cat=pag.findAll('li',class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")#l'idée est de sortir ayant récupèrer tous les lien sur tous les élements
# de la page et on met dans la liste nommée lien

list=[]

for h in cat:       #pour chaque élément de la liste cat l'élément de la balise 'a'
    bon=h.find('a')
    list.append(bon)
#print(list)               #dans list, on a les éléments de la balise 'a'
ref=[]
for t in list:        # chaque élément de list est un dictionnaire ayant une clé 'href' on la recupère
    d=t['href']
    ref.append(d)

#print(ref)

lien=[]
for r in ref:                         #chaque élément de ref est comme ceci ../../../the-torch-is-passed-a-harding-family-story_945/index.html

    b=r[8:]                           # il faut éliminer les 8 premiers caractère du debut soit ../../..
    c=''.join(b)                      # on créee une nouvelle chaine de caractère
    l="http://books.toscrape.com/catalogue"+c   # remplacement de la partie supprimée recement par "http://books.toscrape.com/catalogue"
    lien.append(l)
                        #lien est une liste contenant tout les liens sur les livres de la page

#à prèsent on va récupérer s'il existe le contenu du bouton "next"
next=pag.findAll('li',class_="next")
if next:
    for b in next:
        nexti = b.find('a')
        #on sort de la boucle avec un élément de type dictionnaire ayant une clé nommé href
    n=nexti['href']
    u=url_cat[:-10]    # on enlère les dix derniers élt
    ur=''.join(u)
    next_url=ur+n
    #print(next_url)


#pagination=1
iteration=1             # cette variable doit nous permettre de controler la création du fichier de stockage
for link in lien:
    """ici l'url de notre première page dont nousallons récupérer les infos"""
    url = link
    reponse = requests.get(url)  # récupération de la page

    # parser la page en indiquant qu'elle contient les données html
    # ceci permettra de pourvoir faire des recherche à l'interieur
    page = BeautifulSoup(reponse.text, 'html.parser')
    # recuperation du titre du livre
    # title=page.find('title').string, cette méthode est bonne mais il y a une chaine caractère qui revient (BOOK TO SCRAP....)
    # attention la méthode find de l'objet page retourne une chaine de caractère
    # alors que la méthode findAll retourne liste de dictionnaire
    title = page.findAll(class_="col-sm-6 product_main")  # recupération des éléments de l'attribut class_="col-sm-6 product_main"
    titre = ""  # variable qui contiendra le titre de notre livre
    for i in title:
        t = i.find('h1')  # pour chaque élément de la liste je cherche le bloc  ayant la balise h1
        titre = t.text  # je suis sur de n'avoir qu'un seul élément
    #print("le titre du livre est: ", titre)
    # recupération de la description d'un livre
    # description=page.findAll('article',class_="product_page")
    des = page.findAll('p')
    description = des[3].text  # 'p' est le seul critère de selection que j'ai trouvé et je trouve que mon elt recherché est
    # en quatrième position position dans la liste des (c'est un du vol mais bon ça marche)
    # print (description)

    # on recupere la catégorie du livre
    cat = page.findAll('ul', class_="breadcrumb")
    # print(len(cat))
    a = []
    for i in cat:
        x = i.findAll('a')  # x est une liste
        a.append(x)
    # print(a)# a est une liste d'un seul elt
    y = a[0]
    categorie = y[2].text
    #print("la catégorie de ce livre est: ", categorie)

    # on recupère l'url de l'image du livre
    img = page.findAll('img')  # la fonction findAll retourne une liste de dictionaire ayant une clé src
    # et la liste n'a qu'un seul élément
    m = img[0]['src']  # valeur de m: ../../media/cache/c7/1a/c71a85dbf8c2dbc75cb271026618477c.jpg
    # on cherche à remplacer '../..'par '	http://books.toscrape.com')
    #n = list(m)  # conversion de la chaine de caractère en list
    k = m[5:]  # suppression des cinq premiers éléments de la liste
    p = ''.join(k)
    img_url = "http://books.toscrape.com" + p
    #print(img_url)

    # on a le l'url de la page qui est url et le titre du livre dans titre
    """on doit cette fois ci recupérer les autres éléments à savoir les upc"""
    # on remarque que sur notre page tout les éléments caractéristique de notre livre sont dans une table
    # ayant des lignes et chaque ligne tr possède 2 cellules un th et l'autre td
    # on recupere les th et td dans deux liste th et td
    # th=page.findAll('th')#on récupere tous les éléments portant th
    td = page.findAll('td')  # on recupère tous les éléments portant la balise td
    # print(th)
    # print(td)
    # nous allons construire deux listes ayant d'un coté les libellés et l'autre les valeurs
    """libelle=[]
    for i in th:
        t=i.text # ici on récupère le text dans les élts de th
        libelle.append(t)
    print(libelle)"""

    valeur = []
    for i in td:
        p = i.text
        valeur.append(p)

    if iteration==1:
        # écriture dans le fichier
        livre="dossier_des_livres/"+"livre_"+categorie+".csv"
        with open(livre, "w") as fich:
            writer = csv.writer(fich, delimiter=',')
            entete = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax",
                  "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                  "image_url"]
            writer.writerow(entete)
            iteration=iteration+1
            #print (livre)
            # ajout et rangement des valeurs dans la liste de valeurs pour respecter le format de la liste entete
            # on ajoute l'url de la page au debut de la liste valeur
            valeur.insert(0, url)
            # on met le titre du livre en troisième position
            valeur[2] = titre
            del valeur[5]  # suppression de la valeur de la taxe
            # échanger les valeurs en position 3 et 4 soit price_excluding_tax et price_including_tax et supprimer le caractère
            # A qui s'affiche en debut
            prix_exclu = valeur[3]
            prix_inclu = valeur[4]
            prix_exc = prix_exclu[1:]
            prix_inc = prix_inclu[1:]
            valeur[3] = prix_inc
            valeur[4] = prix_exc
            valeur.insert(6, description)
            valeur.insert(7, categorie)
            valeur.append(img_url)
            # recupération de la description du produit que nous mettrons dans la liste des valeurs
            writer.writerow(valeur)
            #pagination=pagination+1
            fich.close()
    else:
        with open(livre,"a")as fich:
            writer = csv.writer(fich, delimiter=',')
            # on ajoute l'url de la page au debut de la liste valeur
            valeur.insert(0, url)
            # on met le titre du livre en troisième position
            valeur[2] = titre
            del valeur[5]  # suppression de la valeur de la taxe
            # échanger les valeurs en position 3 et 4 soit price_excluding_tax et price_including_tax et supprimer le caractère
            # A qui s'affiche en debut
            prix_exclu = valeur[3]
            prix_inclu = valeur[4]
            prix_exc = prix_exclu[1:]
            prix_inc = prix_inclu[1:]
            valeur[3] = prix_inc
            valeur[4] = prix_exc
            valeur.insert(6, description)
            valeur.insert(7, categorie)
            valeur.append(img_url)
            writer.writerow(valeur)
            print(valeur)
           