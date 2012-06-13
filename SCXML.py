import spidermonkey
from lxml import etree
import urllib2
import pdb

#create a new context
rt = spidermonkey.Runtime()
cx = rt.new_context()

#load up es5-shim (old version of spidermonkey lacks some APIs)
es5js = open("js-lib/es5-shim/es5-shim.js")
es5jsStr = es5js.read() 
cx.execute(es5jsStr) 
es5js.close() 

#same for json2.js
json2js = open("js-lib/json/json2.js")
json2Str = json2js.read() 
cx.execute(json2Str) 
es5js.close() 

#load up SCION
scionjs = open("scion.js")
scionJsStr = scionjs.read()
cx.execute(scionJsStr)  
scionjs.close()

#expose the js API here
modelFactory = cx.execute("""
    (function(){
        var annotator = require('core/util/annotate-scxml-json'),
            json2model = require('core/scxml/json2model');
 
        return function(scxmlJsonString){
            //do the steps here to construct a model from a DOM object
            //should look pretty similar to the other adapters (node, rhino, browser)

            var scxmlJson = JSON.parse(scxmlJsonString);

            var annotatedScxmlJson = annotator.transform(scxmlJson);

            var model = json2model(annotatedScxmlJson); 

            return model;
        };
    })();
""")

interpreterFactory = cx.execute("""
    (function(){
        var scxml = require('core/scxml/SCXML');

        return function(model){
            return new scxml.SimpleInterpreter(model);
        };
    })();
""")

jsonMLTransform = etree.XSLT(etree.parse(open("lib/jsonml/jsonml.xslt")))

def urlToModel(url):
    s = urllib2.urlopen(url).read()
    return documentStringToModel(s)

def pathToModel(path):
    return documentToModel(etree.parse(open(path)))

def documentStringToModel(scxmlDocString):
    return documentToModel(etree.parse(StringIO(scxmlDocString)))

def documentToModel(scxmlDoc):
    result = jsonMLTransform(scxmlDoc)
    #pdb.set_trace()
    return modelFactory(str(result))

class SCXML:

    def __init__(self,model):
        #construct
        self.interpreter = interpreterFactory(model)  

    def start(self):
        return self.interpreter.start()

    def gen(self,event,data={}):
        return self.interpreter.gen(event,data)
