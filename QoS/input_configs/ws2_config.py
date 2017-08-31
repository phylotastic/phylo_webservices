'''
Required input settings for web service:  

'''
service_id = "ws_2"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn"

input_settings = [{'method': "GET", 'path': "/names_text",'weight': 0.3, 'input_data': {'text': "The lemon dove (Columba larvata) is a species of bird in the pigeon family Columbidae found in montane forests of sub-Saharan Africa."} }, 
		{'method': "GET", 'path': "/names_text", 'weight': 0.7, 'input_data': {'text': "Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries."} }
		]

