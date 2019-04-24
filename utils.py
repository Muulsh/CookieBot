# Author : Ttatanepvp123
# Github : https://github.com/ttatanepvp123
# License : GPL-3 ( https://www.gnu.org/licenses/gpl-3.0.en.html )
import requests
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError as e:
    print("Vous devez installer le module bs4 pour executer ce script")
    os.system("pause")
    exit()
import re

def getRealLink(link, url):
    if re.match(r"http[s]://", link) != None:
        return link
    elif link[0] == "/":
        return "/".join(url.split("/")[0:3])+link
    else:
        return "/".join(url.split("/")[0:len(url.split("/"))-1])+"/"+link

def getAllLinks(req : requests.Response):
    if "text/html" in req.headers["Content-Type"]:
        links = []
        soup = BeautifulSoup(req.text, "html.parser")
        for link in soup.find_all(["a", "link"]):
            tmp = link.get("href")
            if tmp != None:
                links.append(getRealLink(tmp, req.url))
        for link in soup.find_all(["img", "source", "script", "iframe"]):
            tmp = link.get("src")
            if tmp != None:
                links.append(getRealLink(tmp, req.url))
        for link in soup.find_all("form"):
            tmp = link.get("action")
            if tmp != None:
                links.append(getRealLink(tmp, req.url))
        return list(set(links))
    elif "text/" in req.headers["Content-Type"]:
        links = []
        for currentLink in re.findall(r"(http[s]://[a-zA-Z0-9\/\?=%\._\-]+)", req.text):
            links.append(currentLink)
        return list(set(links))
    else:
        return []