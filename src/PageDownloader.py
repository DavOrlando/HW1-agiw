'''
Created on 05 apr 2018

@author: davideorlando
'''
import src.FileManager as fileman
import concurrent.futures
import requests
import asyncio
import os
import shutil
import json
from src.FileParser import FileParser
class PageDownloader(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.fm = fileman.FileManager()

    


    def refreshIndexWithSuccess(self, fileDominio, progressivo, response):
        fileDominio.write(response.url + "\t" + "./" + str(progressivo) + ".html\n")
        print("Scaricato:" + response.url + " dentro " + "./" + str(progressivo) + ".html")

    def saveHtmlTo(self, destinationFolder, progressivo, response):
        fileForUrlSelected = open(destinationFolder + "/" + str(progressivo) + ".html", "w", encoding="utf8")
        fileForUrlSelected.write(response.text)
        fileForUrlSelected.close()
        
    def refreshIndexWithErrorCode(self, fileDominio, response):
        fileDominio.write(response.url + "\t" + str(response.status_code) + "\n")
        print(response.url + "\t" + str(response.status_code))


    def refreshIndexWithRedirectError(self, fileDominio, response):
        fileDominio.write(response.url + "\tredirect\n")
        print(response.url + "\t redirect")

    async def startAsyncDownload(self, loop,category,dominio2URLS):
        dominiConTimeout= FileParser().getDictFromJSONFile("../monitor/listaTimeout.json")
        def doReq(url):
            return requests.get(url,timeout=10)
        self.prepareFolder("../"+category)
        with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
            for dominio in dominio2URLS.keys():
                destinationFolder = self.OUTPUT_FOLDER + "/" + dominio
                if(os.path.exists(destinationFolder)==True):
                    continue;
                self.fm.makeDir(destinationFolder)
                fileDominio = open(destinationFolder+"/index.txt","w")
                urls = dominio2URLS[dominio]       
                futures = [
                    loop.run_in_executor(
                        executor, 
                        doReq, 
                        urls[i]
                    )
                    for i in range(0,len(urls))
                ]
                progressivo = 1;
                    
                try:
                    for response in await asyncio.gather(*futures):
                        if(str(response.status_code)[0] == "2"):
                            self.saveHtmlTo(destinationFolder, progressivo, response)
                            self.refreshIndexWithSuccess(fileDominio, progressivo, response)
                            progressivo+=1;
                        else:
                            if(str(response.status_code)[0] == "4"):
                                self.refreshIndexWithErrorCode(fileDominio, response)
                            else: 
                                self.refreshIndexWithRedirectError(fileDominio, response)
                    fileDominio.close()
                except requests.exceptions.Timeout:
                    fileDominio.close()
                    dominiConTimeout[dominio]=dominio2URLS[dominio]
                    with open("../monitor/listaTimeout.json", 'w') as outfile:
                        json.dump(dominiConTimeout, outfile)
                    shutil.rmtree(destinationFolder);
                    print("Eccezione di timeout")
                except:
                    fileDominio.close()
                    shutil.rmtree(destinationFolder);
                    print("Eccezione di connessione")   
                    
    
    def prepareFolder(self, path):
        self.OUTPUT_FOLDER = path;
        self.fm.makeDir(path)
    
