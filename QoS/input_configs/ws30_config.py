'''
Required input settings for web service:  

'''
service_id = "ws_30"
service_endpoint = "http://phylo.cs.nmsu.edu:5007/phylotastic_ws/sls"

input_settings = [{'method': "GET", 'path': "/get_list", 'weight': 1.0, 'input_data': None }, 
		]

