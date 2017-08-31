'''
Required input settings for web service:  

'''
service_id = "ws_10"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/sl/eol"

input_settings = [{'method': "GET", 'path': "/get_links", 'weight': 0.3, 'input_data': {'species': "Panthera onca"} }, 
		{'method': "POST", 'path': "/links" ,'weight': 0.7, 'input_data': {'species': ["Catopuma badia",
"Catopuma temminckii"]} }
		]

