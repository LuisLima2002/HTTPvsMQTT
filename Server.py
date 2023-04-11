import cherrypy
import paho.mqtt.client as mqtt
from os.path import abspath

class Index(object):
    broker_address = "127.0.0.1"
    def __init__(self):    
        self.mqttUsage="None"
        self.httpUsage="None"
        self.client = mqtt.Client("subscriber")
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address, keepalive=60000)
        self.client.subscribe("mem/usage17")
        
    def on_message(self,client, userdata, message):
        self.mqttUsage=message.payload.decode()

    @cherrypy.expose
    def index(self):
        return open("media/index.html")

    @cherrypy.expose
    def saveMemUsage(self,**args):
        self.client.loop_read()
        self.httpUsage= args["usage"]
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getMemUsage(self,):
        return {"mqtt":self.mqttUsage,"http":self.httpUsage}

if __name__ == '__main__':
    conf = { '/':{
            'tools.staticdir.on': True,
            'tools.staticdir.dir': abspath('./media') # staticdir needs an absolute path
            }
    }
    cherrypy.quickstart(Index(), '/', conf)