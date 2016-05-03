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

class Bot:
    """Representaion of a Bot"""
    def __init__(self, content):
        """
        :param content: content of the page (give it wiki.readpage(myPage))
        """
        functions = getSections(content)
        print(functions)
