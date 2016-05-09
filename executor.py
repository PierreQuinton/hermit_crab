# -*- coding: utf-8 -*-

from wiki import Wiki
import time

""" Parse and execute bot code """
class Executor:

    def __init__(self, superBot, bots):
        """
        :param superBot: super bot who makes the modifications ( type Wiki )
        :param bots : list of bot to execute
        """
        self.superBot = superBot;
        self.bots = bots;

    def run(self):
        error = 0
        for b in self.bots:
            for f in b.getFunctions():
                try:
                    self.writeConsole(b.name,self.executeFunction(f,b.getFunction(f)))
                except NameError as e:
                    error += 1
                    self.writeConsole(b.name,str(e))
            if error == 0:
                self.writeConsole(self.superBot.user,'[[{}]] executed : SUCCESS'.format(b.name))
            else:
                self.writeConsole(self.superBot.user,'[[{}]] executed : FAILURE'.format(b.name))
            error = 0
                    

    def executeFunction(self,name,code):
        if (name == 'Replace Words'):
            return self.replaceWords(code)
        else:
            raise NameError('Unknown function : ' + name)
        

    def replaceWords(self,code):
        """
        Parse and execute the code for function replaceWords
        :param code: code of the function to parse and execute
        """
        dic = {}
        if ('replace' in code.keys()):
            for c in code['replace']:
                couple = c.split('->')
                if len(couple) == 2:
                    dic[couple[0].strip()] = couple[1].strip()
                else:
                    raise NameError('Replace section of [[Replace Words]] should be of the format aa -> bb')
        else:
            raise NameError('Keyword "replace" is not in [[Replace Words]] !')

        pages = []
        
        if ('in' in code.keys()):
            for page in code['in']:
                pages.append(page[2:len(page)-2])
        else:
            raise NameError('Keyword "in" is not in [[Replace Words]] !')

        summary = ''

        if ('summary' in code.keys()):
            summary = code['summary'][0]
        else:
            raise NameError('Keyword "summary" is not in [[Replace Words]] !')

        self.superBot.replaceWords(pages,dic,summary)
        pa = list(map(lambda x:('[[{}]]').format(x),pages))
        return ('Words {} in {} replaced ! Summary : {}'.format(dic,pa,summary))

    def writeConsole(self,name,message):
        """
        Write output to the console
        :param name: name of the bot
        :param message: message to write
        """
        date = time.strftime("%d/%m/%Y")
        h = time.strftime("%H:%M:%S")
        content = '\n* ' + date + ' ' + h + ' : ' + str(message)
        self.superBot.writeToPage(content,name,True,summary = 'Output to console')
