'''
Required input settings for web service:  

'''
service_id = "ws_19"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pt"

input_settings = [{'method': "GET", 'path': "/get_tree", 'weight': 0.3, 'input_data': {'taxa':"Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens"} }, 
		{'method': "POST", 'path': "/tree" ,'weight': 0.7, 'input_data': {'resolvedNames': ["Setophaga striata", "Setophaga magnolia", "Setophaga angelae", "Setophaga plumbea", "Setophaga virens"]} }
		]

