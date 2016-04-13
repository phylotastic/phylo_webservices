import web_services
json_input='{"scientificNames": ["Formica exsectoides", "Formica pecefica", "Formica polyctena"]}'
result_case_1 = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_POST(json_input,["Formica polyctena", "Formica exsectoides"])
json_input='{"scientificNames": ["Setophaga striata", "Setophaga megnolia", "Setophaga angilae","Setophaga plumbea","Setophaga virens"]}'
result_case_1 = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_POST(json_input,["Setophaga striata", "Setophaga plumbea"])
