'''
Created on 2014-6-12

@author: Feng
'''

from tools.io.urlread import urlread
from bs4 import BeautifulSoup as bs

import urllib, urlparse, json, logging, re

class CallBackError(Exception):
    pass

class IterRets(object):
    '''
    Base class of iteratable returned results.
    '''
    
    def __iter__(self):
        return self
    
    def next(self):
        raise StopIteration
    

class ImageCrawler(object):
    '''
    Implementation of crawler from google image
    '''
    
    class ImageIterRets(IterRets):
        '''
        Implementation of iteratable results of image searching.
        '''
        
        def __init__(self, crawler, maxlen=None):
            self.caches = []
            self.count = 0
            self.host = crawler.hosts[0]
            self.urlparams = crawler.urlparams.copy()
            self.maxlen = maxlen
            
        def __iter__(self):
            return self
        
        def next(self):
            if self.maxlen and self.count > self.maxlen:
                raise StopIteration
            if not self.caches:
                rets = self.get(int(self.count / 100))
                if not rets:
                    raise StopIteration
                else:
                    self.caches.extend(rets)
            
            self.count += 1
            return self.caches.pop()
        
        def get(self, num):
            ureader = urlread()

            is_first = True
            if self.count:
                self.urlparams['ijn'] = num
                self.urlparams['start'] = num*100
                is_first = False
                
            url = '%s/search?%s' % (self.host, urllib.urlencode(self.urlparams))
            content = ureader.read(url)
            rets = self.parse(content, is_first)
            
            eid = is_first and self.parseEID(content)
            if eid:
                self.urlparams['ei'] = eid
            
            self.count += 1
            return rets
            
        def parse(self, data, first = None):
            infolist = []
            try:
                parser = bs(data)
                p = parser.select('.rg_di')
                if first and len(p) > 100:
                    p = p[-100:]
                for item in p:
                    urlinfo = dict(urlparse.parse_qsl(urlparse.urlparse(item.a['href']).query))
                    metainfo = json.loads(item.contents[1].text)
                    
                    info = {}
                    info['imgurl'] = urlinfo['imgurl']
                    info['imgrefurl'] = urlinfo['imgrefurl']
                    info['w'] = urlinfo['w']
                    info['h'] = urlinfo['h']
                    info['type'] = metainfo['ity']
                    info['tw'] = metainfo['tw']
                    info['th'] = metainfo['th']
                    info['turl'] = metainfo['tu']
                    info['fn'] = metainfo['fn']
                    
                    infolist.append(info)
            except Exception, e:
                logging.warn(e)
            return infolist
        
        def parseEID(self, data):
            m = re.search(r'kEI:".*?"', data)
            if m:
                s = m.group()
                eid = s[5:-1]
            else:
                eid = ''
            return eid
                    
    
    def __init__(self, hosts=None, proxy=None):
        '''
        Constructor
        '''
        if not hosts:
            self.hosts = ['https://www.google.com.sg']
        else:
            self.hosts = hosts
            
        self.urlparams = {
           # 'sout': '1',
            'tbm': 'isch'}
    
    def query(self, q, maxlen=None):
        if not q:
            return None
        self.urlparams['q'] = q
        return self.ImageIterRets(self, maxlen)