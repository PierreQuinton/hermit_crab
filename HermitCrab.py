# -*- coding: utf-8 -*-

from wiki import Wiki

if __name__ == '__main__':
    masterBot = 'Utilisateur:Hermit Crab'
    
    wiki = Wiki('Hermit Crab', 'poulpe')
    masterPage = wiki.readPage(masterBot)
    #Retrieve workers in main page
    print(masterPage)
    
    #Convert the content to a list
    #workers = list of workers
    '''
    #Access to all worker pages
    for w in workers:
        code = wiki.readPage(w)
        #Execute them'''

