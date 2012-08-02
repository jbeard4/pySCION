from scion.SCXML import urlToModel,createInterpreter
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import json
import sys
import traceback
import pdb

sessionCounter = 0
sessions = {}
timeouts = {}
timeoutMs = 5000

class SCIONTestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        global sessionCounter, sessions, timeouts, timeoutMs

        try: 
            s = self.rfile.read(int(self.headers['Content-Length']))
            reqJson = json.loads(s)

            if reqJson.has_key("load"):
                print "Loading new statechart"

                model = urlToModel(reqJson["load"].encode("utf8"))

                interpreter = createInterpreter(model)

                sessionToken = sessionCounter
                sessionCounter = sessionCounter + 1
                sessions[sessionToken] = interpreter 

                conf = interpreter.start() 

                self.send_response(200)
                self.end_headers()

                json.dump({
                    "sessionToken" : sessionToken,
                    "nextConfiguration" : list(conf)
                },self.wfile)
                self.wfile.close()

                #TODO: deal with timeouts
                #timeouts[sessionToken] = setTimeout(function(){cleanUp(sessionToken)},timeoutMs)  

            elif reqJson.has_key("event") and reqJson.has_key("sessionToken") and  type(reqJson["sessionToken"]) is int:
                print "sending event to statechart",reqJson["event"]
                sessionToken = reqJson["sessionToken"]
                nextConfiguration = sessions[sessionToken].gen(reqJson["event"])
                print 'nextConfiguration',nextConfiguration

                self.send_response(200)
                self.end_headers()
                json.dump({ "nextConfiguration" : list(nextConfiguration) },self.wfile)
                self.wfile.close()

                #TODO: deal with timeouts
                #clearTimeout(timeouts[sessionToken])
                #timeouts[sessionToken] = setTimeout(function(){cleanUp(sessionToken)},timeoutMs)  
            else:
                #unrecognized. send back an error
                self.send_response(400)
                self.end_headers()
                self.wfile.write("Unrecognized request.")
                self.wfile.close()
        except:
            e = sys.exc_info()[0]
            print "Unexpected error:", e
            print sys.exc_info()
            traceback.print_tb(sys.exc_info()[2],file=sys.stdout)

            self.send_response(500)
            self.end_headers()
            self.wfile.write(e)
            self.wfile.close()

server_address = ('', 42000)
httpd = HTTPServer(server_address, SCIONTestHandler)
httpd.serve_forever()
