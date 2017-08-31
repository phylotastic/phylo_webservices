'''
Required input settings for web service:  

'''
service_id = "ws_8"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol"

input_settings = [{'method': "GET", 'path': "/get_images", 'weight': 0.3, 'input_data': {'species': "Panthera leo"} }, 
		{'method': "POST", 'path': "/images" ,'weight': 0.7, 'input_data': {'species': ["Catopuma badia",
"Catopuma temminckii"]} }
		]

