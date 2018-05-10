'''
Required input settings for web service:  

'''
service_id = "ws_32"
service_endpoint = "http://phylo.cs.nmsu.edu:5013/phylotastic_ws/sd/ecos"

input_settings = [{'method': "GET", 'path': "/get_conservation", 'weight': 0.3, 'input_data': {'species': "Pongo pygmaeu|Rhinoceros sondaicus|Panthera tigris|Pan troglodytes|Loxodonta africana"} }, 
		{'method': "POST", 'path': "/conservation" ,'weight': 0.7, 'input_data': {'species': ["Ursus maritimus", "Ailuropoda melanoleuca", "Vulpes lagopus", "Delphinapterus leucas", "Diceros bicornis", "Balaenoptera musculus", "Pan paniscus", "Balaena mysticetus", "Pan troglodytes", "Balaenoptera physalus", "Carcharodon carcharias", "Chelonia mydas", "Hippopotamus amphibius", "Orcaella brevirostris", "Panthera onca", "Dermochelys coriacea", "Ara ararauna", "Amblyrhynchus cristatus"]} }]

