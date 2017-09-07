'''
Required input settings for web service:  

'''
service_id = "ws_18"
service_endpoint = "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pm"

input_settings = [{'method': "GET", 'path': "/get_tree", 'weight': 0.3, 'input_data': {'taxa':"Panthera leo|Panthera onca|Panthera tigris|Panthera uncia"} }, 
		{'method': "POST", 'path': "/tree" ,'weight': 0.7, 'input_data': {'resolvedNames': ["Helianthus annuus","Passiflora edulis", "Rosa arkansana", "Saccharomyces cerevisiae"]} }
		]

