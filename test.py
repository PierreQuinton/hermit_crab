# -*- coding: utf-8 -*-

from wiki import Wiki

if __name__ == '__main__':
    wiki = Wiki('Calamar', 'poulpe')
    content='===Biographie===\n'
    content+='Pour plus de simplicité utilisez [https://github.com/PierreQuinton/hermit_crab Hermit Crab] !\n'
    content+='===Références===\n'
    page='Bacasable'
    # write some content to page
    #wiki.writeToPage(content, page, summary='Calamarification')
    
    content='\n== Ngrams viewer ==\n'
    # append some extra content to the page
    #wiki.writeToPage(content, page, True, summary='Calamarification')
    
    # read the page, wow it's the same as wat we wrote !
    newContent=wiki.readPage(page)
    print(newContent + '\n\n')
    
    # search the titles
    print(wiki.find([page], [r"===.+===", r"==.+=="]))
    print('\n\n')

    # revert the titles of order 2 and 3
    print(wiki.replace(page, [r"===(.+)===", r"==(.+)=="], [r"==\1==", r"===\1==="], 'Calamarification')[1][0])

