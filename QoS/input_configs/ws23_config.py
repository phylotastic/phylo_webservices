'''
Required input settings for web service:  

'''
service_id = "ws_23"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ip"

input_settings = [{'method': "GET", 'path': "/resolve", 'weight': 0.3, 'input_data': {'names': "Acanthophyllum albidum|Acanthostachys pitcairnioides|Acanthostyles buniifolius"} }, 
		{'method': "POST", 'path': "/names" ,'weight': 0.7, 'input_data': {'scientificNames': ["Alnus glutinosa", "Ilex verticillata", "Ambrosia trifida", "Malus domestica", "Fraxinus pennsylvanica", "Ilex decidua", "Betula papyrifera", "Betula papyrifera", "Betula nigra", "Rudbeckia hirta", "Plantago major", "Asclepias syriaca", "Daucus carota", "Prunus serotina", "Prunus serotina", "Rudbeckia fulgida", "Cornus amomum", "Barbarea verna", "Cardamine concatenata", "Rudbeckia hirta", "Cornus florida", "Cornus nuttallii"]} }
		]

