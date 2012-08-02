var stitch = require('stitch');
var fs = require('fs');
var path = require('path');

var pkg = stitch.createPackage({
    paths: [path.join('js-lib','scion','lib')],
    excludes : [
        path.join('js-lib','scion','lib','node'),
        path.join('js-lib','scion','lib','rhino'),
        path.join('js-lib','scion','lib','browser'),
        path.join('js-lib','scion','lib','external','jsUri','build')
    ]
});

pkg.compile(function (err, source){
    fs.writeFile('scion.js', source, function (err) {
        if (err) throw err;
        console.log('Compiled scion.js');
    });
});

