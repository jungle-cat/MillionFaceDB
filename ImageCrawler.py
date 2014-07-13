'''
Created on 2014-7-12

@author: Feng
'''

from tools.io.urlread import urlread
import logging, os, json, gevent

def downloader(url, name):
    ur = urlread()
    if not ur.retrieve(url, name):
        logging.error('DownloaderError: url: %s, name: %s' % (url, name))


if __name__ == '__main__':
    logging.basicConfig(filename='craw.log',
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    
    
    metadir = 'meta'
    imgdir = 'images'
    
    metafiles = os.listdir(metadir)
    
    # load image metadata 
    threads = []
    for metafile in metafiles:
        with open(os.path.join(metadir, metafile),'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    info = json.loads(line)
                    
                    url = info['imgurl']
                    type = info['type']
                    id = info['id']
                    
                    name = '%04d.%s' % (id, type)
                    name = os.path.join(imgdir, name)
                    
                    threads.append(gevent.spawn(downloader, url, name))
    
    gevent.joinall(threads)
    