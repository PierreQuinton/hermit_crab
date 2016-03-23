# -*- coding: utf-8 -*-

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import requests
from bs4 import BeautifulSoup
import re

class Wiki:
    """ Simplifie l'acces a wiki """
    def __init__(self, user, password, baseURL='http://wikipast.world/wiki/'):
        """
        :param user: nom d'utilisateur du bot
        :param password: mot de passe du bot
        :param baseURL: url du wiki
        :param summary: summary du bot (message associé aux modifications qu'il apporte)
        """
        passw=urllib2.quote(password)
        login_params='?action=login&lgname=%s&lgpassword=%s&format=json'% (user,passw)
        # Login request
        r1=requests.post(baseURL+'api.php'+login_params)
        login_token=r1.json()['login']['token']

        #login confirm
        login_params2=login_params+'&lgtoken=%s'% login_token
        r2=requests.post(baseURL+'api.php'+login_params2,cookies=r1.cookies)

        #get edit token2
        params3='?format=json&action=query&meta=tokens&continue='
        r3=requests.get(baseURL+'api.php'+params3,cookies=r2.cookies)
        self.edit_token=r3.json()['query']['tokens']['csrftoken']
        self.edit_cookie=r2.cookies.copy()
        self.edit_cookie.update(r3.cookies)
        self.baseURL = baseURL

    def writeToPage(self, content, page, append=False, summary='Bot modification'):
        """
        :param content: content to push to page
        """
        headers={'content-type':'application/x-www-form-urlencoded'}
        if append:
            payload={'action':'edit','assert':'user','format':'json','appendtext':content,'summary':summary,'title':page,'token':self.edit_token}
        else:
            payload={'action':'edit','assert':'user','format':'json','text':content,'summary':summary,'title':page,'token':self.edit_token}
        r4=requests.post(self.baseURL+'api.php',headers=headers,data=payload,cookies=self.edit_cookie)

    def readPage(self, page):
        """
        :param page: page to get content from
        :return: the content of the page
        """
        result=requests.post(self.baseURL+'api.php?action=query&titles='+page+'&export&exportnowrap')
        soup=BeautifulSoup(result.text, "lxml")
        code=''
        for primitive in soup.findAll("text"):
            code+=primitive.string
        return code

    def search(self, page, pattern):
        """
        :param page: page in which we sould search
        :param pattern: regex pattern to parse the page with, see https://docs.python.org/2/library/re.html
        :return: return all the matches
        """
        #TODO: make page eigther a page or a list of pages
        return re.findall(pattern, self.readPage(page))

    def replace(self, page, pattern, replace, summary='Bot modification'):
        """
        :param page: page in which we should replace
        :param pattern: regex pattern to parse the page with, see https://docs.python.org/2/library/re.html
        :param replace: the replacement string (might want to use groups with \1, \2 ...)
        :return: the new page content and the amount of replacement done in a tuple
        """
        #TODO: make page eigther a page or a list of pages
        res = re.subn(pattern, replace, self.readPage(page))
        self.writeToPage(res[0], page, False, summary)
        return res



