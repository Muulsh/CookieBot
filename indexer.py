# Author : Ttatanepvp123
# Github : https://github.com/ttatanepvp123
# License : GPL-3 ( https://www.gnu.org/licenses/gpl-3.0.en.html )
import _thread
import tempfile
import os
import time
import requests
import utils
import random

class indexer():
    # EVENTS
    def onReady(self):
        pass
    def onRequests(self, r : requests.Response):
        pass
    def onError(self, e):
        pass

    def addLinks(self, links):
        while self.linksFileIsOpen:
            time.sleep(0.005)
        self.linksFileIsOpen = True
        with open(f"{tempfile.gettempdir()}/{self.numberInstance}/links.txt", "a+") as fp:
            for currentLink in links:
                fp.write(f"{currentLink}\n")
        self.linksFileIsOpen = False

    def getLink(self):
        while self.linksFileIsOpen:
            time.sleep(0.005)
        self.linksFileIsOpen = True
        with open(f"{tempfile.gettempdir()}/{self.numberInstance}/links.txt", "r") as fp:#get first link
            link = fp.readline()
        with open(f"{tempfile.gettempdir()}/{self.numberInstance}/links.tmp", "w") as fp:#delete first link (without load file)
            with open(f"{tempfile.gettempdir()}/{self.numberInstance}/links.txt", "r") as fpp:
                for currentLine in fpp:
                    if currentLine != link:
                        fp.write(currentLine)
        os.remove(f"{tempfile.gettempdir()}/{self.numberInstance}/links.txt")
        os.rename(f"{tempfile.gettempdir()}/{self.numberInstance}/links.tmp", f"{tempfile.gettempdir()}/{self.numberInstance}/links.txt")
        self.linksFileIsOpen = False
        self.linksNumber -= 1
        return link.replace("\n","")
    
    def addLinkChecked(self, link):
        while self.linksCheckedFileIsOpen:
            time.sleep(0.005)
        self.linksCheckedFileIsOpen = True
        with open(f"{tempfile.gettempdir()}/{self.numberInstance}/checked.txt", "a+") as fp:
            fp.write(f"{link}\n")
        self.linksCheckedFileIsOpen = False

    def isChecked(self, link):
        returner = False
        while self.linksCheckedFileIsOpen:
            time.sleep(0.005)
        self.linksCheckedFileIsOpen = True
        with open(f"{tempfile.gettempdir()}/{self.numberInstance}/checked.txt", "r") as fp:
            for currentLink in fp:
                if currentLink.replace("\n","") == link:
                    returner = True
                    break
        self.linksCheckedFileIsOpen = False
        return returner

    def worker(self, link):
        try:
            if self.isChecked(link):
                self.threadStarted -= 1
                return
            else:
                self.addLinkChecked(link)
            r = requests.get(link, headers=self.headers, timeout=self.timeout)
            self.onRequests(r)
            links = self.getAllLinks(r)
            self.addLinks(links)
            self.linksNumber += len(links)
        except Exception as e:
            self.onError(e)
        self.threadStarted -= 1

    def __init__(self, url, threadNumber=5, headers={"User-Agent":"CookieBot/0.2 (+https://slackercompany.ml/CookieBot/)"}, timeout=10):
        self.getAllLinks = utils.getAllLinks
        self.linksFileIsOpen = False
        self.linksCheckedFileIsOpen = False
        self.threadStarted = 0
        self.headers = headers
        self.timeout = timeout
        self.numberInstance = random.randint(0,99999999)
        os.mkdir(f"{tempfile.gettempdir()}/{self.numberInstance}/")
        self.addLinkChecked("debug")
        self.addLinks([url])
        self.linksNumber = 1
        fakeDoWhile = False
        self.onReady()
        while True:
            time.sleep(0.0025)
            if self.threadStarted < threadNumber and self.linksNumber > 0:
                fakeDoWhile = True
                self.threadStarted += 1
                _thread.start_new_thread(self.worker, (self.getLink(),))
            elif fakeDoWhile and self.threadStarted == 0 and self.linksNumber == 0:
                break