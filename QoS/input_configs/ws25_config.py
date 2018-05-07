'''
Required input settings for web service:  

'''
service_id = "ws_25"
service_endpoint = "http://phylo.cs.nmsu.edu:5013/phylotastic_ws/cs/itis"

input_settings = [{'method': "GET", 'path': "/get_scientific_names", 'weight': 0.3, 'input_data': {'commonnames': "Brown bear|Gray wolf"} }, 
		{'method': "POST", 'path': "/scientific_names" ,'weight': 0.7, 'input_data': {'commonnames': ["Flowering dogwood", "White oak", "Oregon pine", "Button mangrove", "Yellow mombin"]} }
		]

