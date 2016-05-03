# -*- coding: utf-8 -*-

import re

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

class Bot:
    """Representaion of a Bot"""
    def __init__(self, content):
        """
        :param content: content of the page (give it wiki.readpage(myPage))
        """
        functions = getSections(content)
        self.functions = {}
        for i in functions.keys():
        	parts = getParts(i)
        	
        
