all : scion.js spidermonkey.so

get-deps:
	git submodule init && git submodule update
	npm install git://github.com/jbeard4/stitch.git
	sudo apt-get install python-setuptools python2.7-dev pkg-config libnspr4-dev 
	if [ -n "`apt-cache search xulrunner-1.9.2-dev`" ]; then sudo apt-get install xulrunner-1.9.2-dev; fi	#not on some ubuntu systems

scion.js : get-deps
	node js-src/build/stitch.js

spidermonkey.so : get-deps
	cd lib/python-spidermonkey && python setup.py build
	mv `find -name spidermonkey.so` .

clean : 
	rm pyscion.js spidermonkey.so

.PHONY : clean get-deps all

