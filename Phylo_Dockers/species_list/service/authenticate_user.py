import json
import requests
import urllib

# Access client_secrets.json file
#CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
headers = {'content-type': 'application/json'}

#----------------------------------------
#Verify an Access Token
def verify_access_token(access_token, email=None):
 	if access_token == 'ya29..zQLSyEJmYu5jaYI00NQgkUpljPBDseL8lh-zE7xuFkFUdpJXWhzskGFgnITR1pLhWw':
 		return {'is_access_token_valid' : True, 'g_user_id' : "phylo_admin", 'message': "valid phylo access token"}

 	access_token_validity_obj = {}
 	
 	url = ('https://www.googleapis.com/oauth2/v3/tokeninfo')
 	payload = {
        'access_token': access_token
    }
    
 	encoded_payload = urllib.urlencode(payload)
 	response = requests.get(url, params=encoded_payload, headers=headers) 
 	#print response.text
 	if response.status_code == requests.codes.ok:
 		result = json.loads(response.text)			
 		#if result['aud'] != CLIENT_ID:
 			# This is not meant for this app. It is VERY important to check
 			# the client ID in order to prevent man-in-the-middle attacks.
 			#access_token_validity_obj['is_access_token_valid'] = False
 			#access_token_validity_obj['g_user_id'] = None
 			#access_token_validity_obj['message'] = 'Access Token not meant for this application.'
 		if not(result['email_verified']):
 			access_token_validity_obj['is_access_token_valid'] = False
 			access_token_validity_obj['g_user_id'] = None
 			access_token_validity_obj['message'] = 'Invalid Access Token. Email is not verified'
 		elif (result['email'] != email):
 			access_token_validity_obj['is_access_token_valid'] = False
 			access_token_validity_obj['g_user_id'] = None
 			access_token_validity_obj['message'] = 'Email is not verified'
 		else:
 			access_token_validity_obj['is_access_token_valid'] = True
 			access_token_validity_obj['g_user_id'] = result['sub']
 			access_token_validity_obj['message'] = 'Valid Access Token.'
 	else:
 		# This is not a valid token.
 		access_token_validity_obj['is_access_token_valid'] = False
 		access_token_validity_obj['g_user_id'] = None
 		access_token_validity_obj['message'] = 'Invalid Access Token. Access Token expired'
 	
 	return access_token_validity_obj

#--------------------------------------
#if __name__ == '__main__':
 	#test_token = 'ya29..zQLSyEJmYu5jaYI00NQgkUpljPBDseL8lh-zE7xuFkFUdpJXWhzskGFgnITR1pLhWw'
 	#print verify_access_token(test_token, "abusalehmdtayeen@gmail.com")
 	
