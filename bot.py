# -*- coding: utf-8 -*-

import re
import requests

def getSections(content):
    """
    :param content: content to get sections from
    :return: return dict containing {tile:content}
    """
    pattern = r'==(([^=].*[^=])|[^=])==\s+((([^=]+)(\s+))+)(?=(\s==))'
    res = {}
    for x in re.finditer(pattern, content):
        res.update({x.group(1):x.group(3)})
    return res

def getParts(content):
    """
    :param content: content to get parts from
    :return: return dict containing {tile:content}
    """
    pattern = r'<strong>([^<]+)</strong>\s+((([^<]+)(\s+))+)(?=(<strong>))'
    res = {}
    for x in re.finditer(pattern, content):
        res.update({x.group(1).lower():x.group(2)})
    pattern = r'<strong>([^<]+)</strong>\s+((([^<]+)(\s+))+)$'
    m = re.search(pattern, content)
    res.update({m.group(1).lower():m.group(2)})
    return res

def getList(content):
    """
    Take a "wiki" list ( with * ) and transform it to a python list
    :param content: content to transform in list
    :return: a python list from a wiki list
    """
    li = content.splitlines()
    ret = []
    for i in range(len(li)):
        if len(li[i]) > 0:
            if li[i][0] == "*":
                li[i] = li[i][1:]
            #remove space
            li[i] = li[i].strip()
            ret.append(li[i])
        
    return ret;

class Bot:
    """Representaion of a Bot"""
    def __init__(self, name, content):
        """
        :param content: content of the page (give it wiki.readpage(myPage))
        """
        self.name = name
        functions = getSections(content)
        self.functions = {}
        for i in functions.keys():
            parts = getParts(functions[i])
            temp = {}
            for j in parts.keys():
                temp.update({j:getList(parts[j])})
            self.functions.update({i:temp})
        
    def getFunction(self, name):
        """
        :param name: name of functions
        :return: code of function
        """
        return self.functions.get(name)
    def getFunctions(self):
        """
        :param name: name of functions
        :return: code of function
        """
        return self.functions.keys()
