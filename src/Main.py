'''
Created on 05 apr 2018

@author: davideorlando
'''

import src.FileParser as filepars
import src.PageDownloader as pagedown
import src.FileManager as fm
import asyncio
import concurrent.futures
import requests


async def main():
    parser = filepars.FileParser()
    pageDownloader = pagedown.PageDownloader();
    pageDownloader.prepareFolder("../monitor")
    fileman = fm.FileManager()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        dominio2URLS = parser.getDominio2UrlsFromJSONFile("../resources/urls.json")
        loop = asyncio.get_event_loop()
        for dominio in dominio2URLS.keys():
            fileman.makeDir(pageDownloader.OUTPUT_FOLDER + "/" + dominio)
            fileDominio = open(pageDownloader.OUTPUT_FOLDER + "/" + dominio+"/index.txt","w")
            urls = dominio2URLS[dominio];
            futures = [
                loop.run_in_executor(
                    executor, 
                    requests.get, 
                    urls[i]
                )
                for i in range(0,len(urls))
            ]
            progressivo = 1;
            for response in await asyncio.gather(*futures):
                if(str(response.status_code)[0] == "2" and response.url in urls):
                    fileForUrlSelected = open(pageDownloader.OUTPUT_FOLDER + "/" + dominio+"/"+str(progressivo)+".html","w",encoding = "utf8")
                    fileForUrlSelected.write(response.text);
                    fileForUrlSelected.close();
                    fileDominio.write(response.url+"\t"+"./"+str(progressivo)+".html\n")
                    print("Inserito nel file:\n"+response.url+"\t"+"./"+str(progressivo)+".html\n")
                    progressivo+=1;
                else:
                    if(str(response.status_code)[0] == "4"):
                        fileDominio.write(response.url+"\t"+str(response.status_code)+"\n")
                        print("Inserito nel file:\n"+response.url+"\t"+str(response.status_code))
                    else: 
                        fileDominio.write(response.url+"\tredirect\n")
                        print("Inserito nel file:\n"+response.url+"\t redirect")
            fileDominio.close()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
