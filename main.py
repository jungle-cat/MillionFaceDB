'''
Created on 2014-6-12

@author: Feng
'''

from tools.crawler import google

if __name__ == '__main__':
    crawler = google.ImageCrawler()
    
    rets = crawler.query('yao ming', 200)
    for item in rets:
        print item 

