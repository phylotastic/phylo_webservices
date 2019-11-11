import requests
import re
import urllib2
from urllib2 import urlopen

#------------------------------------------------------
def is_http_url(url):
    """
    Returns true if url is valid http url, else false 
    """
	#Ref: http://urlregex.com/
    if re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',url):
        return True
    else:
        return False
 
#---------------------------------------------------------
def does_url_exist(url):
	try:
		code = urlopen(url).code
	except urllib2.URLError:
		return False
	if (code == 200):
		return True
	else:
		print False

#=====================================
#if __name__ == '__main__':
	#print does_url_exist("https://www.google.com")
	#print does_url_exist("http://notexist.example.com")

