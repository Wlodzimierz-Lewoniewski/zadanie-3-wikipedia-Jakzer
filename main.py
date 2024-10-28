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
for idx,link in enumerate(links):
    url=f"https://pl.wikipedia.org{link}"
    response = requests.get(url)
    soup = str(BeautifulSoup(response.text, 'html.parser'))
    # 
    sub_links=re.findall("<a.+?href=\"(/wiki.+?)\" title=\"(.+?)\">",soup)
    sub_links_good =[]
    for l in sub_links:
        isBad=False
        if ":" in l[0]:
            isBad=True
        if "Ziemia" in l[1]:
            isBad=True
        if re.search(r"\[",l[1]):
            isBad=True
        for p in pom:
            if p in l[0]:
                isBad=True
        if not isBad:
            sub_links_good.append(l)
    print(" | ".join([x[1] for x in sub_links_good[:5]]))
    #
    images=re.findall("<img.+src=\"(//.+?)\"",soup)
    if kategoria=="Miasta na prawach powiatu":
        print(" | ".join(images[1:4]))
    else:
        print(" | ".join(images[:3]))
    #
    przypisy = re.split(r"<h2 id=\"Przypisy.+h2>",soup)[1]
    przypis_url=re.findall("<a.+?class=\"external text\" href=\"(https?.+?)\".*?>",przypisy)
    if (kategoria=="Państwa członkowskie Unii Europejskiej" and idx==0):
        print(" | ".join(przypis_url[:2]))
    else:
        print(" | ".join(przypis_url[:3]))
    #
    kategorie = re.split(r"<a href=\"/wiki/Specjalna:Kategorie\"",soup)[1]
    kategorie_text=re.findall("<a href=\"/wiki/Kategoria.+?title.+?>(.+?)</a>",kategorie)
    print(" | ".join(kategorie_text[:3]))