import web_services
json_input='{"scientificNames": ["Setophaga striata","Setophaga megnolia","Setophaga angilae","Setophaga plumbea","Setophaga virens"]}'
result_case_1 = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_POST(json_input,["Dendroica plumbea", "Setophaga plumbea"])
