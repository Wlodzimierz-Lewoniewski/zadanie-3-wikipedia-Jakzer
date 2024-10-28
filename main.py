import requests
from bs4 import BeautifulSoup
import regex as re

kategoria = input()
pom =["Plik:","Kategoria:","Wikipedysta(-ka):","Wikipedia:","Pomoc:","Portal:","Wikiprojekt:",
"MediaWiki:","Szablon:","Moduł:","Specjalna:","Media:"]
# kategoria="Miasta na prawach powiatu"
url = f"https://pl.wikipedia.org/wiki/Kategoria:{kategoria}"
response = requests.get(url)
soup = str(BeautifulSoup(response.text, 'html.parser'))
html = re.split(r"<h2>Strony w kategorii .+</h2>",soup)[1]
links=re.findall("<a href=\"(.+)\" title.+</a>",html)
links = links[0:2]
for link in links:
    url=f"https://pl.wikipedia.org{link}"
    response = requests.get(url)
    soup = str(BeautifulSoup(response.text, 'html.parser'))
    # 
    break
    sub_links=re.findall("<a href=\"(.+?)\" title=\"(.+?)\">",soup)
    sub_links_good =[]
    for l in sub_links:
        isBad=False
        for p in pom:
            if p in l[0]:
                isBad=True
        if not isBad:
            sub_links_good.append(l)
    print(" | ".join([x[1] for x in sub_links_good[5:10]]))
    #
    images=re.findall("<img.+src=\"(//.+?)\"",soup)
    print(" | ".join(images[:3]))
    #
    przypisy = re.split(r"<h2 id=\"Przypisy.+h2>",soup)[1]
    przypis_url=re.findall("<a.+class=\"external text\".+href=\"(https.+?)\".+></a>",przypisy)
    print(" | ".join(przypis_url[:3]))
    #
    kategorie = re.split(r"<a href=\"/wiki/Specjalna:Kategorie\"",soup)[1]
    kategorie_text=re.findall("<a href=\"/wiki/Kategoria.+?title.+?>(.+?)</a>",kategorie)
    print(" | ".join(kategorie_text[:3]))