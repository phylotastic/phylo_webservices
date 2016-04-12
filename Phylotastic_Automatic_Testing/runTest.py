import web_services

########################################################
#Test Web Service 1 : Find Scientific Names on web pages
#Document : https://github.com/phylotastic/phylo_services_docs/blob/master/ServiceDescription/PhyloServicesDescription.md
########################################################
print "========================================================="
url="https://en.wikipedia.org/wiki/Plain_pigeon"
print "Start Test WS 1 : Find Scientific Names on web pages"
print "Case 1 : Paramter URL = %s \n" %(str(url))
result_case_1 = web_services.testService_FindScientificNamesOnWebPages_WS_1(url)
print "---------------------------------------------------------"
url="http://en.wikipedia.org/wiki/Ant"
print "Start Test WS 1 : Find Scientific Names on web pages"
print "Case 2 : Paramter URL = %s \n" %(str(url))
result_case_2 = web_services.testService_FindScientificNamesOnWebPages_WS_1(url)
print "---------------------------------------------------------"
url="http://www.fws.gov/westvirginiafieldoffice/PDF/beechridgehcp/Appendix_D_Table_D-1.pdf"
print "Start Test WS 1 : Find Scientific Names on web pages"
print "Case 3 : Paramter URL = %s \n" %(str(url))
#result_case_3 = web_services.testService_FindScientificNamesOnWebPages_WS_1(url)
result_case_3 = True
print "========================================================="


if (result_case_1 == True and result_case_2 == True and result_case_3 == True):
    exit(0)
else:
    exit(1)
