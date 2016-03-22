# -*- coding: utf-8 -*-

from wiki import Wiki

if __name__ == '__main__':
    wiki = Wiki('Calamar', 'poulpe', summary='Calamarification')
    content='==Biographie==\n'
    content+='Veuillez écrire une biographie ici\n'
    content+='==Références==\n'
    page='Calamar SandBox'
    wiki.writeToPage(content, page)
    
    content='=== Ngrams viewer ===\n'
    wiki.writeToPage(content, page, True)
