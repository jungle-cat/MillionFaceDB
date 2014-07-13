'''
@date: 2014-7-8
@author: Feng
'''
from tools.crawler import google
import json, logging

if __name__ == '__main__':
    logging.basicConfig( level=logging.DEBUG,
                         format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')
    
    fn = 'data/name.txt'
    
    crawler = google.ImageCrawler()
    with open(fn, 'r') as f:
        for line in f:
            line = line.strip()
            results = crawler.query(line, 300)
            
            ofn = line.replace(' ', '_') + '.txt'
            with open('meta/'+ofn, 'w') as fo:
                for item in results:
                    js = json.dumps(item)
                    fo.write(js+'\n')
            print 'processed %s ...' % line
