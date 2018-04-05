'''
Created on 05 apr 2018

@author: davideorlando
'''
import requests

import aiohttp
import src.FileManager as fileman
import asyncio
import async_timeout

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
    
    async def downloadPages(self, domain, urlsList):
        async with aiohttp.ClientSession() as session:
            destinationFolder = self.OUTPUT_FOLDER + "/" + domain
            self.fm.makeDir(destinationFolder)
            progressivo = 1
            fileDominio = open(destinationFolder+"/index.txt","w")
            for url in urlsList:
                if (await self.downloadPage(url, session, destinationFolder, progressivo,fileDominio)):
                    progressivo+=1
            fileDominio.close()

    async def downloadPage(self, url, session, destinationFolder, progressivo,fileDominio):
        async with async_timeout.timeout(10):
            async with session.get(url) as response:
                if (str(response.status)[0] =="2"):
                    fileForUrlSelected = open(destinationFolder+"/"+str(progressivo)+".html","w")
                    fileForUrlSelected.write(str((await response.text()).encode("utf-8")));
                    fileForUrlSelected.close();
                    fileDominio.write(url+"\t"+"./"+str(progressivo)+".html\n")
                    print("Inserito nel file:\n"+url+"\t"+"./"+str(progressivo)+".html\n")
                    return True
                else:
                    fileDominio.write(url+"\t"+str(response.status)+"\n")
                    print("Inserito nel file:\n"+url+"\t"+str(response.status)+"\n")
                    return False

