get-deps:
	git submodule init && git submodule update
	npm install git://github.com/jbeard4/stitch.git
	sudo apt-get install python-setuptools python2.7-dev pkg-config libnspr4-dev xulrunner-1.9.2-dev 

scion.js : get-deps
	node js-src/build/stitch.js

spidermonkey.so :
	cd lib/python-spidermonkey && python setup.py build
	mv lib/python-spidermonkey/spidermonkey.so .

clean : 
	rm pyscion.js

.PHONY : clean get-deps

