'''
Required input settings for web service:  

'''
service_id = "ws_20"
service_endpoint = "http://phylo.cs.nmsu.edu:5009/phylotastic_ws/sc"

input_settings = [{'method': "POST", 'path': "/scale", 'weight': 0.3, 'input_data': {'newick': "((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);"} }, 
		{'method': "POST", 'path': "/scale" ,'weight': 0.7, 'input_data': {'newick': "(((((Canis lupus pallipes,Melursus ursinus)Caniformia,((Panthera tigris,Panthera pardus)Panthera,Herpestes fuscus))Carnivora,(Macaca mulatta,Homo sapiens)Catarrhini)Boreoeutheria,Elephas maximus)Eutheria,Haliastur indus)Amniota;"} }
		]

