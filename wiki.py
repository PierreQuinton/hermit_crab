# -*- coding: utf-8 -*-

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import requests
from bs4 import BeautifulSoup
import re

from graph import Graph

class Wiki:
    """ Simplifie l'acces a wiki """
    def __init__(self, user, password, baseURL='http://wikipast.world/wiki/'):
        """
        :param user: nom d'utilisateur du bot
        :param password: mot de passe du bot
        :param baseURL: url du wiki
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
        :param page: page to write to
        :param append: if false we replace, else we add it at the end
        :param summary: summary du bot (message associé aux modifications qu'il apporte)
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
#TODO add a find method with which we can play with groups in a more regex like way
    def find(self, pages, patterns):
        """
        :param page: page or list of pages in which we sould search
        :param pattern: regex pattern or list of patterns to parse the page with, see https://docs.python.org/2/library/re.html
        :return: return all the matches
        """
        if type(pages) == type(''):
            pages = [pages]
        if type(patterns) == type(''):
            patterns = [patterns]
        res = []
        unionPattern = '|'.join(patterns)
        for page in pages:
            res.append(re.findall(unionPattern, self.readPage(page)))
        return res

    def replace(self, pages, mapping, summary='Bot modification'):
        """
        :param page: page in which we should replace
        :param mapping: a dict that match patterns with their replacement
        :param summary: summary du bot (message associé aux modifications qu'il apporte)
        :return: the new page content and the amount of replacement done in a tuple
        """
        if type(pages) == type(''):
            pages = [pages]
        res = (0, [])
        patterns = mapping.keys()
        unionPattern = '|'.join(patterns)
        for page in pages:
            c = self.readPage(page)
            length = len(c)
            newContent = c
            offset = 0
            for m in re.finditer(unionPattern, c):
                res = (res[0]+1,res[1])
                matchText = c[m.start():m.end()]
                i = 0
                for p in patterns:
                    if re.match(p, matchText) != None:
                        replaceContent = re.sub(p, mapping[p], matchText)
                        if m.start() != 0 and m.end() != length-1:
                            newContent = newContent[:m.start()+offset] + replaceContent + c[m.end():]
                        elif m.start() == 0 and m.end() != length-1:
                            newContent = replaceContent + c[m.end():]
                        elif m.start() != 0 and m.end() == length-1:
                            newContent = newContent[:m.start()+offset] + replaceContent
                        else:
                            newContent = replaceContent
                        offset += len(replaceContent) - (m.end()-m.start())
                        break
                    i = i+1
            res[1].append(newContent)
            self.writeToPage(newContent, page, False, summary)
        return res

    def replaceWords(self, pages, mapping, summary='Bot modification'):
        """
        :param page: page in which we should replace
        :param mapping: mapping of words to replace and their replacement
        :param summary: summary du bot (message associé aux modifications qu'il apporte)
        :return: the new page content and the amount of replacement done in a tuple
        """
        # we escape the sequence to avoid parsing in it
        newDict = {}
        for m in mapping.keys():
            newDict.update({re.escape(m):re.escape(mapping[m])})
        return self.replace(pages, newDict, summary)

    def getGraphFrom(self, page, deepness=-1, outSider=False):
        """
        :param page: starting page
        :param deepness: max deepness of the graph, if less than 0 will do all the graph
        :param outsider: if we want or not the outsider link of format [link] in the graph, they will not be nodes
        :return: a graph of the page relationships
        """
        graph = Graph()
        if deepness != 0:
            edges = {}
            for x in self.find(page, r'\\[\\[(.+)\\]\\]'):
                #TODO don't do it if already in list
                name = x[2:-2]
                graph.addNode(name)
                edge.add(name)
                graph.merge(self.getGraphFrom(name, deepness-1, outSider))
            if outSider:
                for x in self.find(page, r'\\[[^\\[\\]]+\\]')
                    edge.add(x[1:-1])
            graph.addConnexions(page, edges)
        return graph



