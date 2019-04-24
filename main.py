import os
import re
import time
import sys
import json
import getpass
import os
if os.name == "nt":
    os.system("title Cookie Bot v0.2.5")
if os.name == "posix":
    print(f"\x1b]2;Cookie Bot v0.2.5\x07", end="")

if sys.version_info[0] < 3:
    print("Vous devez executer ce script avec python 3 !")
    os.system("pause")
    exit()
try:
    import requests
except ModuleNotFoundError as e:
    print("Vous devez installer le module requests pour executer ce script")
    os.system("pause")
    exit()
import indexer


global token, showtoken, firsturl, config

showtoken = False
token = ""
firsturl = ""
config = "{}"
permWrite = False
permRead = False

print("\nBienvenue sur le CookieBot qui permet de crawler les pages pour alimenter le Cookie Search\n")

try:
    f = open("file", "w")
    f.write("cookie")
    f.close()
    os.remove('file')
    permWrite = True
except PermissionError as e:
    permWrite = False

try:
    f = open("config.json", "r")
    config = json.loads(f.read())
    permRead = True
except Exception:
    permRead = False
    print("[ERROR] Fichier de configuration automatique introuvable/endommagé")
    print("[INFO] Création du fichier...")
    try:
        f = open("config.json", "w")
        f.write("{}")
        f.close()
        permWrite = True
    except PermissionError as e:
        print("[ERROR] "+str(e))
        permWrite = False

if "--show-token" in sys.argv or "-st" in sys.argv:
    showtoken = True
    print("[INFO] Token visible : oui")
else:
    showtoken = False

if os.name == "nt":
    showtoken = True

class myIndexer(indexer.indexer):
    def onError(self, e):
        print('[ERROR] '+str(e))
    def onRequests(self, req : requests.Response):
        global token
        if req.status_code == 200:
            print("[INFO] : "+str(req.url))
            title = ""
            if "text/html" in req.headers["Content-Type"]:
                try:
                    soup = BeautifulSoup(req.text, "html.parser")
                    title = soup.head.find('title').text
                except:
                    pass
            data = {
                "url":req.url,
                "site":req.url.split("/")[2],
                "encoding":str(req.encoding).upper(),
                "timestamp":int(time.time()),
                "contentType":req.headers["Content-Type"].split(";")[0],
                "title":title,
                "token":token
            }
            requests.post("https://slackercompany.ml/CookieBot/send.php", data=data)

def userToken():
    global showtoken, config
    if showtoken:
        token = input("[ASK] Token: ")
    else:
        token = getpass.getpass("[ASK] Token: ")
    checkToken(token)

def userLink():
    global config
    link = input("[ASK] Lien de départ: ")
    checkLink(link)

def token():
    global config
    if permRead:
        try:
            print("[INFO] Lecture de l'objet token...")
            token = config["token"]
            print("[INFO] Objet token valide")
            checkToken(token)
        except Exception:
            print("[ERROR] Objet token invalide")
            if permWrite:
                if input("[ASK] Voulez vous supprimer le token invalide ? (y/n)") == "y":
                    config["token"] = ""
                    f = open("config.json", "w")
                    print("[INFO] Suppression...")
                    f.write(json.dumps(config))
                    f.close()
                    print("[INFO] Le token à été supprimer")
            userToken()
    else:
        userToken()
    

def link():
    global config
    if permRead:
        try:
            print("[INFO] Lecture de l'objet link...")
            link = config["link"]
            print("[INFO] Objet link valide")
            checkLink(link)
        except Exception:
            print("[ERROR] Objet link invalide")
            if permWrite:
                if input("[ASK] Voulez vous supprimer le lien de départ invalide ? (y/n)") == "y":
                    config["link"] = ""
                    f = open("config.json", "w")
                    print("[INFO] Suppression...")
                    f.write(json.dumps(config))
                    f.close()
                    print("[INFO] Le lien de départ à été supprimer")
            userLink()
    else:
        userLink()

def checkToken(tokentmp):
    global token, config
    print("[INFO] Test du token sur le serveur...")
    r = requests.get('https://slackercompany.ml/CookieBot/token.php?token='+tokentmp)
    rjson = r.json()
    if rjson["success"]:
        token = tokentmp
        print("[INFO] Token valide")
        print("[INFO] Compte actif : "+rjson["name"])
        if permWrite:
            if input("[ASK] Voulez vous enregistrer le token ? (y/n)") == "y":
                config["token"] = token
                f = open("config.json", "w")
                print("[INFO] Enregistrement...")
                f.write(json.dumps(config))
                f.close()
                print("[INFO] Le token à été enregistrer")
    else:
        print("[ERROR] Token invalide, veuillez reessayer")
        userToken()

def checkLink(linktmp):
    global firsturl, config
    if linktmp == "":
        userLink()
    else:
        if re.match(r"http://", linktmp) != None:
            firsturl = linktmp
        elif re.match(r"https://", linktmp) != None:
            firsturl = linktmp
        else:
            userLink()
        if permWrite:
            if input("[ASK] Voulez vous enregistrer le lien de départ ? (y/n)") == "y":
                config["link"] = firsturl
                f = open("config.json", "w")
                print("[INFO] Enregistrement...")
                f.write(json.dumps(config))
                f.close()
                print("[INFO] Le lien de départ à été enregistrer")

def launch():
    global firsturl
    token()
    link()
    print("[INFO] Démarrage en cours...")
    myIndexer(firsturl, threadNumber=25, timeout=5)

try:
    launch()
    
except KeyboardInterrupt:
    print("\n[INFO] Fermeture...")
