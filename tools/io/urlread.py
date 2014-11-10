'''
@date: 2014-7-6
@author: Feng
'''

import urllib2, logging, time

class urlread(object):
    def __init__(self, headers={}, maxtry=2, interval=2, proxy=None):
        self.headers = headers
        if not headers.has_key('User-Agent'):
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'
        self.maxtry = maxtry
        self.interval = interval
        self.proxy = proxy
    
    def read(self, url, headers=None):
        if headers:
            headers = dict(self.headers, **headers)
        request = urllib2.Request(url, headers=self.headers)

        n = 0
        content = ''
        while n < self.maxtry:
            try:
                n += 1
                page = urllib2.urlopen(request)
                content = page.read()
                failure = False
            except urllib2.HTTPError, e:
                logging.error('HTTPError: %s %s with url: %s' % (e.code, e.message, url))
                failure = True
            except Exception, e:
                logging.error('FatalError: %s %s with url: %s' % (e.code, e.message, url))
                failure = True
            finally:
                page.close()
                if n <= self.maxtry and failure: 
                    time.sleep(self.interval)
                else:
                    break
        return content
    
    def retrieve(self, url, name, headers=None):
        headers = headers and self.headers or dict(self.headers, **headers)
        request = urllib2.Request(url, headers=headers)
         
        n = 0
        content = ''
        while n < self.maxtry:
            try:
                n += 1
                page = urllib2.urlopen(request)
                content = page.read()
                failure = False
            except urllib2.HTTPError, e:
                logging.error('HTTPError: %s %s with url: %s' % (e.code, e.message, url))
                failure = True
            except Exception, e:
                logging.error('FatalError: %s %s with url: %s' % (e.code, e.message, url))
                failure = True
            finally:
                if n <= self.maxtry and failure: 
                    time.sleep(self.interval)
                else:
                    break
        if not failure:
            with open(name, 'wb') as f:
                f.write(content)
        return not failure