'''
Required input settings for web service:  

'''
service_id = "ws_26"
service_endpoint = "http://phylo.cs.nmsu.edu:5013/phylotastic_ws/cs/tpcs"

input_settings = [{'method': "GET", 'path': "/get_scientific_names", 'weight': 0.3, 'input_data': {'commonnames': "Castor bean|Indian sandalwood|Annual blue grass"} }, 
		{'method': "POST", 'path': "/scientific_names" ,'weight': 0.7, 'input_data': {'commonnames': ["cucumber", "tomato", "lettuce", "pea"]} }]

