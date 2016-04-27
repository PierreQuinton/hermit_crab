# -*- coding: utf-8 -*-

import re

def getSections(content, titleLevel):
    """
    :param content: content to get sections from
    :param titleLevel: level of title
    :return: return dict containing {tile:content}
    """
    titleEquals = ""
    for x in range(0, titleLevel):
        titleEquals = titleEquals + '='
    pattern = titleEquals + r'(([^=].*[^=])|[^=])' + titleEquals + r'\s+(((.+)(\s+))+)((?=(\s' + titleEquals + r')|\s*$))'
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
        functions = getSections(content, 2)
        print(functions)
