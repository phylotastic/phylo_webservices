'''
Required input settings for web service:  

'''
service_id = "ws1"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/country_species"

input_settings = [{'method': "GET", 'weight': 0.3, 'input_data': {'taxon': "Panthera", 'country': "Bangladesh"} }, 
		{'method': "GET", 'weight': 0.7, 'input_data': {'taxon': "Felidae", 'country': "Nepal"} }
		]

