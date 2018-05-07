'''
Required input settings for web service:  

'''
service_id = "ws_24"
service_endpoint = "http://phylo.cs.nmsu.edu:5013/phylotastic_ws/cs/ncbi"

input_settings = [{'method': "GET", 'path': "/get_scientific_names", 'weight': 0.3, 'input_data': {'commonnames': "blue whale|swordfish|killer whale"} }, 
		{'method': "POST", 'path': "/scientific_names" ,'weight': 0.7, 'input_data': {'commonnames': ["cattle", "cat", "goat", "pig", "sheep", "duck", "chicken", "horse", "domestic dog"]} }
		]

