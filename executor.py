# -*- coding: utf-8 -*-

from wiki import Wiki
import time

""" Parse and execute bot code """
class Executor:

    def __init__(self, superBot, page, code):
        """
        :param superBot: super bot who makes the modifications ( type Wiki )
        :param page : page of the bot to execute
        :param code: code of the bot to parse and execute
        """
        self.superBot = superBot;
        self.code = code;

    def run(self):
        #get list of functions
        #for f in list:
        #try:
        #executeFunction()
        #except NameError as e
        #writeConsole()
            

    def executeFunction(self,name,code):
        if (name == 'Replace Words'):
            replaceWords(code)
        else:
            raise NameError('Unknown function' + name)
        

    def replaceWords(self,code):
        """
        Parse and execute the code for function replaceWords
        :param code: code of the function to parse and execute
        """
        print('cool');

    def writeConsole(self,message):
        """
        Write output to the console
        :param code: code of the function to parse and execute
        """
        date = time.strftime("%d/%m/%Y")
        h = time.strftime("%H:%M:%S")
        content = '\n* ' + date + ' ' + h + ' : ' + message
        wiki.writeToPage(content,page,True,summary = 'Output to console')
