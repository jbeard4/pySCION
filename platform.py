from xml.dom.minidom import parse, parseString
import urllib2
from os import path
from urlparse import urlparse,urlunparse
import sys
from threading import Timer

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

    def getPathFromUrl(self,url):
        #parse url
        urlObject = urlparse(url)

        #extract path
        return urlObject[2]

    def changeUrlPath(self,url,newPath):
        #parse url again
        urlObject = list(urlparse(url));
        print('urlObject',urlObject)

        urlObject[2] = newPath
        print('urlObject',urlObject)

        #create a new url, and return a string
        return urlunparse(urlObject)

#FIXME: this class is just a quick-and-dirty solution to add setTimeout behaviour to SCION
#really should function with a synchronized queue. will add this later.
class ScionPlatformTimeoutManager(object):

    def __init__(self):
        self._timerMap = {}
        self._timerCount = 0

    def setTimeout(self,cb,dur):
        t = Timer(float(dur)/1000, cb)

        self._timerCount = self._timerCount + 1
        timerHandle = self._timerCount
        self._timerMap[timerHandle] = t

        t.start()

        return timerHandle 

    def clearTimeout(self,handle):
        if self._timerMap.hasKey(handle):
            t = self._timerMap[handle]
            t.cancel()

            del self._timerMap[handle]

class ScionPlatform(object): 

    def __init__(self,rt):
        self._rt = rt
        self.path = ScionPlatformPathHelper()
        self.url = ScionPlatformUrlHelper()

        scionPlatformTimeoutManager = ScionPlatformTimeoutManager()
        self.setTimeout = scionPlatformTimeoutManager.setTimeout 
        self.clearTimeout = scionPlatformTimeoutManager.clearTimeout 

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
            f.close()
            self.parseDocumentFromString(s,cb)
        except:
            cb(sys.exc_info())

    def getResourceFromUrl(self,url,cb):
        #TODO: fix this: parse the url and stuff. look at the protocol. get the resource
        try: 
            urlObject = urlparse(url)
            scheme = urlObject[0]
            path = urlObject[2]
            if scheme == "http":
                #http url
                s = urllib2.urlopen(url).read()
                cb(None,s)
            elif path and not scheme: 
                f = open(path)
                s = f.read()
                f.close()
                cb(None,s)
            else:
                #pass through an exception: not supported
                cb(Exception("Unable to handle URL",url))
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

