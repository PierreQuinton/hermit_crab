# -*- coding: utf-8 -*-

from wiki import Wiki
from bot import Bot
from executor import Executor
import re

def readBots(content):
    pattern = r'= Workers =\s+((([^=]+)(\s+))+)'
    m = re.search(pattern, content)
    li = m.group(1).splitlines()
    ret = []
    for i in range(len(li)):
        if len(li[i]) > 0:
            if li[i][0] == "*":
                li[i] = li[i][1:]
                #remove space
                li[i] = li[i].strip()
                ret.append(li[i])       
    return ret;

if __name__ == '__main__':
    masterBot = 'Utilisateur:Hermit Crab'
    
    wiki = Wiki('Utilisateur:Hermit Crab', 'poulpe')
    #Retrieve workers in main page

    bots = readBots(wiki.readPage(masterBot));

    pBots = [];

    for b in bots:
        name = b.strip()
        name = name[2:len(name)-2]
        pBots.append(Bot(name,wiki.readPage(name)))

    exe = Executor(wiki,pBots)

    exe.run()
