'''
Created on 05 apr 2018

@author: davideorlando
'''
import os


class FileManager(object):
    '''
    Una classe che organizza i file 
    '''

    OUTPUT_FOLDER = "../output"

    def __init__(self):
        '''
        Constructor
        '''
    
    
        
    def makeDir(self, path):
        '''
        Crea una cartella nel path specificato
        '''
        if(os.path.exists(path)==False):
            os.mkdir(path);
        print("Cartella creata: " + path)
        
    
    
        
