from xml.dom.minidom import parse, parseString
import urllib2
from os import path
from urlparse import urlparse
import sys

class ScionPlatformPathHelper(object):

    def join(self,p1,p2): 
        return path.join(p1,p2)

    def dirname(self,p): 
        return path.dirname(p)

    def basename(self,p): 
        return path.basename(p)

    def extname(self,p):
        return path.splitext(p)[1]

class ScionPlatformUrlHelper(object):

    def getPathFromUrl(url):
        #parse url
        urlObject = urlparse(url)

        #extract path
        return urlObject[2]

    def changeUrlPath(url,newPath):
        #parse url again
        urlObject = urlparse(url);

        urlObject[2] = newPath

        #create a new url, and return a string
        return urlObject.geturl()


class ScionPlatform(object): 

    def __init__(self,rt):
        self._rt = rt
        self.path = ScionPlatformPathHelper()
        self.url = ScionPlatformUrlHelper()

    def getDocumentFromUrl(self,url,cb):
        try: 
            s = urllib2.urlopen(url).read()
            self.parseDocumentFromString(s,cb)
        except:
            cb(sys.exc_info())
        
    def parseDocumentFromString(self,s,cb):
        try: 
            xml = parseString(s);
            cb(None,xml)
        except:
            cb(sys.exc_info())
            
    def getDocumentFromFilesystem(self,path,cb):
        try:
            f = open(path)
            s = f.read()
            self.parseDocumentFromString(s,cb)
        except:
            cb(sys.exc_info())

    def getResourceFromUrl(self,url,cb):
        #TODO: fix this: parse the url and stuff. look at the protocol. get the resource
        try: 
            s = urllib2.urlopen(url).read()
            cb(None,s)
        except:
            cb(sys.exc_info())

    def setTimeout(self,fn,timeout):
        pass

    def clearTimeout(timeoutId):
        pass

    def log(*args):
        print " ".join(map(lambda x : str(x),args[1:]))

    def eval(content,name):
        cx = self._rt.new_context()
        cx.execute(content)

