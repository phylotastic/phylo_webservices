'''
Required input settings for web service:  

'''
service_id = "ws_21"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/tf"

input_settings = [{'method': "GET", 'path': "/names_url", 'weight': 0.3, 'input_data': {'url': "https://en.wikipedia.org/wiki/Cave_bear"} }, 
		{'method': "GET", 'path': "/names_url", 'weight': 0.7, 'input_data': {'url': "https://en.wikipedia.org/wiki/Monkey"} }
		]

