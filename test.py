# -*- coding: utf-8 -*-

from wiki import Wiki

if __name__ == '__main__':
    wiki = Wiki('Calamar', 'poulpe')
    content='==Biographie==\n'
    content+='Veuillez écrire une biographie ici\n'
    content+='==Références==\n'
    page='Bacasable'
    wiki.writeToPage(content, page, summary='Calamarification')
    
    content='\n=== Ngrams viewer ===\n'
    wiki.writeToPage(content, page, True, summary='Calamarification')
    
    newContent=wiki.readPage(page)
    print(newContent)
