# Quality of Service (QoS) for phylotastic webservices

The API to access the QoS framework for phylotastic webservices are described below.

#### QoS API 1

__Service Name:__  	 	<a name="servicegroups">Get group names of web services</a>

__Service Description:__  A service	to get group names of phylotastic web services for which qos metrics are available.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5010/phylotastic_ws/qs/get_service_groups>

__HTTP Method:__ 		GET

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__			None

 				
__Examples:__ 

1. To get the group names of the web services
```
http://phylo.cs.nmsu.edu:5010/phylotastic_ws/qs/get_service_groups
```
__Example Results:__

1. 
``` 
{
    "status_code":200,
    "message":"Success",
    "service_groups":[
        "Scientific Name Extraction",
        "Image-Information URL Retrieval",
        "Miscellaneous",
        "Phylogenetic Tree Retrieval",
        "Tree Scaling",
        "Taxonomic Name Resolution",
        "Common Name to Scientific Name",
        "Species data services",
        "Species List Manipulation",
        "Tree Viewer",
        "Taxon to Species"
    ]
}
```

---


#### QoS API 2

__Service Name:__  	 	<a name="serviceids">Get web service ids based on web service group</a>

__Service Description:__  A service	to get ids of phylotastic web services for which qos metrics are available.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5010/phylotastic_ws/qs/get_serviceids>

__HTTP Method:__ 		GET

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	group 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  a string value to specify the group of web services. 
  * __Permitted Values:__ any value retrieved using [group service](#servicegroups)
 				

__Examples:__ 

1. To get the web service ids of service group "Scientific Name Extraction"
```
http://phylo.cs.nmsu.edu:5010/phylotastic_ws/qs/get_serviceids?group=Scientific%20Name%20Extraction
```
2. To get the web service ids of service group "Taxon to Species"
```
http://phylo.cs.nmsu.edu:5010/phylotastic_ws/qs/get_serviceids?group=Taxon%20to%20Species
```
__Example Results:__

1. 
``` 
{
    "status_code":200,
    "message":"Success",
    "matched_services":[
        {
            "service_id":"ws_1",
            "service_title":"GNRD_wrapper_URL"
        },
        {
            "service_id":"ws_2",
            "service_title":"GNRD_wrapper_text"
        },
        {
            "service_id":"ws_21",
            "service_title":"TaxonFinder_wrapper_URL"
        },
        {
            "service_id":"ws_22",
            "service_title":"TaxonFinder_wrapper_text"
        }
    ]
}
```
2. 
```
{
    "status_code":200,
    "message":"Success",
    "matched_services":[
        {
            "service_id":"ws_6",
            "service_title":"Taxon_all_species"
        },
        {
            "service_id":"ws_7",
            "service_title":"Taxon_country_species"
        },
        {
            "service_id":"ws_9",
            "service_title":"Taxon_genome_species"
        }
    ]
}
``` 

---

#### QoS API 3

__Service Name:__  	 	Get qos metric value for a particular web service

__Service Description:__  A service	to get value of a qos metric for a particular phylotastic web service.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5010/phylotastic_ws/qs/get_qosvalue>

__HTTP Method:__ 		GET

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	service_id 
  * __Category:__  	mandatory
  * __Data Type:__  integer
  * __Description:__  an integer value to specify the id of the web service. 
  * __Permitted Values:__ any values retrieved using the above [service](#serviceids)
 				
2. Parameter details:
  * __Name:__ 	 	qos_id 
  * __Category:__  	mandatory
  * __Data Type:__  integer
  * __Description:__  an integer value to specify the id of the qos metric. 
  * __Permitted Values:__ any qos_id values from the following table.


| qos_id        | qos_parameter | qos_param_definition  |
| ------------- |---------------| ----------------------|
| 1             | Response time | The amount of time taken to receive respose after a request is sent       |
| 2             | Throughput    | Average number of successful responses for a given period of time         |
| 3             | Availability  | The probability that the service will be available at some period of time |
| 4             | Reliability   | Total operational time/number of failures                                 |

__Examples:__ 

1. To get the response time for web service with id 'ws_2'
```
http://phylo.cs.nmsu.edu:5010/phylotastic_ws/qs/get_qosvalue?service_id=ws_2&qos_id=1
```
2. To get the throughput for web service with id 'ws_3'
```
http://phylo.cs.nmsu.edu:5010/phylotastic_ws/qs/get_qosvalue?service_id=ws_3&qos_id=2
```
__Example Results:__

1. 
``` 
{"service_id": "ws_2","status_code": 200,"message": "Success","qos_result": {"qos_unit": "seconds","qos_date_updated": "09-04-2017","qos_value": 0.45,"qos_parameter": "response time"}}
```
2. 
```
{"service_id": "ws_3","status_code": 200,"message": "Success","qos_result": {"qos_unit": "requests per second (RPS)","qos_date_updated":"09-04-2017","qos_value": 27.49,"qos_parameter": "throughput"}}
```

