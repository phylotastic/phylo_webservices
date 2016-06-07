import web_services
import helper

########################################################
#Test Web Service 1 : Find Scientific Names on web pages
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 1 : Find Scientific Names on web pages (GNRD)"
print "========================================================="
result_ws_1 = True
ws1_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/Find_Sc_Names_Web_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	input_list = helper.create_list_file(f)
	ws1_input = input_list[0]
	#print "Case file input: " + ws1_input
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_1 = False
 		print "Could not find output file for " + f
		break;
	else:		
		ws1_output = helper.create_list_file(output_file)
		#print "Case file output: " + ws1_output
 		ws1_result = web_services.testService_FindScientificNamesOnWebPages_WS_1(ws1_input, ws1_output)
		if ws1_result:
			print "Test succeeded for Case file: " + f
			print "---------------------------------------------------------" 
		ws1_results.append(ws1_result)

for result in ws1_results:
	result_ws_1 = (result_ws_1 and result)
 	if not(result_ws_1):
		break; 

print "---------------------------------------------------------"
if len(ws1_results) == 0:
	print "No Test Cases found"
	result_ws_1 = False 
elif (result_ws_1):
    print("Success ! Web Service 1 : Find Scientific Names on web pages IS WORKING WELL")
else:
    print("Failed ! Web Service 1 : Find Scientific Names on web pages IS NOT WORKING")

########################################################
#Test Web Service 2 : Find Scientific Names on free-form text
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 2 : Find Scientific Names on free-form text"
print "========================================================="
result_ws_2 = True
ws2_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/Find_Sc_Names_Text_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	ws2_input = helper.create_content_file(f)
	#print "Case file input: " + ws2_input
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_2 = False
 		print "Could not find output file for " + f
		break		
	ws2_output = helper.create_list_file(output_file)
	#print "Case file output: " + ws2_output
 	ws2_result = web_services.testService_FindScientificNamesOnText_WS_2(ws2_input, ws2_output)
	if ws2_result:
		print "Test succeeded for Case file: " + f
		print "-----------------------------------------------------" 
	ws2_results.append(ws2_result)

for result in ws2_results:
	result_ws_2 = (result_ws_2 and result)
 	if not(result_ws_2):
		break 

print "---------------------------------------------------------"
if len(ws2_results) == 0:
	print "No Test Cases found"
	result_ws_2 = False 
elif (result_ws_2):
    print("Success ! Web Service 2 : Find Scientific Names on free-form text IS WORKING WELL")
else:
    print("Failed ! Web Service 2 : Find Scientific Names on free-form text IS NOT WORKING")

########################################################
#Test Web Service 3 : Resolve Scientific Names with Open Tree TNRS - (Both GET and Post method) 
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 3 : Resolve Scientific Names with Open Tree TNRS"
print "========================================================="
result_ws_3 = False
ws3_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/TNRS_OT_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	input_list = helper.create_list_file(f)
 	#prepare ws3 input
	separator = "|"
	ws3_input_GET = separator.join(input_list)
	print "Case file input: " + ws3_input_GET
	ws3_input_POST = helper.prepare_json_input('{"scientificNames":[',input_list) 
	print "Case file input: " + ws3_input_POST
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_3 = False
 		print "Could not find output file for " + f
		break		
	ws3_output = helper.create_list_file(output_file)
	#print "Case file output: " + ws2_output
 	ws3_result_GET = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_GET(ws3_input_GET, ws3_output)
	ws3_result_POST = web_services.testService_ResolveScientificNamesOpenTreeWS_WS_3_POST(ws3_input_POST, ws3_output) 	
	ws3_result = ws3_result_GET and ws3_result_POST

	if ws3_result_GET and ws3_result_POST:
		print "Test succeeded for Case file: " + f
	elif ws3_result_GET:
		print "GET - method Test succeeded for Case file: " + f
	elif ws3_result_POST:
		print "POST - method Test succeeded for Case file: " + f
	print "-----------------------------------------------------" 
	ws3_results.append(ws3_result)

for result in ws3_results:
	result_ws_3 = (result_ws_3 and result)
 	if not(result_ws_3):
		break 

print "---------------------------------------------------------"
if len(ws3_results) == 0:
	print "No Test Cases found"
	result_ws_3 = False 
elif (result_ws_3):
    print("Success ! Web Service 3 : Resolve Scientific Names with Open Tree TNRS IS WORKING WELL")
else:
    print("Failed ! Web Service 3 : Resolve Scientific Names with Open Tree TNRS IS NOT WORKING")

########################################################
#Test Web Service 4 : Resolve Scientific Names with GNR TNRS - (Both GET and Post method)
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
print "Start Testing WS 4 : Resolve Scientific Names with GNR TNRS"
print "========================================================="
result_ws_4 = False
ws4_results = []
files_list = helper.get_filepaths("Phylotastic_Automatic_Testing/TNRS_GNR_TestCases")
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")

for f in input_files:
	print "Testing Case file: " + f
	file_no = helper.get_file_num(f)
	input_list = helper.create_list_file(f)
 	#prepare ws3 input
	separator = "|"
	ws4_input_GET = separator.join(input_list)
	print "Case file input: " + ws4_input_GET
	ws4_input_POST = helper.prepare_json_input('{"scientificNames":[',input_list) 
	print "Case file input: " + ws4_input_POST
	output_file = None
	output_file = helper.find_outputfile(output_files, file_no)
	if output_file == None:
		result_ws_4 = False
 		print "Could not find output file for " + f
		break		
	ws4_output = helper.create_list_file(output_file)
	#print "Case file output: " + ws2_output
 	ws4_result_GET = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_GET(ws4_input_GET, ws4_output)
	ws4_result_POST = web_services.testService_ResolveScientificNamesGNR_TNRS_WS_4_POST(ws4_input_POST, ws4_output) 	
	ws4_result = ws4_result_GET and ws4_result_POST

	if ws4_result_GET and ws4_result_POST:
		print "Test succeeded for Case file: " + f
	elif ws4_result_GET:
		print "GET - method Test succeeded for Case file: " + f
	elif ws4_result_POST:
		print "POST - method Test succeeded for Case file: " + f
	print "-----------------------------------------------------" 
	ws4_results.append(ws4_result)

for result in ws4_results:
	result_ws_4 = (result_ws_4 and result)
 	if not(result_ws_4):
		break 

print "---------------------------------------------------------"
if len(ws4_results) == 0:
	print "No Test Cases found"
	result_ws_4 = False 
elif (result_ws_4):
    print("Success ! Web Service 4 : Resolve Scientific Names with GNR TNRS IS WORKING WELL")
else:
    print("Failed ! Web Service 4 : Resolve Scientific Names with GNR TNRS IS NOT WORKING")


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
    print("Sucessful ! Web Service 8 : Get Image URLs of a list of species - GET method IS WORKING WELL")
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
    print("Sucessful ! Web Service 8 : Get Image URLs of a list of species - POST method IS WORKING WELL")
else:
    result_ws_8 = False
print "========================================================="


########################################################
#Test Web Service 9 : Get Species (of a Taxon) that have genome sequence in NCBI
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
result_ws_9 = False
taxon="Panthera"
print "Start Test WS 9 : Get Species (of a Taxon) that have genome sequence in NCBI"
print "Case 1 : Paramter taxon = %s \n" %(str(taxon))
result_case_1 = False
result_case_1 = web_services.testService_GetSpeciesNCBI_WS_9_GET(taxon,["Panthera tigris amoyensis", "Panthera tigris altaica", "Panthera tigris"])
print "---------------------------------------------------------"

taxon="Rodentia"
print "Case 2 : Paramter taxon = %s \n" %(str(taxon))
result_case_2 = False
result_case_2 = web_services.testService_GetSpeciesNCBI_WS_9_GET(taxon,["Nannospalax galili", "Fukomys damarensis", "Myodes glareolus", "Peromyscus maniculatus bairdii"])
print "---------------------------------------------------------"

if (result_case_1 == True and result_case_2 == True):
    result_ws_9 = True
    print("Sucessful ! Web Service 9 : Get Species (of a Taxon) that have genome sequence in NCBI IS WORKING WELL")
else:
    result_ws_8 = False
print "========================================================="

########################################################
#Finally Result
########################################################
if (result_ws_1 == True and result_ws_2 == True and result_ws_3 == True and result_ws_4 == True and result_ws_5 == True and result_ws_6 == True and result_ws_7 == True and result_ws_8 == True and result_ws_9 == True):
    exit(0)
else:
    exit(1)
