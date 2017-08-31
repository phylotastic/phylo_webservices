'''
Required input settings for web service:  

'''
service_id = "ws_7"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts"

input_settings = [{'method': "GET", 'path': "/country_species", 'weight': 0.3, 'input_data': {'taxon': "Panthera", 'country': "Bangladesh"} }, 
		{'method': "GET", 'path': "/country_species",'weight': 0.7, 'input_data': {'taxon': "Felidae", 'country': "Nepal"} }
		]

