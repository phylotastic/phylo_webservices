'''
Required input settings for web service:  

'''
service_id = "ws_28"
service_endpoint = "http://phylo.cs.nmsu.edu:5013/phylotastic_ws/sd/eol"

input_settings = [{'method': "GET", 'path': "/get_habitat_conservation", 'weight': 0.4, 'input_data': {'species': "Thunnus alalunga|Delphinapterus leucas"} }, 
		{'method': "POST", 'path': "/habitat_conservation" ,'weight': 0.6, 'input_data': {'species': ["Ceratotherium simum", "Bison bison bison"]} }]

