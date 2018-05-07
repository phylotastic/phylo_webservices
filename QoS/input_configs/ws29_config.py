'''
Required input settings for web service:  

'''
service_id = "ws_29"
service_endpoint = "http://phylo.cs.nmsu.edu:5012/phylotastic_ws/gt/tb"

input_settings = [{'method': "POST", 'path': "/tree", 'weight': 0.3, 'input_data': {'taxa':["Physcomitrella patens", "Solanum tuberosum", "Lactuca sativa","Vitis vinifera", "Glycine max", "Carica papaya", "Oryza sativa"]} }, 
		{'method': "POST", 'path': "/tree" ,'weight': 0.7, 'input_data': {'taxa': ["Panthera pardus", "Taxidea taxus", "Enhydra lutris", "Lutra lutra", "Canis latrans", "Canis lupus", "Mustela altaica", "Mustela eversmanni", "Martes americana", "Ictonyx striatus", "Canis anthus", "Lycalopex vetulus", "Lycalopex culpaeus", "Puma concolor", "Felis catus","Leopardus jacobita"]} }
		]

