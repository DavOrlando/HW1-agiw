'''
Created on 05 apr 2018

@author: davideorlando
'''
import json


class FileParser(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def getDictFromJSONFile(self, path):
        domain2listUrl = {}
        try:
            fileURL = open(path, "r")
            domain2listUrl = json.loads(fileURL.read())
            print("Mappa dominio e lista URL di quel dominio creata correttamente")
            fileURL.close()
            return domain2listUrl
        except:
            return domain2listUrl    