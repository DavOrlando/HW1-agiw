'''
Created on 05 apr 2018

@author: davideorlando
'''

import src.FileParser as filepars
import src.PageDownloader as pagedown
import asyncio
import concurrent.futures

if __name__ == '__main__':
    parser = filepars.FileParser()
    pageDownloader = pagedown.PageDownloader();
    pageDownloader.prepareFolder("../monitor")
    #Creazione mappa dominio e lista URL di quel dominio
    dominio2URLS = parser.getDominio2UrlsFromJSONFile("../resources/urls.json")
    for dominio in dominio2URLS.keys():
        pageDownloader.downloadPages(dominio, dominio2URLS[dominio])
    