from SCXML import pathToModel,createInterpreter

model = pathToModel("test/basic1.scxml")

interpreter = createInterpreter(model)

initialConf = interpreter.start()
print initialConf 

nextConf = interpreter.gen("t")
print nextConf 
