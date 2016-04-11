def testWebService():
   import urllib2
   wsResult = urllib2.urlopen("http://127.0.0.1:8080/index").read()
   if (wsResult == "Hello World!"):
       print "Pass"
       exit(0)
   if (wsResult == "It fails"):
       print "Fail"
       exit(1)
def testNormal(flag):
   if (flag == "PASS"):
       print "PASS"
       exit(0)
   if (flag == "FAIL"):
       print "FAIL"
       exit(1)
#testWebService();
testNormal("PASS")
