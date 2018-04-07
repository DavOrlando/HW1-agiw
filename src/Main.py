'''
Created on 05 apr 2018

@author: davideorlando
'''

import src.PageDownloader as pagedown
import asyncio
import src.FileParser as filepars


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    
    pageDownloader=pagedown.PageDownloader()
    parser = filepars.FileParser()
    dominio2URLS = parser.getDictFromJSONFile("../resources/urls.json")
    print(len(dominio2URLS.keys()))
    loop.run_until_complete(pageDownloader.startAsyncDownload(loop,"monitor",dominio2URLS))

