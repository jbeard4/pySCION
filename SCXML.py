from __future__ import print_function
import spidermonkey
import urllib2
import os
from StringIO import StringIO
from platform import ScionPlatform

#create a new context
rt = spidermonkey.Runtime()
cx = rt.new_context()

cx.add_global("print", print )   #expose a global print function to the spidermonkey context

cwd = os.path.dirname(__file__)

#load up es5-shim (old version of spidermonkey lacks some APIs)
es5js = open(os.path.join(cwd,"js-lib/es5-shim/es5-shim.js"))
es5jsStr = es5js.read() 
cx.execute(es5jsStr) 
es5js.close() 

#same for json2.js
json2js = open(os.path.join(cwd,"js-lib/json/json2.js"))
json2Str = json2js.read() 
cx.execute(json2Str) 
es5js.close() 

#load up SCION
scionjs = open(os.path.join(cwd,"scion.js"))
scionJsStr = scionjs.read()
cx.execute(scionJsStr)  
scionjs.close()

#TODO: pass in as a function argument, rather than exposing a global
pythonPlatform = ScionPlatform(rt)
cx.add_global("pythonPlatform", pythonPlatform )

#TODO: tomorrow: update scion with changes. check in. 
#consider using a synchronous api instead of an async one. not sure if this is possible...
#write up some documentation, email the list....
#bindings for seed, qt, and boost.
#try to build on windows...

#expose the js API here
[urlToModel,pathToModel,documentStringToModel,createInterpreter] = cx.execute("""
    //define a new platform object
    var scion = require('scion');
    scion.ext.platformModule.platform = pythonPlatform; 

    //these two dom helper functions need to be implemented in js, because they must return js arrays,
    //which currently can't be done from Python
    scion.ext.platformModule.platform.dom.getChildren = function(node){
        var r = [];
        for(var i = 0; i < node.childNodes.length; i++){
            r.push(node.childNodes[i]);
        }
        return r;
    }

    scion.ext.platformModule.platform.dom.getElementChildren = function(node){
        return this.getChildren(node).filter(function(n){return n.nodeType === 1;});
    }

    //wrap these functions up in synchronous apis
    function urlToModel(url){
        var err, model;
        scion.urlToModel(url,function(e,m){
            err = e;
            model = m;
        });
        if(err) throw err;
        return model;
    }

    function pathToModel(path){
        var err, model;
        scion.pathToModel(path,function(e,m){
            err = e;
            model = m;
        });
        if(err) throw err;
        return model;
    }

    function documentStringToModel(s){
        var err, model;
        scion.documentStringToModel(s,function(e,m){
            err = e;
            model = m;
        }); 
        if(err) throw err;
        return model;
    }

    //regular function wrapper around the constructor function, 
    //as this is not supported in python-spidermonkey
    function createInterpreter(model){
        return new scion.SCXML(model);
    }

    [urlToModel,pathToModel,documentStringToModel,createInterpreter];
""")

