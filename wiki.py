# -*- coding: utf-8 -*-

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import requests
from bs4 import BeautifulSoup

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
        """
        result=requests.post(self.baseURL+'api.php?action=query&titles='+page+'&export&exportnowrap')
        soup=BeautifulSoup(result.text, "lxml")
        code=''
        for primitive in soup.findAll("text"):
            code+=primitive.string
        return code
