'''
Required input settings for web service:  

'''
service_id = "ws_17"
service_endpoint = "http://phylo.cs.nmsu.edu:5006/phylotastic_ws/md"

input_settings = [{'method': "GET", 'path': "/get_studies", 'weight': 0.3, 'input_data': {'list': "Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens", 'list_type': "taxa"} }, 
		{'method': "POST", 'path': "/studies" ,'weight': 0.7, 'input_data': {"list": ["Delphinidae","Delphinus capensis","Delphinus delphis","Tursiops truncatus","Tursiops aduncus","Sotalia fluviatilis","Sousa chinensis"], "list_type": "taxa"} }
		]

