#tree-studies service: version 1.0
import json
import time
import requests
#import urllib

headers = {'content-type': 'application/json'}
opentree_base_url = "https://api.opentreeoflife.org/v3/"

#~~~~~~~~~~~~~~~~~~~~ (OpenTree-tree_of_life)~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_study_ids(ottid_list):
    opentree_method_url = opentree_base_url + "tree_of_life/induced_subtree"
    
    payload = {
        'ott_ids': ottid_list	
    }
    
    jsonPayload = json.dumps(payload)
    
    response = requests.post(opentree_method_url, data=jsonPayload, headers=headers)
    
    studyid_result = {}

    if response.status_code == requests.codes.ok:    
        result_data_json = json.loads(response.text)
        studyid_result['study_ids'] = result_data_json['supporting_studies']
        studyid_result['message'] =  "Success"
     	studyid_result['status_code'] = 200
    else:    
        studyid_result['message'] =  "Error: getting study ids from OpenTree"
     	studyid_result['status_code'] = 500

    return studyid_result

#------------------------(OpenTree-studies)------------------------------
def get_study_info(studyid):
    opentree_method_url = opentree_base_url + "studies/find_studies"
    
    payload = {
        'property': 'ot:studyId',
        'value': studyid,
        'verbose': True	
    }
    
    jsonPayload = json.dumps(payload)
    
    response = requests.post(opentree_method_url, data=jsonPayload, headers=headers)
    
    studyinfo_result = {}

    if response.status_code == requests.codes.ok:    
        result_data_json = json.loads(response.text)
        if (len(result_data_json['matched_studies']) == 0):
           studyinfo_result['message'] =  "No matching study found"
     	   studyinfo_result['status_code'] = 204
        else: 
           if ('ot:studyPublicationReference' in result_data_json['matched_studies'][0]):
              studyinfo_result['Publication'] = result_data_json['matched_studies'][0]['ot:studyPublicationReference']
           else:
              studyinfo_result['Publication'] = ""
           if ('ot:studyId' in result_data_json['matched_studies'][0]):
              studyinfo_result['PublicationIdentifier'] = result_data_json['matched_studies'][0]['ot:studyId']
           else:
              studyinfo_result['PublicationIdentifier'] = studyid
           if ('ot:curatorName' in result_data_json['matched_studies'][0]):
              studyinfo_result['Curator'] = result_data_json['matched_studies'][0]['ot:curatorName']
           else:
              studyinfo_result['Curator'] = ""
           if ('ot:studyYear' in result_data_json['matched_studies'][0]):
              studyinfo_result['PublicationYear'] = result_data_json['matched_studies'][0]['ot:studyYear']
           else:
              studyinfo_result['PublicationYear'] = ""
           if ('ot:focalCladeOTTTaxonName' in result_data_json['matched_studies'][0]):
              studyinfo_result['FocalCladeTaxonName'] = result_data_json['matched_studies'][0]['ot:focalCladeOTTTaxonName']
           else:
              studyinfo_result['FocalCladeTaxonName'] = ""
           if ('ot:studyPublication' in result_data_json['matched_studies'][0]):
              studyinfo_result['PublicationDOI'] = result_data_json['matched_studies'][0]['ot:studyPublication']
           else:
              studyinfo_result['PublicationDOI'] = ""
           if ('ot:dataDeposit' in result_data_json['matched_studies'][0]):
              studyinfo_result['DataRepository'] = result_data_json['matched_studies'][0]['ot:dataDeposit']
           else:
              studyinfo_result['DataRepository'] = ""
           if ('ot:candidateTreeForSynthesis' in result_data_json['matched_studies'][0]):
              studyinfo_result['CandidateTreeForSynthesis'] = result_data_json['matched_studies'][0]['ot:candidateTreeForSynthesis']
           else:
              studyinfo_result['CandidateTreeForSynthesis'] = ""
        
        studyinfo_result['message'] =  "Success"
     	studyinfo_result['status_code'] = 200
    else:    
        studyinfo_result['message'] =  "Error: getting study info from OpenTree"
     	studyinfo_result['status_code'] = 500

    return studyinfo_result

#----------------------------------------------------
def get_studies(studyid_list):
    studies_list = []
    for studyid in studyid_list:
        study_info = get_study_info(studyid)
        if study_info['status_code'] == 200:
           #delete status keys from dictionary 
           del study_info['status_code']
           del study_info['message']
           studies_list.append(study_info)
    
    return studies_list

#----------------------------------------------------
def get_studies_from_ids(id_list, is_ottid=True, post=False):
    start_time = time.time()
    studies_info = {}
    if is_ottid: #check whether the id_list is a list of ott ids or not
       study_id_list_json = get_study_ids(id_list)
       if study_id_list_json['status_code'] == 200:
          study_id_list = study_id_list_json['study_ids']
          studies_info['studies'] = get_studies(study_id_list) 
          studies_info['message'] = "Success"
          studies_info['status_code'] = 200
       else:
          studies_info['studies'] = []
          studies_info['message'] = study_id_list_json['message']
          studies_info['status_code'] = study_id_list_json['status_code']
    else: #when study ids are given directly
       study_list = get_studies(id_list)
       studies_info['studies'] = study_list  
       studies_info['message'] = "Success"
       studies_info['status_code'] = 204 if (len(study_list) == 0) else 200

    end_time = time.time()
    execution_time = end_time-start_time
    studies_info['execution_time'] = float('{:4.2f}'.format(execution_time))

    return studies_info
    #if post:
    #   return studies_info
    #else:
    #   return json.dumps(studies_info)

#-------------------(OpenTree-TNRS)-----------------------------
def get_ott_ids(taxa, context=None):
    opentree_method_url = opentree_base_url + "tnrs/match_names"
    
    payload = {
        'names': taxa
    }
    if context is not None:
       payload['context_name'] = context

    jsonPayload = json.dumps(payload)
   
    response = requests.post(opentree_method_url, data=jsonPayload, headers=headers)
    
    ott_id_list = []
    ott_id_result = {}

    if response.status_code == requests.codes.ok:    
        result_data_json = json.loads(response.text)
        result_list = result_data_json['results'] 
        for result in result_list:
            match_list = result['matches']
            for match in match_list:
                if float(match['score']) >= 0.7:
                   ott_id_list.append(match['taxon']['ott_id'])
                   break

        ott_id_result['ott_ids'] = ott_id_list	
        ott_id_result['status_code'] = 200
        ott_id_result['message'] = "Success"
    else:
        ott_id_result['ott_ids'] = ott_id_list	
        ott_id_result['status_code'] = 500
        ott_id_result['message'] = "Error: getting ott ids from OpenTree"
    
    return ott_id_result

#----------------------------------------------------------
def get_studies_from_names(taxa_list, context=None, post=False):
    start_time = time.time()
    ottidlist_json = get_ott_ids(taxa_list, context)
    studies_info = {}
    if ottidlist_json['status_code'] == 500:    
        final_result = ottidlist_json   
    else:
        study_id_list_json = get_study_ids(ottidlist_json['ott_ids'])
        if study_id_list_json['status_code'] == 200:
           studies_info['studies'] = get_studies(study_id_list_json['study_ids'])
           studies_info['message'] = "Success"
           studies_info['status_code'] = 200 
        else:
           studies_info['studies'] = []
           studies_info['message'] = study_id_list_json['message']
           studies_info['status_code'] = study_id_list_json['status_code']

        final_result = studies_info
    
    end_time = time.time()
    execution_time = end_time-start_time
    final_result['execution_time'] = float('{:4.2f}'.format(execution_time))

    return final_result
    #if post:
    #   return final_result
    #else:
    #   return json.dumps(final_result)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':
	#idlist = []
	#print get_studies_controller(idlist)
