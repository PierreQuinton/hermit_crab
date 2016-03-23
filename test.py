# -*- coding: utf-8 -*-

from wiki import Wiki

if __name__ == '__main__':
    wiki = Wiki('Calamar', 'poulpe')
    content='==Biographie==\n'
    content+='Pour plus de simplicité utilisez [https://github.com/PierreQuinton/hermit_crab Hermit Crab] !\n'
    content+='==Références==\n'
    page='Bacasable'
    wiki.writeToPage(content, page, summary='Calamarification')
    
    content='\n=== Ngrams viewer ===\n'
    wiki.writeToPage(content, page, True, summary='Calamarification')
    
    newContent=wiki.readPage(page)
    print(newContent)
