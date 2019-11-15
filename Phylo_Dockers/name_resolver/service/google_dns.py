import requests
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import re

#------------------------------------------------------
def ip_address_matcher(text):
	ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";
	ip = re.compile(ValidIpAddressRegex)
	#ip = re.compile('(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}'+'(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))')

	match = ip.search(text)
	if match:
 		#print 'IP address found:',
 		#print match.group(), # matching substring
 		#print 'at position',match.span() # indexes of the substring found
		return True
	else:
 		#print 'IP address not found'
		return False
	

#---------------------------------------------------------
def get_ip_address(service_root): 
	ip_address = None
	print "Using alternate DNS for %s"%service_root
	dns_url = "https://dns.google.com/resolve"
	payload = {'name': service_root}
	
	resp = requests.get(dns_url, params=payload)
	if resp.status_code == requests.codes.ok:
		json_resp = json.loads(resp.text)
		answers = json_resp['Answer']
		for ans in answers:
			ans_data = ans['data']
			if ip_address_matcher(ans_data):
	 			ip_address = ans_data
				break
	
	return ip_address

#-----------------------------------------------
def alt_service_url(service_url):
	#Suppress warning for using a version of Requests which vendors urllib3 inside
	#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	#+++++++++++++++
	slash_pos = [pos for pos, char in enumerate(service_url) if char == '/']
	#curl -X POST https://api.opentreeoflife.org/v2/tnrsmatch_names -H "content-type:application/json" -d '{"names": ["Aster"]}'
	#extract the service root "api.opentreeoflife.org" from the service url
	service_root = service_url[slash_pos[1]+1: slash_pos[2]]

	ip_address = get_ip_address(service_root)

	alt_api_url = service_url[:slash_pos[1]+1] + ip_address + service_url[slash_pos[2]: ]

	#resp = requests.post(api_url, data=json.dumps(service_payload), headers={'Content-Type': "application/json"}, verify=False)
 	return alt_api_url

#=====================================
#if __name__ == '__main__':
	#alt_url = alt_service_url("https://api.opentreeoflife.org/v2/tnrs/match_names")
	#print alt_url
	#service_payload = {'names': ["Aster"]}
	#resp = requests.post(alt_url, data=json.dumps(service_payload), headers={'Content-Type': "application/json"}, verify=False)
	#print resp.text
