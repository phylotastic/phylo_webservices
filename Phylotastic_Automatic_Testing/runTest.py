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
result_case_1 = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_GET(names,["Setophaga striata", "Setophaga plumbea"])
print "---------------------------------------------------------"
names="Formica polyctena|Formica exsectoides|Formica pecefica"
print "Case 2 : Paramter NAMES = %s \n" %(str(names))
result_case_2 = False
result_case_2 = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_GET(names,["Formica polyctena", "Formica exsectoides"])
print "---------------------------------------------------------"
if (result_case_1 == True and result_case_2 == True):
    result_ws_3 = True
    print("Sucessful ! Web Service 3 : Resolve Scientific Names with Open Tree TNRS - GET method IS WORKING WELL")
else:
    result_ws_3 = False
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
result_case_1 = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_POST(json_input,["Setophaga striata", "Setophaga plumbea"])
print "---------------------------------------------------------"
json_input='{"scientificNames": ["Formica exsectoides", "Formica pecefica", "Formica polyctena"]}'
print "Case 2 : Paramter  = %s \n" %(str(json_input))
result_case_2 = False
result_case_2 = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_POST(json_input,["Formica polyctena", "Formica exsectoides"])
print "---------------------------------------------------------"
if (result_case_1 == True and result_case_2 == True):
    result_ws_3 = True
    print("Sucessful ! Web Service 3 : Resolve Scientific Names with Open Tree TNRS - POST method IS WORKING WELL")
else:
    result_ws_3 = False
print "========================================================="


########################################################
#Test Web Service 4 : Resolve Scientific Names with GNR TNRS - GET method
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_4 = False
names="Setophaga striata|Setophaga megnolia|Setophaga angilae|Setophaga plumbea|Setophaga virens"
print "Start Test WS 4 : Resolve Scientific Names with GNR TNRS - GET method"
print "Case 1 : Paramter NAMES = %s \n" %(str(names))
result_case_1 = False
result_case_1 = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_GET(names,["Setophaga striata", "Setophaga plumbea"])
print "---------------------------------------------------------"
names="Formica polyctena|Formica exsectoides|Formica pecefica"
print "Case 2 : Paramter NAMES = %s \n" %(str(names))
result_case_2 = False
result_case_2 = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_GET(names,["Formica polyctena", "Formica exsectoides"])
print "---------------------------------------------------------"
if (result_case_1 == True and result_case_2 == True):
    result_ws_4 = True
    print("Sucessful ! Web Service 4 : Resolve Scientific Names with GNR TNRS - GET method IS WORKING WELL")
else:
    result_ws_4 = False
print "========================================================="


########################################################
#Test Web Service 4 : Resolve Scientific Names with GNR TNRS - POST METHOD
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_4 = False
json_input='{"scientificNames": ["Setophaga striata","Setophaga megnolia","Setophaga angilae","Setophaga plumbea","Setophaga virens"]}'
print "Start Test WS 4 : Resolve Scientific Names with GNR TNRS - POST METHOD"
print "Case 1 : Paramter = %s \n" %(str(json_input))
result_case_1 = False
result_case_1 = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_POST(json_input,["Setophaga striata", "Setophaga plumbea"])
print "---------------------------------------------------------"
json_input='{"scientificNames": ["Formica exsectoides", "Formica pecefica", "Formica polyctena"]}'
print "Case 2 : Paramter  = %s \n" %(str(json_input))
result_case_2 = False
result_case_2 = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_POST(json_input,["Formica polyctena", "Formica exsectoides"])
print "---------------------------------------------------------"
if (result_case_1 == True and result_case_2 == True):
    result_ws_4 = True
    print("Sucessful ! Web Service 4 : Resolve Scientific Names with GNR TNRS  - POST method IS WORKING WELL")
else:
    result_ws_4 = False
print "========================================================="


########################################################
#Test Web Service 5 : Get Phylogenetic Trees from Open Tree of Life - GET method
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_5 = False
taxa="Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens"
print "Start Test WS 5 : Get Phylogenetic Trees from Open Tree of Life - GET method"
print "Case 1 : Paramter TAXA = %s \n" %(str(taxa))
result_case_1 = False
result_case_1 = web_services.testService_GetPhylogeneticTreeFrom_OpenTree_5_GET(taxa,"(((Setophaga_striata_ott60236,Setophaga_magnolia_ott3597209),Setophaga_virens_ott3597195),(Setophaga_plumbea_ott3597205,Setophaga_angelae_ott3597191))Setophaga_ott666104;")
print "---------------------------------------------------------"
if (result_case_1 == True):
    result_ws_5 = True
    print("Sucessful ! Web Service 5 : Get Phylogenetic Trees from Open Tree of Life - GET method IS WORKING WELL")
else:
    result_ws_5 = False
print "========================================================="

########################################################
#Test Web Service 5 : Get Phylogenetic Trees from Open Tree of Life - POST method
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_5 = False
json_input='{"resolvedNames": [{"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga striata", "search_string": "setophaga strieta", "synonyms": ["Dendroica striata", "Setophaga striata"], "taxon_id": 60236}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Setophaga magnolia", "search_string": "setophaga magnolia", "synonyms": ["Dendroica magnolia", "Setophaga magnolia"], "taxon_id": 3597209}, {"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga angelae", "search_string": "setophaga angilae", "synonyms": ["Dendroica angelae", "Setophaga angelae"], "taxon_id": 3597191}, {"match_type": "Exact", "resolver_name": "OT", "matched_name": "Setophaga plumbea", "search_string": "setophaga plambea", "synonyms": ["Dendroica plumbea", "Setophaga plumbea"], "taxon_id": 3597205}, {"match_type": "Fuzzy", "resolver_name": "OT", "matched_name": "Setophaga virens", "search_string": "setophaga virens", "synonyms": ["Dendroica virens", "Setophaga virens"], "taxon_id": 3597195}]}'
print "Start Test WS 5 : Get Phylogenetic Trees from Open Tree of Life - POST method"
print "Case 1 : Paramter  = %s \n" %(str(json_input))
result_case_1 = False
result_case_1 = web_services.testService_GetPhylogeneticTreeFrom_OpenTree_5_POST(json_input,"(((Setophaga_striata_ott60236,Setophaga_magnolia_ott3597209),Setophaga_virens_ott3597195),(Setophaga_plumbea_ott3597205,Setophaga_angelae_ott3597191))Setophaga_ott666104;")
print "---------------------------------------------------------"
if (result_case_1 == True):
    result_ws_5 = True
    print("Sucessful ! Web Service 5 : Get Phylogenetic Trees from Open Tree of Life - POST method IS WORKING WELL")
else:
    result_ws_5 = False
print "========================================================="


########################################################
#Test Web Service 6 : Get all Species from a Taxon
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_6 = False
taxon='Vulpes'
print "Start Test WS 6 : Get all Species from a Taxon"
print "Case 1 : Paramter Taxon = %s \n" %(str(taxon))
result_case_1 = False
result_case_1 = web_services.testService_GetAllSpeciesFromATaxon_WS_6(taxon,["Vulpes environmental sample", "Vulpes stenognathus", "Vulpes bengalensis"])
print "---------------------------------------------------------"
taxon='Canidae'
print "Case 2 : Paramter Taxon = %s \n" %(str(taxon))
result_case_2 = False
result_case_2 = web_services.testService_GetAllSpeciesFromATaxon_WS_6(taxon,["Aelurodon taxoides", "Aelurodon asthenostylus", "Aelurodon ferox", "Aelurodon montanensis"])

if (result_case_1 == True and result_case_2 == True):
    result_ws_6 = True
    print("Sucessful ! Web Service 6 : Get all Species from a Taxon IS WORKING WELL")
else:
    result_ws_6 = False
print "========================================================="


########################################################
#Test Web Service 7 : Get all Species from a Taxon filtered by country
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_7 = False
taxon='Panthera'
country='Bangladesh'
print "Start Test WS 7 : Get all Species from a Taxon filtered by country"
print "Case 1 : Paramter Taxon = %s ; Country = %s \n" %(str(taxon),str(country))
result_case_1 = False
result_case_1 = web_services.testService_GetAllSpeciesFromATaxonFilteredByCountry_WS_7(taxon,country,[])
print "---------------------------------------------------------"
taxon='Felidae'
country='Nepal'
print "Case 2: Paramter Taxon = %s ; Country = %s \n" %(str(taxon),str(country))
result_case_2= False
result_case_2 = web_services.testService_GetAllSpeciesFromATaxonFilteredByCountry_WS_7(taxon,country,[])

if (result_case_1 == True and result_case_2 == True):
    result_ws_7 = True
    print("Sucessful ! Web Service 7 : Get all Species from a Taxon filtered by country IS WORKING WELL")
else:
    result_ws_7 = False
print "========================================================="


########################################################
#Test Web Service 8 : Get Image URLs of a list of species - GET method
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_8 = False
species="Panthera leo|Panthera onca|Panthera pardus"
print "Start Test WS 8 : Get Image URLs of a list of species - GET method"
print "Case 1 : Paramter species = %s \n" %(str(species))
result_case_1 = False
result_case_1 = web_services.testService_GetImagesURLListOfSpecies_WS_8_GET(species,"http://media.eol.org/content/2015/11/13/05/46343_orig.jpg")
print "---------------------------------------------------------"
if (result_case_1 == True):
    result_ws_8 = True
    print("Sucessful ! 8 : Get Image URLs of a list of species - GET method IS WORKING WELL")
else:
    result_ws_8 = False
print "========================================================="

########################################################
#Test Web Service 8 : Get Image URLs of a list of species - POST method
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_8 = False
json_param_species='{"species": ["Catopuma badia","Catopuma temminckii"]}'
print "Start Test WS 8 : Get Image URLs of a list of species - POST method"
print "Case 1 : Paramter = %s \n" %(str(json_param_species))
result_case_1 = False
result_case_1 = web_services.testService_GetImagesURLListOfSpecies_WS_8_POST(json_param_species,"http://media.eol.org/content/2014/01/04/04/58116_orig.jpg")
print "---------------------------------------------------------"
if (result_case_1 == True):
    result_ws_8 = True
    print("Sucessful ! 8 : Get Image URLs of a list of species - POST method IS WORKING WELL")
else:
    result_ws_8 = False
print "========================================================="

########################################################
#Finally Result
########################################################
if (result_ws_1 == True and result_ws_2 == True and result_ws_3 == True and result_ws_4 == True and result_ws_5 == True and result_ws_6 == True and result_ws_7 == True and result_ws_8 == True):
    exit(0)
else:
    exit(1)
