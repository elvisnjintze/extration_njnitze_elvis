import requests
import csv
from bs4 import BeautifulSoup
url_cat="http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html"#on recupère l'url sur le
#catologue
rep=requests.get(url_cat)
pag=BeautifulSoup(rep.content,'html.parser')
cat=pag.findAll('li',class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")#on récupère tous les élements de la page
# on met dans cat

list=[]

for h in cat:       #pour chaque élément de la liste cat l'élément de la balise 'a'
    bon=h.find('a')
    list.append(bon)
#print(list)               #dans list, on a les éléments de la balise 'a'
ref=[]
for t in list:        # chaque élément de list est un dictionnaire ayant une clé 'href' on la recupère
    d=t['href']
    ref.append(d)

print(ref)

lien=[]
for r in ref:                         #chaque élément de ref est comme ceci ../../../the-torch-is-passed-a-harding-family-story_945/index.html

    b=r[8:]                           # il faut éliminer les 8 premiers caractère du debut soit ../../..
    c=''.join(b)                      # on créee une nouvelle chaine de caractère
    l="http://books.toscrape.com/catalogue"+c   # remplacement de la partie supprimée recement par "http://books.toscrape.com/catalogue"
    lien.append(l)
print(lien)                         #lien est une liste contenant tout les liens de la page
