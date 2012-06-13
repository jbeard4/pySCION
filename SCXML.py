import spidermonkey
from xml.dom.minidom import parse, parseString
import urllib2

#create a new context
rt = spidermonkey.Runtime()
cx = rt.new_context()

#load up es5-shim (old version of spidermonkey lacks some APIs)
es5js = open("js-lib/es5-shim/es5-shim.js")
es5jsStr = es5js.read() 
cx.execute(es5jsStr) 
es5js.close() 

#load up SCION
scionjs = open("scion.js")
scionJsStr = scionjs.read()
cx.execute(scionJsStr)  
scionjs.close()

#expose the js API here
modelFactory = cx.execute("""
    (function(){
        JsonML = require('external/jsonml/jsonml-dom'),
        annotator = require('core/util/annotate-scxml-json'),
        json2model = require('core/scxml/json2model');
 
        return function(doc){
            //do the steps here to construct a model from a DOM object
            //should look pretty similar to the other adapters (node, rhino, browser)

            var arr = JsonML.parseDOM(doc);
            var scxmlJson = arr[1];

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

def urlToModel(url):
    s = urllib2.urlopen(url).read()
    return documentStringToModel(s)

def pathToModel(path):
    f = open(path)
    dom = parse(f)
    f.close()
    return documentToModel(dom)

def documentStringToModel(scxmlDocString):
    dom = parseString(scxmlDocString)
    return documentToModel(dom)

def documentToModel(dom):
    return modelFactory(dom)

class SCXML:

    def __init__(self,model):
        #construct
        self.interpreter = interpreterFactory(model)  

    def start():
        return self.interpreter.start()

    def gen(event,data):
        return self.interpreter.gen(event,data)
