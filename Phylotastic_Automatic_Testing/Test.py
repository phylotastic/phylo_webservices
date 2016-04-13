import web_services
json_input='Formica polyctena|Formica exsectoides|Formica pecefica'
result_case_1 = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_GET(json_input,["Formica polyctena", "Formica exsectoides"])
json_input='Setophaga striata|Setophaga megnolia|Setophaga angilae|Setophaga plumbea|Setophaga virens'
result_case_1 = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_GET(json_input,["Setophaga striata", "Setophaga plumbea"])
