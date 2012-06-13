from SCXML import pathToModel,SCXML

m = pathToModel("test/basic1.scxml")
print m

interpreter = SCXML(m)
print interpreter 

initialConf = interpreter.start()
print initialConf 

nextConf = interpreter.gen("t")
print nextConf 
