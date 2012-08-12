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

class ScionPlatformDomHelper(object):

    #these first two methods return JavaScript arrays, and so are done in JavaScript

    #def getChildren(self,node):
    #    return node.childNodes

    #def getElementChildren(self,node):
    #    return [child for child in node.childNodes if child.nodeType is 1]

    def localName(self,node):
        return node.localName

    def getAttribute(self,node,attribute):
        return node.getAttribute(attribute)  

    def hasAttribute(self,node,attribute):
        return node.hasAttribute(attribute)

    def namespaceURI(self,node):
        return node.namespaceURI

    def createElementNS(self,doc,ns,localName):
        return doc.createElementNS(ns,localName)

    def setAttribute(self,node,name,value):
        return node.setAttribute(name,value)

    def appendChild(self,parent,child):
        return parent.appendChild(child)

    def textContent(self,node,txt=None):
        if txt is None:
            if node.nodeType is 1:
                #element
                return "".join([child.data for child in node.childNodes if child.nodeType is 3])
            elif node.nodeType is 3:
                #textnode
                return node.data;
            else:
                return ""
        else:
            if node.nodeType is 1:
                #clear out existing child nodes
                for child in node.childNodes: node.removeChild(child)

                tn = node.ownerDocument.createTextNode(txt)
                node.appendChild(tn)
                return txt;
            elif node.nodeType is 3:
                #textnode
                node.data = txt
                return txt


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
        self.dom = ScionPlatformDomHelper()

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

