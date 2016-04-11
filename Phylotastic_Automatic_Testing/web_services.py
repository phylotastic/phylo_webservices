import cherrypy
  
class HelloWorld(object):
    def index(self):
        return "Hello World!"
    def testFail(self):
        return "It fails"
    index.exposed = True
    testFail.exposed = True

cherrypy.quickstart(HelloWorld())