import web_services

########################################################
#Test Web Service 1 : Find Scientific Names on web pages
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_1 = False
url="https://en.wikipedia.org/wiki/Plain_pigeon"
print "Start Test WS 1 : Find Scientific Names on web pages"
print "Case 1 : Paramter URL = %s \n" %(str(url))
result_case_1 = web_services.testService_FindScientificNamesOnWebPages_WS_1(url,["Patagioenas inornata wetmorei", "Animalia", "Chordata", "Columbiformes"])
print "---------------------------------------------------------"
url="http://en.wikipedia.org/wiki/Ant"
print "Case 2 : Paramter URL = %s \n" %(str(url))
result_case_2 = web_services.testService_FindScientificNamesOnWebPages_WS_1(url,["Animalia", "Arthropoda", "Insecta", "Hymenoptera", "Apocrita", "Vespoidea", "Formicidae"])
print "---------------------------------------------------------"
url="http://www.fws.gov/westvirginiafieldoffice/PDF/beechridgehcp/Appendix_D_Table_D-1.pdf"
print "Case 3 : Paramter URL = %s \n" %(str(url))
#result_case_3 = web_services.testService_FindScientificNamesOnWebPages_WS_1(url)
result_case_3 = True
print "---------------------------------------------------------"
if (result_case_1 == True and result_case_2 == True and result_case_3 == True):
    result_ws_1 = True
    print("Sucessful ! Web Service 1 : Find Scientific Names on web pages IS WORKING WELL")
else:
    result_ws_1 = False
print "========================================================="


########################################################
#Test Web Service 2 : Find Scientific Names on free-form text
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_2 = False
text="The lemon dove (Columba larvata) is a species of bird in the pigeon family Columbidae found in montane forests of sub-Saharan Africa."
print "Start Test WS 2 : Find Scientific Names on free-form text"
print "Case 1 : Paramter TEXT = %s \n" %(str(text))
result_case_1 = False
result_case_1 = web_services.testService_FindScientificNamesOnText_WS_2(text,["Columba larvata", "Columbidae"])
print "---------------------------------------------------------"
text="Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries."
print "Case 2 : Paramter TEXT = %s \n" %(str(text))
result_case_2 = False
result_case_2 = web_services.testService_FindScientificNamesOnText_WS_2(text,["Formica polyctena", "Tetramorium caespitum", "Pseudomyrmex", "Adetomyrma venatrix", "Carebara diversa", "Formicinae"])
print "---------------------------------------------------------"
if (result_case_1 == True and result_case_2 == True):
    result_ws_2 = True
    print("Sucessful ! Web Service 2 : Find Scientific Names on free-form text IS WORKING WELL")
else:
    result_ws_2 = False
print "========================================================="

########################################################
#Test Web Service 3 : Resolve Scientific Names with Open Tree TNRS - GET method
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_3 = False
names="Setophaga striata|Setophaga megnolia|Setophaga angilae|Setophaga plumbea|Setophaga virens"
print "Start Test WS 3 : Resolve Scientific Names with Open Tree TNRS - GET method"
print "Case 1 : Paramter NAMES = %s \n" %(str(names))
result_case_1 = False
result_case_1 = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_GET(names,["Dendroica plumbea", "Setophaga plumbea"])
print "---------------------------------------------------------"
names="Formica polyctena|Formica exsectoides|Formica pecefica"
print "Case 2 : Paramter NAMES = %s \n" %(str(names))
result_case_2 = False
result_case_2 = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_GET(names,["Formica polyctenum", "Formica polyctena"])
print "---------------------------------------------------------"
if (result_case_1 == True and result_case_2 == True):
    result_ws_2 = True
    print("Sucessful ! Web Service 3 : esolve Scientific Names with Open Tree TNRS - GET method IS WORKING WELL")
else:
    result_ws_2 = False
print "========================================================="

########################################################
#Test Web Service 3 : Resolve Scientific Names with Open Tree TNRS - POST method
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_3 = False
json_input='{"scientificNames": ["Setophaga striata","Setophaga megnolia","Setophaga angilae","Setophaga plumbea","Setophaga virens"]}'
print "Start Test WS 3 : Resolve Scientific Names with Open Tree TNRS - POST method"
print "Case 1 : Paramter = %s \n" %(str(json_input))
result_case_1 = False
result_case_1 = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_POST(json_input,["Dendroica plumbea", "Setophaga plumbea"])
print "---------------------------------------------------------"
json_input='{"scientificNames": ["Formica exsectoides", "Formica pecefica", "Formica polyctena"]}'
print "Case 2 : Paramter  = %s \n" %(str(json_input))
result_case_2 = False
result_case_2 = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_POST(json_input,["Formica polyctenum", "Formica polyctena"])
print "---------------------------------------------------------"
if (result_case_1 == True and result_case_2 == True):
    result_ws_2 = True
    print("Sucessful ! Web Service 3 : esolve Scientific Names with Open Tree TNRS - POST method IS WORKING WELL")
else:
    result_ws_2 = False
print "========================================================="


if (result_ws_1 == True and result_ws_2 == True):
    exit(0)
else:
    exit(1)
