'''
Created on 05 apr 2018

@author: davideorlando
'''
import requests

import src.FileManager as fileman

class PageDownloader(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.fm = fileman.FileManager()
    
    def prepareFolder(self, path):
        self.OUTPUT_FOLDER = path;
        self.fm.makeDir(path)
    
    def downloadPages(self, domain, urlsList):
            destinationFolder = self.OUTPUT_FOLDER + "/" + domain
            self.fm.makeDir(destinationFolder)
            progressivo = 1
            fileDominio = open(destinationFolder+"/index.txt","w")
            for url in urlsList:
                if (self.downloadPage(url, destinationFolder, progressivo,fileDominio)):
                    progressivo+=1
            fileDominio.close()

    def downloadPage(self, url, destinationFolder, progressivo,fileDominio):
        response = requests.get(url)
        if (str(response.status_code)[0] =="2"):
            fileForUrlSelected = open(destinationFolder+"/"+str(progressivo)+".html","w",encoding = "utf8")
            fileForUrlSelected.write(response.text);
            fileForUrlSelected.close();
            fileDominio.write(url+"\t"+"./"+str(progressivo)+".html\n")
            print("Inserito nel file:\n"+url+"\t"+"./"+str(progressivo)+".html\n")
            return True
        else:
            fileDominio.write(url+"\t"+str(response.status_code)+"\n")
            print("Inserito nel file:\n"+url+"\t"+str(response.status_code)+"\n")
            return False

