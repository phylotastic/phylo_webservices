# Phylotastic Web Services Documentation
 
If you have a suggestion to improve this documentation or have found any errors in any of the web services, please submit an issue on the
[repo](https://github.com/phylotastic/phylo_services_docs/issues).

__Phylotastic Web Services__ are grouped into the following categories:

**[Scientific Name Extraction services](#nameextraction)** : services to extract scientific names on web pages, PDFs, Microsoft Office documents, images.

**[Taxonomic Name Resolution services](#tnrs)** : services for resolving taxonomic names to different data source identifiers.

**[Phylogenetic Tree Retrieval services](#treeretrieval)** : services to retrieve Phylogenetic trees.

**[Taxon to Species services](#taxonspecies)** : services to fetch a set of species belonging to a particular Taxon.

**[Image/Infromation URL Retrieval services](#imageinforetrieval)** :  services for obtaining Image/Infromation URLs related to a set of species.

**[Common Name to Sceintific Name services](#commonname)** :  services to find scientific names from common names.

**[Species List services](#specieslist)** :  services to publish/remove/update/access lists of species owned by a phylotastic web application/services user.

**[Tree scaling services](#treescaling)** :  services for getting chronograms (trees with branch lengths proportional to time).

**[Miscellaneous services](#misc)** :  services for different use cases.

---

## <a name='nameextraction'></a>Scientific Name Extraction

__Service Name:__  	 	GNRD_wrapper_URL

__Service Description:__ 	A service to extract scientific names from URL of a web page or a file(e.g. PDF, Microsoft Office documents, images) using Global Names Recognition and Discovery (GNRD) services.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">url</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  an encoded URL for a web page, PDF, Microsoft Office document, or image file from which scientific names need to be extracted.
 				
2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">engine</span> 
  * __Category:__  	optional
  * __Data Type:__  integer
  * __Description:__  a integer value to specify which search engine (_TaxonFinder_ or _NetiNeti_) to use. By default it is `0` which means it will use both engines. Value `1` means TaxonFinder and value `2` means NetiNeti.
 				
__Example Commands/Requests:__

1. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url?url=https://en.wikipedia.org/wiki/Plain_pigeon&engine=1
```

2. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url?url=http://www.fws.gov/westvirginiafieldoffice/PDF/beechridgehcp/Appendix_D_Table_D-1.pdf
```

__Example Results:__

1. 
```json
{
	"status_code": 200,
	"input_url": "https://en.wikipedia.org/wiki/Plain_pigeon",
	"meta_data": {
		"execution_time": 1.33,
		"creation_time": "2017-10-18T15:01:40.552183",
		"source_urls": [
			"http://gnrd.globalnames.org/"
		]
	},
	"total_names": 9,
	"scientific_names": [
		"Patagioenas inornata wetmorei",
		"Animalia",
		"Chordata",
		"Aves",
		"Columbiformes",
		"Columbidae",
		"Patagioenas",
		"Patagioenas inornata",
		"Columba inornata"
	],
	"message": "Success",
	"gnrd_parameters": {
		"engine": 1,
		"best_match_only": false,
		"data_source_ids": [],
		"detect_language": true,
		"preferred_data_sources": [],
		"all_data_sources": false,
		"return_content": false
	}
}
```
2. 
```json
{
	"status_code": 200,
	"input_url": "http://www.fws.gov/westvirginiafieldoffice/PDF/beechridgehcp/Appendix_D_Table_D-1.pdf",
	"meta_data": {
		"execution_time": 1.95,
		"creation_time": "2017-10-18T15:03:58.433858",
		"source_urls": [
			"http://gnrd.globalnames.org/"
		]
	},
	"total_names": 153,
	"scientific_names": [
		"Menziesia pilosa",
		"Fagus grandifolia",
		"Sorbus americana",
		"Lolium multiflorum",
		"Elaeagnus umbellata",
		"Prunus serotina",
		"Robinia pseudoacacia",
		"Rubus",
		"Lespedeza",
		"Prunus",
		"Trifolium",
		"Magnolia acuminata",
		"Tsuga canadensis",
		"Sambucus",
		"Schedonorus phoenix",
		"Alliaria petiolata",
		"Solidago",
		"Smilax",
		"Microstegium vimineum",
		"Impatiens capensis",
		"Pueraria montana var. lobata",
		"Multiflora",
		"Tulip poplar",
		"Trifolium pratense",
		"Lonicera morrowii",
		"Kalmia latifolia",
		"Acer spicatum",
		"Rosa multiflora",
		"Quercus",
		"Lolium perenne",
		"Pinus",
		"Festuca rubra",
		"Quercus rubra",
		"Picea rubens",
		"Betula alleghaniensis",
		"Arabis serotina",
		"Isotria medeoloides",
		"Urtica dioica",
		"Acer pensylvanicum",
		"Acer saccharum",
		"Ailanthus altissima",
		"Liriodendron tulipifera",
		"Micropterus",
		"Salvelinus fontinalis",
		"Etheostoma osburni",
		"Etheostoma",
		"Ambloplites rupestris",
		"Cottus",
		"Plethodon nettingi",
		"Empidonax alnorum",
		"Vermivora chrysoptera",
		"Corvus brachyrhynchos",
		"Dumetella carolinensis",
		"Falco sparverius",
		"Catharus minimus",
		"Setophaga ruticilla",
		"Setophaga citrina",
		"Turdus migratorius",
		"Passerina cyanea",
		"Scolopax minor",
		"Geothlypis formosa",
		"Haliaeetus leucocephalus",
		"Anas platyrhynchos",
		"Strix vari",
		"Oreothlypis ruficapilla",
		"Setophaga castanea",
		"Accipiter gentilis",
		"Coragyps atratus",
		"Circus cyaneus",
		"Mniotilta varia",
		"Pandion haliaetus",
		"Coccyzus erythropthalmus",
		"Seiurus aurocapilla",
		"Setophaga fusca",
		"Setophaga discolor",
		"Setophaga caerulescens",
		"Loxia curvirostra",
		"Setophaga virens",
		"Vireo olivaceus",
		"Cyanocitta cristata",
		"Vermivora cyanoptera",
		"Melanerpes erythrocephalus",
		"Buteo lineatus",
		"Buteo platypterus",
		"Buteo jamaicensis",
		"Toxostoma rufum",
		"Buteo lagopus",
		"Molothrus ater",
		"Bonasa umbellus",
		"Cardellina canadensis",
		"Accipiter striatus",
		"Bombycilla cedrorum",
		"Melospiza melodia",
		"Setophaga cerulea",
		"Cyanocitta stelleri",
		"Setophaga pensylvanica",
		"Catharus ustulatus",
		"Spizella passerina",
		"Limnothlypis swainsonii",
		"Quiscalus quiscula",
		"Cathartes aura",
		"Chordeiles minor",
		"Catharus fuscescens",
		"Accipiter cooperii",
		"Pooecetes gramineus",
		"Junco hyemalis",
		"Aphelocoma californica",
		"Tyrannus tyrannus",
		"Caprimulgus vociferus",
		"Megascops asio",
		"Aix sponsa",
		"Pipilo erythrophthalmus",
		"Hylocichla mustelina",
		"Sturnus vulgaris",
		"Empidonax flaviventris",
		"Spizella pusilla",
		"Icteria virens",
		"Aquila chrysaetos",
		"Setophaga coronata",
		"Eptesicus fuscus",
		"Myotis lucifugus",
		"Ursus americanus",
		"Zapus hudsonius",
		"Lynx rufus",
		"Eptesicus nilssonii",
		"Tadarida brasiliensis",
		"Myotis septentrionalis",
		"Otospermophilus beecheyi",
		"Sorex palustris albibarbis",
		"Canis latrans",
		"Procyon lotor",
		"Peromyscus maniculatus",
		"Corynorhinus rafinesquii",
		"Cervus canadensis canadiensis",
		"Lasiurus borealis",
		"Lasiurus seminolus",
		"Myotis leibii",
		"Lasionycteris noctivagans",
		"Nycticeius humeralis",
		"Lepus americanus",
		"Glaucomys",
		"Sciurus niger",
		"Myotis grisescens",
		"Sciurus carolinensis",
		"Lasiurus cinereus",
		"Pipistrellus subflavus",
		"Corynorhinus townsendii virginianus",
		"Mustela",
		"Glaucomys sabrinus fuscus",
		"Odocoileus virginianus",
		"Myotis sodalis",
		"Bison bison athabascae",
		"Sciurus vulgaris"
	],
	"message": "Success",
	"gnrd_parameters": {
		"engine": 0,
		"best_match_only": false,
		"data_source_ids": [],
		"detect_language": true,
		"preferred_data_sources": [],
		"all_data_sources": false,
		"return_content": false
	}
}
```

__Citation/Source:__  	 		http://gnrd.globalnames.org/

__Service Quality:__

 * *Restrictions on capacity:*  __unknown__
 * *Restrictions on scope:*     __accepts only valid URL inputs__ 
 * *Expected response time:*  	__1s~10s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. ulr)     | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /nme_url)| 404             | Error: Could not find the requested resource URI |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_scientific_names_) will be an empty list.

---

__Service Name:__  	 	GNRD_wrapper_text

__Service Description:__ 	A service to extract scientific names on free-form text using Global Names Recognition and Discovery (GNRD) services.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_text>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">text</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  text from which scientific names need to be extracted.
 				
2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">engine</span> 
  * __Category:__  	optional
  * __Data Type:__  integer
  * __Description:__  a integer value to specify which search engine (_TaxonFinder_ or _NetiNeti_) to use. By default it is `0` which means it will use both engines. Value `1` means TaxonFinder and value `2` means NetiNeti.
 				
__Example Commands/Requests:__

1. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_text?text=The lemon dove (Columba larvata) is a species of bird in the pigeon family Columbidae found in montane forests of sub-Saharan Africa.&engine=2
```
2. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_text?text=Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries.
```

__Example Results:__

1. 
```json
{
	"status_code": 200,
	"meta_data": {
		"execution_time": 1.05,
		"creation_time": "2017-10-18T17:48:09.949718",
		"source_urls": [
			"http://gnrd.globalnames.org/"
		]
	},
	"total_names": 2,
	"scientific_names": [
		"Columba larvata",
		"Columbidae"
	],
	"message": "Success",
	"gnrd_parameters": {
		"engine": 2,
		"best_match_only": false,
		"data_source_ids": [],
		"detect_language": true,
		"preferred_data_sources": [],
		"all_data_sources": false,
		"return_content": false
	},
	"input_text": "The lemon dove (Columba larvata) is a species of bird in the pigeon family Columbidae found in montane forests of sub-Saharan Africa."
}
``` 

2. 
```json
{
	"status_code": 200,
	"meta_data": {
		"execution_time": 0.93,
		"creation_time": "2017-10-18T17:49:32.614705",
		"source_urls": [
			"http://gnrd.globalnames.org/"
		]
	},
	"total_names": 6,
	"scientific_names": [
		"Formica polyctena",
		"Tetramorium caespitum",
		"Pseudomyrmex",
		"Adetomyrma venatrix",
		"Carebara diversa",
		"Formicinae"
	],
	"message": "Success",
	"gnrd_parameters": {
		"engine": 0,
		"best_match_only": false,
		"data_source_ids": [],
		"detect_language": true,
		"preferred_data_sources": [],
		"all_data_sources": false,
		"return_content": false
	},
	"input_text": "Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries."
}
```

__Citation/Source:__  	 		http://gnrd.globalnames.org/

__Service Quality:__

 * *Restrictions on capacity:*  __unknown__
 * *Restrictions on scope:*     __accepts english text content as input__ 
 * *Expected response time:*  	__0.5s~10s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. txt)     | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /nme_txt)| 404             | Error: Could not find the requested resource URI |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_scientific_names_) will be an empty list.

---

## <a name="tnrs"></a>Taxonomic Name Resolution

__Service Name:__  	 		OToL_TNRS_wrapper

__Service Description:__ 	A service which resolves scientific names using Open Tree of Life Taxonomic name resolution services.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json

__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">names</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  one or more scientific names to be resolved delimited by pipe "|".
 				
2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">fuzzy_match</span> 
  * __Category:__  	optional
  * __Data Type:__  boolean
  * __Description:__  a boolean value to specify whether to perform approximate string (a.k.a. "fuzzy") matching. By default, it is `false`. To turn on "fuzzy" matching `true` must be used. 

3. Parameter details:
  * __Name:__ 	 	<span style="color:blue">multiple_match</span> 
  * __Category:__  	optional
  * __Data Type:__  boolean
  * __Description:__  a boolean value to specify whether to return multiple match results when fuzzy matching is turned on. By default it is `false`. If fuzzy matching is turned on and _multiple_match_ is enabled (`true`), then the service will return results of matches with score more than `0.75`.
 				
__Example Commands/Requests:__

1. 

```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve?names=Formica polyctena|Formica exsectoides|Formica pecefica
```
2. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/resolve?names=Pinus resionosa|Meli officinalis&fuzzy_match=true&multiple_match=true
```

__Example Results:__

1. 
```json
{
	"input_names": [
		"Formica polyctena",
		"Formica exsectoides",
		"Formica pecefica"
	],
	"status_code": 200,
	"resolved_names": [
		{
			"matched_results": [
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Exact",
					"match_score": 1.0,
					"matched_name": "Formica polyctena",
					"search_string": "formica polyctena",
					"synonyms": [
						"Formica polyctenum",
						"Formica polyctena"
					],
					"taxon_id": 815730
				}
			],
			"input_name": "Formica polyctena"
		},
		{
			"matched_results": [
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Exact",
					"match_score": 1.0,
					"matched_name": "Formica exsectoides",
					"search_string": "formica exsectoides",
					"synonyms": [
						"Formica exsectoides"
					],
					"taxon_id": 3261265
				}
			],
			"input_name": "Formica exsectoides"
		}
	],
	"meta_data": {
		"execution_time": 0.79,
		"creation_time": "2017-10-18T18:56:40.441870",
		"source_urls": [
			"https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tnrs"
		]
	},
	"total_names": 2,
	"message": "Success"
}
```
2. 
```json
{
	"input_names": [
		"Pinus resionosa",
		"Meli officinalis"
	],
	"status_code": 200,
	"resolved_names": [
		{
			"matched_results": [
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Melissa officinalis",
					"search_string": "meli officinalis",
					"synonyms": [
						"Faucibarba officinalis",
						"Mutelia officinalis",
						"Thymus melissa",
						"Melissa officinalis"
					],
					"taxon_id": 355945
				},
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Fuzzy",
					"match_score": 0.8125,
					"matched_name": "Sepia officinalis",
					"search_string": "meli officinalis",
					"synonyms": [
						"Sepia zebrina",
						"Sepia mediterranea",
						"Sepia fischeri",
						"Sepia filliouxi",
						"Sepia officinalis",
						"Sepia vicellius",
						"Sepia rugosa",
						"Sepia officinalis subsp. mediterranea"
					],
					"taxon_id": 528817
				},
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Malva officinalis",
					"search_string": "meli officinalis",
					"synonyms": [
						"Althaea officinalis subsp. micrantha",
						"Althaea pulchra",
						"Althaea sublobata",
						"Althaea taurinensis",
						"Althaea officinalis var. pseudoarmeniaca",
						"Malva althaea",
						"Althaea officinalis subsp. pseudoarmeniaca",
						"Althaea officinalis",
						"Althaea villosa",
						"Althaea villosoides",
						"Althaea balearica",
						"Malva maritima",
						"Althaea micrantha",
						"Malva officinalis"
					],
					"taxon_id": 643492
				},
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Mutelia officinalis",
					"search_string": "meli officinalis",
					"synonyms": [
						"Faucibarba officinalis",
						"Mutelia officinalis",
						"Thymus melissa",
						"Melissa officinalis"
					],
					"taxon_id": 355945
				}
			],
			"input_name": "Meli officinalis"
		},
		{
			"matched_results": [
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Fuzzy",
					"match_score": 0.8571428571428571,
					"matched_name": "Pinus resinosa",
					"search_string": "pinus resionosa",
					"synonyms": [
						"Pinus resinosa",
						"Pinus rubra"
					],
					"taxon_id": 81207
				},
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Fuzzy",
					"match_score": 0.8571428571428571,
					"matched_name": "Pinus resinosa",
					"search_string": "pinus resionosa",
					"synonyms": [
						"Pinus hartwegii",
						"Pinus donnell-smithii",
						"Pinus frondosa",
						"Pinus tlamacaensis",
						"Pinus krelagii",
						"Pinus suffruticosa",
						"Pinus atrovirens",
						"Pinus corrugata",
						"Pinus montezumae var. hartwegii",
						"Pinus standishii",
						"Pinus roezlii",
						"Pinus lowii",
						"Pinus decaisneana var. wilsonii",
						"Pinus hartwegii var. rudis",
						"Pinus resinosa",
						"Pinus aculcensis",
						"Pinus wilsonii",
						"Pinus endlicheriana",
						"Pinus northumberlandiana",
						"Pinus robusta",
						"Pinus amecaensis",
						"Pinus lindleyana",
						"Pinus iztacihuatlii",
						"Pinus montezumae var. lindleyana",
						"Pinus papeleuii",
						"Pinus montezumae var. rudis",
						"Pinus ehrenbergii",
						"Pinus rudis",
						"Pinus scoparia",
						"Pinus decandolleana var. ehrenbergii",
						"Pinus montezumae subsp. hartwegii"
					],
					"taxon_id": 212471
				}
			],
			"input_name": "Pinus resionosa"
		}
	],
	"meta_data": {
		"execution_time": 5.41,
		"creation_time": "2017-10-18T19:49:25.143588",
		"source_urls": [
			"https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tnrs"
		]
	},
	"total_names": 2,
	"message": "Success"
}
```

__Alternative Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/names>

__HTTP Method:__ 		POST

__Input Format:__ 		application/json

__Output Format:__ 		application/json 


__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">scientific_names</span> 
  * __Category:__  	mandatory
  * __Data Type:__  list of strings
  * __Description:__  list of scientific names to be resolved.
 				
2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">fuzzy_match</span> 
  * __Category:__  	optional
  * __Data Type:__  boolean
  * __Description:__  a boolean value to specify whether to perform approximate string (a.k.a. "fuzzy") matching. By default, it is `false`. To turn on "fuzzy" matching `true` must be used. 

3. Parameter details:
  * __Name:__ 	 	<span style="color:blue">multiple_match</span> 
  * __Category:__  	optional
  * __Data Type:__  boolean
  * __Description:__  a boolean value to specify whether to return multiple match results when fuzzy matching is turned on. By default it is `false`. If fuzzy matching is turned on and _multiple_match_ is enabled (`true`), then the service will return results of matches with score more than `0.75`.
 				
__Example Commands/Requests:__

1. 
```bash
curl -X POST "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ot/names" -H "content-type:application/json" -d '{"scientific_names": ["Setophaga striata","Setophaga megnolia","Setophaga angilae","Setophaga plumbea","Setophaga virens"],"fuzzy_match":true}'
``` 

__Example Results:__

1. 
```json
{
	"input_names": [
		"Setophaga striata",
		"Setophaga megnolia",
		"Setophaga angilae",
		"Setophaga plumbea",
		"Setophaga virens"
	],
	"status_code": 200,
	"resolved_names": [
		{
			"matched_results": [
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Fuzzy",
					"match_score": 0.8888888888888888,
					"matched_name": "Setophaga magnolia",
					"search_string": "setophaga megnolia",
					"synonyms": [
						"Setophaga magnolia",
						"Dendroica magnolia",
						"? magnolia"
					],
					"taxon_id": 532751
				}
			],
			"input_name": "Setophaga megnolia"
		},
		{
			"matched_results": [
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Exact",
					"match_score": 1.0,
					"matched_name": "Setophaga plumbea",
					"search_string": "setophaga plumbea",
					"synonyms": [
						"Setophaga plumbea",
						"Dendroica plumbea"
					],
					"taxon_id": 45750
				}
			],
			"input_name": "Setophaga plumbea"
		},
		{
			"matched_results": [
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Fuzzy",
					"match_score": 0.8823529411764706,
					"matched_name": "Setophaga angelae",
					"search_string": "setophaga angilae",
					"synonyms": [
						"Dendroica angelae",
						"Setophaga angelae"
					],
					"taxon_id": 381849
				}
			],
			"input_name": "Setophaga angilae"
		},
		{
			"matched_results": [
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Exact",
					"match_score": 1.0,
					"matched_name": "Setophaga striata",
					"search_string": "setophaga striata",
					"synonyms": [
						"Dendroica striata",
						"? striata",
						"Setophaga striata"
					],
					"taxon_id": 60236
				}
			],
			"input_name": "Setophaga striata"
		},
		{
			"matched_results": [
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Exact",
					"match_score": 1.0,
					"matched_name": "Setophaga virens",
					"search_string": "setophaga virens",
					"synonyms": [
						"Dendroica virens subsp. virens",
						"? virens",
						"Dendroica virens",
						"Dendroica virens subsp. waynei",
						"Setophaga virens"
					],
					"taxon_id": 1014098
				}
			],
			"input_name": "Setophaga virens"
		}
	],
	"meta_data": {
		"execution_time": 6.00,
		"creation_time": "2017-10-18T20:12:15.171086",
		"source_urls": [
			"https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tnrs"
		]
	},
	"total_names": 5,
	"message": "Success"
}
```

__Citation/Source:__  	 		https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tnrs

__Service Quality:__

 * *Restrictions on capacity:*  __maximum `1000` names allowed__
 * *Restrictions on scope:*     __unknown__ 
 * *Expected response time:*  	__1s~30s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. sc_name) | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /name)   | 404             | Error: Could not find the requested resource URI |
   | Reached maximum input limit                        | 403             | Error: Currently more than 1000 names is not supported |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_resolved_names_) will be an empty list.

---

__Service Name:__  	 		GNR_TNRS_wrapper

__Service Description:__ 	A service which resolves scientific names against known taxonomy sources using Global Names Resolution services.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/gnr/resolve>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json

__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">names</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  one or more scientific names to be resolved delimited by pipe "|".
 				
2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">fuzzy_match</span> 
  * __Category:__  	optional
  * __Data Type:__  boolean
  * __Description:__  a boolean value to specify whether to perform approximate string (a.k.a. "fuzzy") matching. By default, it is `false`. To turn on "fuzzy" matching `true` must be used. 

3. Parameter details:
  * __Name:__ 	 	<span style="color:blue">multiple_match</span> 
  * __Category:__  	optional
  * __Data Type:__  boolean
  * __Description:__  a boolean value to specify whether to return multiple match results when fuzzy matching is turned on. By default it is `false`. If fuzzy matching is turned on and _multiple_match_ is enabled (`true`), then the service will return results of matches with score more than `0.75`.
 				
__Example Commands/Requests:__

1. 

```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/gnr/resolve?names=Formica%20pecefica&fuzzy_match=true&multiple_match=true
```

__Example Results:__

1. 

```json
{
	"input_names": [
		"Formica pecefica"
	],
	"status_code": 200,
	"resolved_names": [
		{
			"matched_results": [
				{
					"data_source": "Catalogue of Life",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "2f41fe085d8ff5d5bb75e520d0a692de"
				},
				{
					"data_source": "ITIS",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "576854"
				},
				{
					"data_source": "NCBI",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "609847"
				},
				{
					"data_source": "Interim Register of Marine and Nonmarine Genera",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "10920253"
				},
				{
					"data_source": "GBIF Backbone Taxonomy",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "1315056"
				},
				{
					"data_source": "EOL",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "33847491"
				},
				{
					"data_source": "EOL",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "20639408"
				},
				{
					"data_source": "EOL",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "28015733"
				},
				{
					"data_source": "AntWeb",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "105695350"
				},
				{
					"data_source": "nlbif",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "131429640"
				},
				{
					"data_source": "Index to Organism Names",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "126834498"
				},
				{
					"data_source": "Index to Organism Names",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "127538181"
				},
				{
					"data_source": "uBio NameBank",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "94022877"
				},
				{
					"data_source": "uBio NameBank",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "95837151"
				},
				{
					"data_source": "uBio NameBank",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "102401655"
				},
				{
					"data_source": "Arctos",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "1951521"
				},
				{
					"data_source": "Open Tree of Life Reference Taxonomy",
					"match_type": "Fuzzy",
					"match_score": 0.75,
					"matched_name": "Formica pacifica",
					"search_string": "Formica pecefica",
					"synonyms": [],
					"taxon_id": "3261024"
				}
			],
			"input_name": "Formica pecefica"
		}
	],
	"meta_data": {
		"execution_time": 0.54,
		"creation_time": "2017-10-18T21:25:32.366358",
		"source_urls": [
			"http://resolver.globalnames.org/"
		]
	},
	"total_names": 1,
	"gnr_parameters": {
		"with_vernaculars": false,
		"best_match_only": false,
		"data_sources": [],
		"with_context": false,
		"header_only": false,
		"resolve_once": false,
		"preferred_data_sources": [],
		"with_canonical_ranks": false
	},
	"message": "Success"
}
```

__Alternative Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/gnr/names>

__HTTP Method:__ 		POST

__Input Format:__ 		application/json

__Output Format:__ 		application/json 


__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">scientific_names</span> 
  * __Category:__  	mandatory
  * __Data Type:__  list of strings
  * __Description:__  list of scientific names to be resolved.
 				
2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">fuzzy_match</span> 
  * __Category:__  	optional
  * __Data Type:__  boolean
  * __Description:__  a boolean value to specify whether to perform approximate string (a.k.a. "fuzzy") matching. By default, it is `false`. To turn on "fuzzy" matching `true` must be used. 

3. Parameter details:
  * __Name:__ 	 	<span style="color:blue">multiple_match</span> 
  * __Category:__  	optional
  * __Data Type:__  boolean
  * __Description:__  a boolean value to specify whether to return multiple match results when fuzzy matching is turned on. By default it is `false`. If fuzzy matching is turned on and _multiple_match_ is enabled (`true`), then the service will return results of matches with score more than `0.75`.
 				
__Example Commands/Requests:__

1. 
```bash
curl -X POST "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/gnr/names" -H "content-type:application/json" -d '{"scientific_names": ["Rana Temporaria"],"fuzzy_match":true, "multiple_match":false}'
``` 

__Example Results:__

1. 
```json
{
	"input_names": [
		"Rana Temporaria"
	],
	"status_code": 200,
	"resolved_names": [
		{
			"matched_results": [
				{
					"data_source": "NCBI",
					"match_type": "Exact",
					"match_score": 0.988,
					"matched_name": "Rana temporaria",
					"search_string": "Rana Temporaria",
					"synonyms": [],
					"taxon_id": "8407"
				}
			],
			"input_name": "Rana Temporaria"
		}
	],
	"meta_data": {
		"execution_time": 0.74,
		"creation_time": "2017-10-18T21:51:58.633393",
		"source_urls": [
			"http://resolver.globalnames.org/"
		]
	},
	"total_names": 1,
	"gnr_parameters": {
		"with_vernaculars": false,
		"best_match_only": false,
		"data_sources": [],
		"with_context": false,
		"header_only": false,
		"resolve_once": false,
		"preferred_data_sources": [],
		"with_canonical_ranks": false
	},
	"message": "Success"
}
```

__Citation/Source:__		http://resolver.globalnames.org/

__Service Quality:__

 * *Restrictions on capacity:*  __maximum `1000` names allowed__
 * *Restrictions on scope:*     __unknown__ 
 * *Expected response time:*  	__1s~30s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. sc_name) | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /name)   | 404             | Error: Could not find the requested resource URI |
   | Reached maximum input limit/capacity               | 403             | Error: Currently more than 1000 names is not supported |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_resolved_names_) will be an empty list.

---

## <a name="treeretrieval"></a>Phylogenetic Tree Retrieval

__Service Name:__  	 		OToL_wrapper_Tree

__Service Description:__ 	A service to get Phylogenetic Trees from a list of taxa using Open Tree of Life's induced_subtree method.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/get_tree>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json

__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">taxa</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  one or more scientific names delimited by pipe "|".
 				
 				
__Example Commands/Requests:__

1. 

```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/get_tree?taxa=Crabronidae|Ophiocordyceps|Megalyridae|Formica polyctena|Tetramorium caespitum|Pseudomyrmex|Carebara diversa|Formicinae
```

__Example Results:__

1. 
```json
{
	"status_code": 200,
	"message": "Success",
	"meta_data": {
		"execution_time": 6.61,
		"creation_time": "2017-10-18T22:11:59.502157",
		"source_urls": [
			"https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tree_of_life"
		]
	},
	"tree_metadata": {
		"alignment_method": "NA",
		"character_matrix": "NA",
		"rooted": true,
		"supporting_studies": [],
		"anastomosing": false,
		"branch_lengths_type": null,
		"consensus_type": "NA",
		"inference_method": "induced_subtree from synthetic tree with ID opentree9.1",
		"branch_support_type": null,
		"num_tips": 6,
		"gene_or_species": "species",
		"topology_id": "NA",
		"synthetic_tree_id": "opentree9.1"
	},
	"newick": "((Crabronidae_ott372234,(((Formica_polyctena_ott815730)Formicinae_ott614614,(Tetramorium_caespitum_ott214421,Carebara_diversa_ott842045)),Pseudomyrmex_ott412943))Aculeata_ott206138,Megalyridae_ott840287);"
}
```

__Alternative Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/tree>

__HTTP Method:__ 		POST

__Input Format:__ 		application/json

__Output Format:__ 		application/json 


__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">taxa</span> 
  * __Category:__  	mandatory
  * __Data Type:__  list of strings
  * __Description:__ list of scientific names.
 				
 				
__Example Commands/Requests:__

1. 
```bash
curl -X POST "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/tree" -H "content-type:application/json" -d '{"taxa": ["Setophaga striata","Setophaga magnolia","Setophaga angelae","Setophaga plumbea","Setophaga virens"]}'
``` 

__Example Results:__

1. 

```
{
	"status_code": 200,
	"message": "Success",
	"meta_data": {
		"execution_time": 7.61,
		"creation_time": "2017-10-18T22:57:19.406397",
		"source_urls": [
			"https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tree_of_life"
		]
	},
	"tree_metadata": {
		"alignment_method": "NA",
		"character_matrix": "NA",
		"rooted": true,
		"supporting_studies": [],
		"anastomosing": false,
		"branch_lengths_type": null,
		"consensus_type": "NA",
		"inference_method": "induced_subtree from synthetic tree with ID opentree9.1",
		"branch_support_type": null,
		"num_tips": 5,
		"gene_or_species": "species",
		"topology_id": "NA",
		"synthetic_tree_id": "opentree9.1"
	},
	"newick": "(Setophaga_magnolia_ott532751,Setophaga_striata_ott60236,Setophaga_plumbea_ott45750,Setophaga_angelae_ott381849,Setophaga_virens_ott1014098)Setophaga_ott285198;"
}
```

__Citation/Source:__		https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#tree_of_life

__Service Quality:__

 * *Restrictions on capacity:*  __maximum `1000` taxa allowed__
 * *Restrictions on scope:*     __unknown__ 
 * *Expected response time:*  	__1s~30s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. tax)     | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /get_tre)| 404             | Error: Could not find the requested resource URI |
   | Reached maximum input limit                        | 403             | Error: Currently more than 1000 taxa is not supported |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_newick_) will be an empty string.

---

__Service Name:__  	 		Phylomatic_wrapper_Tree

__Service Description:__ 	A service to get Phylogenetic Trees from a list of taxa using Phylomatic service.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pm/get_tree>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json

__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">taxa</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  one or more scientific names delimited by pipe "|".
 				
 				
__Example Commands/Requests:__

1. 

```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pm/get_tree?taxa=Panthera leo|Panthera onca|Panthera tigris|Panthera uncia
```

__Example Results:__

1. 
```json
{
	"status_code": 200,
	"message": "Success",
	"meta_data": {
		"execution_time": 4.81,
		"creation_time": "2017-10-18T23:27:24.903835",
		"source_urls": [
			"http://phylodiversity.net/phylomatic/"
		]
	},
	"input_taxa": [
		"Panthera leo",
		"Panthera onca",
		"Panthera tigris",
		"Panthera uncia"
	],
	"newick": "((Panthera_leo:6.3,Panthera_onca:6.3):0.1,Panthera_tigris:6.4):159.8;"
}
```

__Alternative Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pm/tree>

__HTTP Method:__ 		POST

__Input Format:__ 		application/json

__Output Format:__ 		application/json 


__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">taxa</span> 
  * __Category:__  	mandatory
  * __Data Type:__  list of strings
  * __Description:__ list of scientific names.
 				
 				
__Example Commands/Requests:__

1. 
```bash
curl -X POST "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pm/tree" -H "content-type:application/json" -d '{"taxa": ["Helianthus annuus","Passiflora edulis", "Rosa arkansana", "Saccharomyces cerevisiae"]}'
``` 

__Example Results:__

1. 

```
{
	"status_code": 200,
	"message": "Success",
	"meta_data": {
		"execution_time": 3.59,
		"creation_time": "2017-10-18T23:29:51.576322",
		"source_urls": [
			"http://phylodiversity.net/phylomatic/"
		]
	},
	"input_taxa": [
		"Helianthus annuus",
		"Passiflora edulis",
		"Rosa arkansana",
		"Saccharomyces cerevisiae"
	],
	"newick": "(Helianthus_annuus,(Rosa_arkansana,Passiflora_edulis));"
}
```

__Citation/Source:__		

- http://phylodiversity.net/phylomatic/
- https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#taxonomy

__Service Quality:__

 * *Restrictions on capacity:*  __maximum `1000` taxa allowed__
 * *Restrictions on scope:*     __unknown__ 
 * *Expected response time:*  	__1s~30s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. tax)     | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /get_tre)| 404             | Error: Could not find the requested resource URI |
   | Reached maximum input limit                        | 403             | Error: Currently more than 1000 taxa is not supported |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_newick_) will be an empty string.

---

__Service Name:__  	 		PhyloT_wrapper_Tree

__Service Description:__ 	A service to get Phylogenetic Trees (based on NCBI taxonomy) from a list of taxa using phyloT.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pt/get_tree>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json

__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">taxa</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  one or more scientific names delimited by pipe "|".
 				
 				
__Example Commands/Requests:__

1. 

```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pt/get_tree?taxa=Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens
```

__Example Results:__

1. 
```json
{
	"status_code": 200,
	"message": "Success",
	"meta_data": {
		"execution_time": 9.08,
		"creation_time": "2017-10-18T23:37:03.449076",
		"source_urls": [
			"http://phylot.biobyte.de/"
		]
	},
	"input_taxa": [
		"Setophaga striata",
		"Setophaga magnolia",
		"Setophaga angelae",
		"Setophaga plumbea",
		"Setophaga virens"
	],
	"newick": "(Setophaga_virens,Setophaga_angelae,Setophaga_plumbea,Setophaga_striata,Setophaga_magnolia);"
}
```

__Alternative Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pt/tree>

__HTTP Method:__ 		POST

__Input Format:__ 		application/json

__Output Format:__ 		application/json 


__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">taxa</span> 
  * __Category:__  	mandatory
  * __Data Type:__  list of strings
  * __Description:__ list of scientific names.
 				
 				
__Example Commands/Requests:__

1. 
```bash
curl -X POST "http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pt/tree" -H "content-type:application/json" -d '{"taxa": ["Aix sponsa", "Anas acuta", "Anas americana", "Aythya americana", "Branta canadensis","Bucephala albeola", "Dendrocygna autumnalis", "Dendrocygna bicolor"]}'
``` 

__Example Results:__

1. 

```
{
	"status_code": 200,
	"message": "Success",
	"meta_data": {
		"execution_time": 9.60,
		"creation_time": "2017-10-18T23:45:45.493155",
		"source_urls": [
			"http://phylot.biobyte.de/"
		]
	},
	"input_taxa": [
		"Aix sponsa",
		"Anas acuta",
		"Anas americana",
		"Aythya americana",
		"Branta canadensis",
		"Bucephala albeola",
		"Dendrocygna autumnalis",
		"Dendrocygna bicolor"
	],
	"newick": "((Bucephala_albeola),(Aythya_americana),(Aix_sponsa),(Branta_canadensis),(Anas_acuta),(Anas_americana),(Dendrocygna_autumnalis,Dendrocygna_bicolor));"
}
```

__Citation/Source:__		http://phylot.biobyte.de/

__Service Quality:__

 * *Restrictions on capacity:*  __maximum `250` taxa allowed__ 
 * *Expected response time:*  	__1s~30s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. tax)     | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /get_tre)| 404             | Error: Could not find the requested resource URI |
   | Reached maximum input limit                        | 403             | Error: Currently more than 250 taxa is not supported |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_newick_) will be an empty string.

---

## <a name='taxonspecies'></a>Taxon to Species

__Service Name:__  	 	Taxon_all_species

__Service Description:__ 	A service to get all Species that belong to a particular Taxon.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/all_species>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">taxon</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  name of a taxon.
 				
 				
__Example Commands/Requests:__

1. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/all_species?taxon=Vulpes
```

2. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/all_species?taxon=Canidae
```

__Example Results:__

1. 
```json
{
	"status_code": 200,
	"input_taxon": "Vulpes",
	"meta_data": {
		"execution_time": 1.16,
		"creation_time": "2017-10-19T07:25:03.918115",
		"source_urls": [
			"https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-Taxonomy"
		]
	},
	"total_names": 15,
	"message": "Success",
	"species": [
		"Vulpes environmental sample",
		"Vulpes stenognathus",
		"Vulpes bengalensis",
		"Vulpes pallida",
		"Vulpes cana",
		"Vulpes chama",
		"Vulpes vulpes",
		"Vulpes lagopus",
		"Vulpes corsac",
		"Vulpes rueppellii",
		"Vulpes zerda",
		"Vulpes velox",
		"Vulpes macrotis",
		"Vulpes sp.",
		"Vulpes ferrilata"
	]
}
```
2. 
```json
{
	"status_code": 200,
	"input_taxon": "Canidae",
	"meta_data": {
		"execution_time": 5.87,
		"creation_time": "2017-10-19T07:25:50.754427",
		"source_urls": [
			"https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-Taxonomy"
		]
	},
	"total_names": 166,
	"message": "Success",
	"species": [
		"Aelurodon taxoides",
		"Aelurodon asthenostylus",
		"Aelurodon ferox",
		"Aelurodon montanensis",
		"Aelurodon mcgrewi",
		"Aelurodon stirtoni",
		"Cynotherium sardous",
		"Rhizocyon oregonensis",
		"Paratomarctus temerarius",
		"Paratomarctus euthos",
		"Archaeocyon pavidus",
		"Archaeocyon leptodus",
		"Archaeocyon falkenbachi",
		"Metatomarctus canavus",
		"Psalidocyon marianae",
		"Protomarctus optatus",
		"Neocynodesmus delicatus",
		"Protepicyon raki",
		"Desmocyon matthewi",
		"Desmocyon thomsoni",
		"Paracynarctus kelloggi",
		"Paracynarctus sinclairi",
		"Microtomarctus conferta",
		"Otarocyon cooki",
		"Otarocyon macdonaldi",
		"Paraenhydrocyon robustus",
		"Paraenhydrocyon josephi",
		"Sunkahetanka geringensis",
		"Procynodictis vulpiceps",
		"Procynodictis progressus",
		"Hesperocyon gregorious",
		"Hesperocyon coloradensis",
		"Hesperocyon gregarius",
		"Euoplocyon spissidens",
		"Euoplocyon brachygnathus",
		"Philotrox condoni",
		"Leptocyon vulpinus",
		"Leptocyon gregorii",
		"Leptocyon vafer",
		"Carpocyon limosus",
		"Carpocyon robustus",
		"Carpocyon webbi",
		"Carpocyon compressus",
		"Ectopocynus intermedius",
		"Ectopocynus simplicidens",
		"Ectopocynus antiquus",
		"Osbornodon iamonensis",
		"Osbornodon brachypus",
		"Osbornodon scitulus",
		"Osbornodon renjiei",
		"Osbornodon wangi",
		"Osbornodon sesnoni",
		"Osbornodon fricki",
		"Epicyon haydeni",
		"Epicyon aelurodontoides",
		"Epicyon saevus",
		"Eucyon davisi",
		"Cormocyon copei",
		"Cormocyon haydeni",
		"Cerdocyon thous",
		"Borophagus pugnator",
		"Borophagus hilli",
		"Borophagus littoralis",
		"Borophagus diversidens",
		"Borophagus secundus",
		"Borophagus orc",
		"Borophagus dudleyi",
		"Borophagus parvus",
		"Cynarctoides harlowi",
		"Cynarctoides roii",
		"Cynarctoides acridens",
		"Cynarctoides gawnae",
		"Cynarctoides lemur",
		"Cynarctoides luskensis",
		"Cynarctoides emryi",
		"Prohesperocyon wilsoni",
		"Tomartus euthos",
		"Tomarctus brevirostris",
		"Tomarctus hippophaga",
		"Phlaocyon achoros",
		"Phlaocyon minor",
		"Phlaocyon leucosteus",
		"Phlaocyon latidens",
		"Phlaocyon marslandensis",
		"Phlaocyon yatkolai",
		"Phlaocyon multicuspus",
		"Phlaocyon mariae",
		"Phlaocyon annectens",
		"Phlaocyon taylori",
		"Mesocyon temnodon",
		"Mesocyon coryphaeus",
		"Mesocyon brachyops",
		"Cynodesmus thooides",
		"Cynodesmus martini",
		"Oxetocyon cuspidatus",
		"Enhydrocyon pahinsintewakpa",
		"Enhydrocyon basilatus",
		"Enhydrocyon crassidens",
		"Enhydrocyon stenocephalus",
		"Caedocyon tedfordi",
		"Cynarctus voorhiesi",
		"Cynarctus marylandica",
		"Cynarctus crucidens",
		"Cynarctus galushai",
		"Cynarctus saxatilis",
		"Lycalopex sp. Fuegian dog",
		"Lycalopex fulvipes",
		"Lycalopex gymnocercus",
		"Lycalopex griseus",
		"Lycalopex culpaeus",
		"Lycalopex vetulus",
		"Lycalopex sechurae",
		"Cuon texanus",
		"Cuon alpinus",
		"Vulpes environmental sample",
		"Vulpes stenognathus",
		"Vulpes bengalensis",
		"Vulpes pallida",
		"Vulpes cana",
		"Vulpes chama",
		"Vulpes vulpes",
		"Vulpes lagopus",
		"Vulpes corsac",
		"Vulpes rueppellii",
		"Vulpes zerda",
		"Vulpes velox",
		"Vulpes macrotis",
		"Vulpes sp.",
		"Vulpes ferrilata",
		"Otocyon megalotis",
		"Lycaon pictus",
		"Speothos venaticus",
		"Atelocynus microtis",
		"Chrysocyon brachyurus",
		"Nyctereutes abdeslami",
		"Nyctereutes procyonoides",
		"Canis anthus",
		"Canis sp. Russia/33,500",
		"Canis sp. Belgium/36,000",
		"Canis environmental sample",
		"Canis spelaeus",
		"Canis hyaena",
		"Canis primigenius",
		"Canis cedazoensis",
		"Canis apolloniensis",
		"Canis edwardii",
		"Canis alopex",
		"Canis dirus",
		"Canis ferox",
		"Canis armbrusteri",
		"Canis lepophagus",
		"Canis lycaon",
		"Canis simensis",
		"Canis mesomelas",
		"Canis aureus",
		"Canis adustus",
		"Canis sp. CANInt1",
		"Canis lupus",
		"Canis latrans",
		"Canis sp.",
		"Canis rufus",
		"Urocyon progressus",
		"Urocyon cinereoargenteus",
		"Urocyon littoralis",
		"Dusicyon avus",
		"Dusicyon australis"
	]
}
```

__Citation/Source:__  	 	
- https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#taxonomy

__Service Quality:__

 * *Restrictions on capacity:*  __maximum taxonomic rank allowed: `family`__
 * *Expected response time:*  	__1s~20s__ (_might be longer depending on the rank of input taxon_)
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. tax)     | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /all_sp) | 404             | Error: Could not find the requested resource URI |
   | Reached maximum input limit                        | 403         | Error: Currently input taxon with '_rank name_' rank is not supported |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_species_) will be an empty list.

---

__Service Name:__  	 	Taxon_country_species

__Service Description:__ 	A service to get a set of Species that belong to a particular Taxon and established in a particular country using INaturalist services.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/country_species>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">taxon</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  name of a taxon.
 				
2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">taxon</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  name of a country.

 				
__Example Commands/Requests:__

1. 
```json
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/country_species?taxon=Panthera&country=Bangladesh
```
2. 
```json
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/country_species?taxon=Vulpes&country=Nepal
```

__Example Results:__

1. 
```json
{
	"status_code": 200,
	"input_country": "Bangladesh",
	"meta_data": {
		"execution_time": 0.97,
		"creation_time": "2017-10-19T07:53:43.968268",
		"source_urls": [
			"https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-Taxonomy",
			"https://www.inaturalist.org"
		]
	},
	"total_names": 1,
	"message": "Success",
	"species": [
		"Panthera tigris"
	],
	"input_taxon": "Panthera"
}
```

2. 
```json
{
	"status_code": 200,
	"input_country": "Nepal",
	"meta_data": {
		"execution_time": 0.49,
		"creation_time": "2017-10-19T07:56:17.137755",
		"source_urls": [
			"https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-Taxonomy",
			"https://www.inaturalist.org"
		]
	},
	"total_names": 2,
	"message": "Success",
	"species": [
		"Vulpes bengalensis",
		"Vulpes ferrilata"
	],
	"input_taxon": "Vulpes"
}
```

__Citation/Source:__  	 	

- https://github.com/OpenTreeOfLife/opentree/wiki/Open-Tree-of-Life-APIs#taxonomy
- http://www.inaturalist.org/pages/api+reference#get-places


__Service Quality:__

 * *Restrictions on capacity:*  __maximum taxonomic rank allowed: `family`__ 
 * *Expected response time:*  	__1s~30s__ (_might be longer depending on the rank of input taxon_)
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. tax)     | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /coun_sp)| 404             | Error: Could not find the requested resource URI |
   | Reached maximum input limit                        | 403         | Error: Currently input taxon with '_rank name_' rank is not supported |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_species_) will be an empty list.

---


__Service Name:__  	 	Taxon_genome_species

__Service Description:__ 	A service to get a set of Species that belong to a particular Taxon and have genome sequence in NCBI database.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/ncbi/genome_species>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">taxon</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  name of a taxon.
 				
 				
__Example Commands/Requests:__

1. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/ncbi/genome_species?taxon=Rodentia
```
2. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/ncbi/genome_species?taxon=Columbidae
```
3. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/ts/ncbi/genome_species?taxon=Aves
```

__Example Results:__

1. 
```json
{
	"status_code": 200,
	"meta_data": {
		"execution_time": 3.46,
		"creation_time": "2017-10-19T10:13:05.479535",
		"source_urls": [
			"https://www.ncbi.nlm.nih.gov/taxonomy",
			"https://www.ncbi.nlm.nih.gov/genome"
		]
	},
	"total_names": 38,
	"message": "Success",
	"species": [
		"Nannospalax galili",
		"Fukomys damarensis",
		"Myodes glareolus",
		"Ellobius talpinus",
		"Peromyscus maniculatus bairdii",
		"Apodemus speciosus",
		"Spermophilus dauricus",
		"Microtus ochrogaster",
		"Mus musculus molossinus",
		"Neotoma lepida",
		"Castor canadensis",
		"Jaculus jaculus",
		"Psammomys obesus",
		"Ictidomys tridecemlineatus",
		"Mus musculus musculus",
		"Ellobius lutescens",
		"Cavia aperea",
		"Chinchilla lanigera",
		"Microtus agrestis",
		"Heterocephalus glaber",
		"Octodon degus",
		"Cavia porcellus",
		"Apodemus sylvaticus",
		"Rattus norvegicus",
		"Mus spretus",
		"Mus pahari",
		"Mus musculus domesticus",
		"Mus musculus castaneus",
		"Mus musculus",
		"Mus caroli",
		"Meriones unguiculatus",
		"Phodopus sungorus",
		"Peromyscus maniculatus",
		"Mesocricetus auratus",
		"Cricetulus griseus",
		"Dipodomys ordii",
		"Marmota marmota marmota",
		"Marmota marmota"
	],
	"input_taxon": "Rodentia"
}
```

2. 
```json
{
	"status_code": 200,
	"meta_data": {
		"execution_time": 3.17,
		"creation_time": "2017-10-19T10:11:00.465616",
		"source_urls": [
			"https://www.ncbi.nlm.nih.gov/taxonomy",
			"https://www.ncbi.nlm.nih.gov/genome"
		]
	},
	"total_names": 3,
	"message": "Success",
	"species": [
		"Patagioenas fasciata monilis",
		"Patagioenas fasciata",
		"Columba livia"
	],
	"input_taxon": "Columbidae"
}
```

3. 
```json
{
	"status_code": 200,
	"meta_data": {
		"execution_time": 3.96,
		"creation_time": "2017-10-19T11:02:14.958038",
		"source_urls": [
			"https://www.ncbi.nlm.nih.gov/taxonomy",
			"https://www.ncbi.nlm.nih.gov/genome"
		]
	},
	"total_names": 105,
	"message": "Success",
	"species": [
		"Lyrurus tetrix",
		"Zosterops lateralis melanops",
		"Setophaga coronata coronata",
		"Corvus cornix cornix",
		"Balearica regulorum",
		"Gallirallus okinawae",
		"Nannopterum harrisi",
		"Struthio camelus australis",
		"Anser cygnoides domesticus",
		"Patagioenas fasciata monilis",
		"Patagioenas fasciata",
		"Podiceps cristatus",
		"Falco cherrug",
		"Manacus vitellinus",
		"Lepidothrix coronata",
		"Lonchura striata domestica",
		"Antrostomus carolinensis",
		"Sporophila hypoxantha",
		"Amazona vittata",
		"Pterocles gutturalis",
		"Aquila chrysaetos canadensis",
		"Tympanuchus cupido pinnatus",
		"Phylloscopus trochilus acredula",
		"Apteryx australis mantelli",
		"Calidris pugnax",
		"Egretta garzetta",
		"Leptosomus discolor",
		"Chlamydotis macqueenii",
		"Pseudopodoces humilis",
		"Corvus cornix",
		"Nestor notabilis",
		"Ara macao",
		"Buceros rhinoceros silvestris",
		"Buceros rhinoceros",
		"Lyrurus tetrix tetrix",
		"Phylloscopus trochiloides viridanus",
		"Phylloscopus trochiloides trochiloides",
		"Nipponia nippon",
		"Tauraco erythrolophus",
		"Picoides pubescens",
		"Setophaga coronata",
		"Balearica regulorum gibbericeps",
		"Phaethon lepturus",
		"Tinamus guttatus",
		"Coturnix japonica",
		"Corvus brachyrhynchos",
		"Anas zonorhyncha",
		"Ficedula albicollis",
		"Taeniopygia guttata",
		"Merops nubicus",
		"Colius striatus",
		"Apaloderma vittatum",
		"Acanthisitta chloris",
		"Phylloscopus plumbeitarsus",
		"Tyto alba",
		"Urile pelagicus",
		"Nannopterum auritus",
		"Cuculus canorus",
		"Eurypyga helias",
		"Cariama cristata",
		"Mesitornis unicolor",
		"Ciconia boyciana",
		"Haliaeetus leucocephalus",
		"Charadrius vociferus",
		"Geospiza fortis",
		"Passer domesticus",
		"Phylloscopus trochiloides",
		"Zonotrichia albicollis",
		"Zosterops lateralis",
		"Cathartes aura",
		"Lonchura striata",
		"Nannopterum brasilianus",
		"Gavia stellata",
		"Pelecanus crispus",
		"Fulmarus glacialis",
		"Opisthocomus hoazin",
		"Grus japonensis",
		"Uria lomvia",
		"Melopsittacus undulatus",
		"Amazona aestiva",
		"Calypte anna",
		"Pygoscelis adeliae",
		"Aptenodytes forsteri",
		"Phoenicopterus ruber ruber",
		"Phoenicopterus ruber",
		"Phalacrocorax carbo",
		"Phylloscopus trochilus",
		"Sturnus vulgaris",
		"Parus major",
		"Serinus canaria",
		"Meleagris gallopavo",
		"Gallus gallus",
		"Colinus virginianus",
		"Callipepla squamata",
		"Tympanuchus cupido",
		"Numida meleagris",
		"Haliaeetus albicilla",
		"Aquila chrysaetos",
		"Falco peregrinus",
		"Columba livia",
		"Chaetura pelagica",
		"Anser cygnoides",
		"Anas platyrhynchos",
		"Apteryx australis",
		"Struthio camelus"
	],
	"input_taxon": "Aves"
}
```

__Citation/Source:__  	

- https://www.ncbi.nlm.nih.gov/taxonomy
- https://www.ncbi.nlm.nih.gov/genome
- http://www.ncbi.nlm.nih.gov/books/NBK25500/#chapter1.Finding_Related_Data_Through_En


__Service Quality:__

 * *Restrictions on capacity:*  __unknown__ (_depends on the source web service. Tested upto __class__ ranked taxon as input_) 
 * *Expected response time:*  	__1s~20s__ (_might be longer depending on the rank of taxon_)
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. tax)     | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /gene_sp)| 404             | Error: Could not find the requested resource URI |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_species_) will be an empty list.

---

## <a name='imageinforetrieval'></a>Image/Information URL Retrieval

__Service Name:__  	 	Image_url_species

__Service Description:__ 	A service to get image urls and corresponding license information of a list of species using EOL services.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/get_images>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">species</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  list of species names delimited by pipe "|".
 				
  > __Note__: The service expects already resolved species names as input to provide the correct output.

__Example Commands/Requests:__

1. 

```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/get_images?species=Panthera%20leo|Panthera%20onca|Panthera%20pardus
```


__Example Results:__

1. 
```json
{
	"input_species": [
		"Panthera leo",
		"Panthera onca",
		"Panthera pardus"
	],
	"status_code": 200,
	"message": "Success",
	"meta_data": {
		"execution_time": 3.12,
		"creation_time": "2017-10-21T08:58:51.049382",
		"source_urls": [
			"http://eol.org"
		]
	},
	"species": [
		{
			"images": [
				{
					"license": "http://creativecommons.org/licenses/by-sa/2.0/",
					"mediaURL": "http://upload.wikimedia.org/wikipedia/commons/e/ec/Lion_cub_with_mother.jpg",
					"eolMediaURL": "http://media.eol.org/content/2015/11/13/05/46343_orig.jpg",
					"rightsHolder": "",
					"vettedStatus": "Trusted",
					"source": "http://commons.wikimedia.org/wiki/File:Lion_cub_with_mother.jpg",
					"eolThumbnailURL": "http://media.eol.org/content/2015/11/13/05/46343_98_68.jpg",
					"dataRating": 4.83333
				},
				{
					"license": "http://creativecommons.org/publicdomain/mark/1.0/",
					"mediaURL": "http://upload.wikimedia.org/wikipedia/commons/a/ae/Lion_Yawning.jpg",
					"eolMediaURL": "http://media.eol.org/content/2016/04/26/05/84896_orig.jpg",
					"rightsHolder": "",
					"vettedStatus": "Trusted",
					"source": "http://commons.wikimedia.org/wiki/File:Lion_Yawning.jpg",
					"eolThumbnailURL": "http://media.eol.org/content/2016/04/26/05/84896_98_68.jpg",
					"dataRating": 4.5
				},
				{
					"license": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
					"mediaURL": "https://farm5.staticflickr.com/4093/4888050484_fba7e481cd_o.jpg",
					"eolMediaURL": "http://media.eol.org/content/2015/04/30/12/90034_orig.jpg",
					"rightsHolder": "David d'O",
					"vettedStatus": "Trusted",
					"source": "https://www.flickr.com/photos/david_o/4888050484/",
					"eolThumbnailURL": "http://media.eol.org/content/2015/04/30/12/90034_98_68.jpg",
					"dataRating": 4.44444
				},
				{
					"license": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
					"mediaURL": "http://farm5.staticflickr.com/4093/4888050484_fba7e481cd_o.jpg",
					"eolMediaURL": "http://media.eol.org/content/2013/03/03/00/50308_orig.jpg",
					"rightsHolder": "David d'O",
					"vettedStatus": "Trusted",
					"source": "http://www.flickr.com/photos/david_o/4888050484/",
					"eolThumbnailURL": "http://media.eol.org/content/2013/03/03/00/50308_98_68.jpg",
					"dataRating": 4.44444
				},
				{
					"license": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
					"mediaURL": "https://farm5.staticflickr.com/4093/4887455027_dae2d6ce69_o.jpg",
					"eolMediaURL": "http://media.eol.org/content/2015/04/30/12/35649_orig.jpg",
					"rightsHolder": "David d'O",
					"vettedStatus": "Trusted",
					"source": "https://www.flickr.com/photos/david_o/4887455027/",
					"eolThumbnailURL": "http://media.eol.org/content/2015/04/30/12/35649_98_68.jpg",
					"dataRating": 4.375
				}
			],
			"searched_name": "Panthera leo",
			"total_images": 5,
			"eol_id": 328672,
			"matched_name": "Panthera leo (Linnaeus, 1758)"
		},
		{
			"images": [
				{
					"license": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
					"mediaURL": "https://farm5.staticflickr.com/4085/5177235312_9f03063e0d_o.jpg",
					"eolMediaURL": "http://media.eol.org/content/2015/04/30/02/29576_orig.jpg",
					"rightsHolder": "Smithsonian Wild",
					"vettedStatus": "Trusted",
					"source": "https://www.flickr.com/photos/smithsonianwild/5177235312/",
					"eolThumbnailURL": "http://media.eol.org/content/2015/04/30/02/29576_98_68.jpg",
					"dataRating": 4.30769
				},
				{
					"license": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
					"mediaURL": "http://farm5.staticflickr.com/4085/5177235312_9f03063e0d_o.jpg",
					"eolMediaURL": "http://media.eol.org/content/2013/07/05/09/54909_orig.jpg",
					"rightsHolder": "Smithsonian Wild",
					"vettedStatus": "Trusted",
					"source": "http://www.flickr.com/photos/smithsonianwild/5177235312/",
					"eolThumbnailURL": "http://media.eol.org/content/2013/07/05/09/54909_98_68.jpg",
					"dataRating": 4.30769
				},
				{
					"license": "http://creativecommons.org/licenses/by/3.0/",
					"mediaURL": "http://calphotos.berkeley.edu/imgs/512x768/0000_0000/0115/1280.jpeg",
					"eolMediaURL": "http://media.eol.org/content/2015/01/12/16/02016_orig.jpg",
					"rightsHolder": "2015 Carlos Henrique Luz Nunes de Almeida",
					"vettedStatus": "Trusted",
					"source": "http://calphotos.berkeley.edu/cgi/img_query?seq_num=628370&one=T",
					"eolThumbnailURL": "http://media.eol.org/content/2015/01/12/16/02016_98_68.jpg",
					"dataRating": 4.0
				},
				{
					"license": "http://creativecommons.org/publicdomain/mark/1.0/",
					"mediaURL": "http://upload.wikimedia.org/wikipedia/commons/2/2c/Obscured_jaguar.jpg",
					"eolMediaURL": "http://media.eol.org/content/2012/06/13/03/77074_orig.jpg",
					"rightsHolder": "",
					"vettedStatus": "Trusted",
					"source": "http://commons.wikimedia.org/wiki/File:Obscured_jaguar.jpg",
					"eolThumbnailURL": "http://media.eol.org/content/2012/06/13/03/77074_98_68.jpg",
					"dataRating": 3.8
				},
				{
					"license": "http://creativecommons.org/licenses/by-nc/3.0/",
					"mediaURL": "http://www.planetscott.com/img/6355/large/jaguar-(panthera-onca).jpg",
					"eolMediaURL": "http://media.eol.org/content/2012/05/18/10/43723_orig.jpg",
					"rightsHolder": "Scott Bowers",
					"vettedStatus": "Trusted",
					"source": "http://www.planetscott.com/speciesdetail/10063/jaguar-(panthera-onca)-",
					"eolThumbnailURL": "http://media.eol.org/content/2012/05/18/10/43723_98_68.jpg",
					"dataRating": 3.0
				}
			],
			"searched_name": "Panthera onca",
			"total_images": 5,
			"eol_id": 328606,
			"matched_name": "Panthera onca (Linnaeus, 1758)"
		},
		{
			"images": [
				{
					"license": "http://creativecommons.org/licenses/by-sa/2.0/",
					"mediaURL": "https://farm7.staticflickr.com/6011/6001436301_ff45749a74_o.jpg",
					"eolMediaURL": "http://media.eol.org/content/2017/03/03/16/37289_orig.jpg",
					"rightsHolder": "Bernard DUPONT",
					"vettedStatus": "Trusted",
					"source": "https://www.flickr.com/photos/berniedup/6001436301/",
					"eolThumbnailURL": "http://media.eol.org/content/2017/03/03/16/37289_98_68.jpg",
					"dataRating": 4.375
				},
				{
					"license": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
					"mediaURL": "https://farm7.staticflickr.com/6011/6001436301_ff45749a74_o.jpg",
					"eolMediaURL": "http://media.eol.org/content/2014/10/11/05/59143_orig.jpg",
					"rightsHolder": "Bernard DUPONT",
					"vettedStatus": "Trusted",
					"source": "https://www.flickr.com/photos/berniedup/6001436301/",
					"eolThumbnailURL": "http://media.eol.org/content/2014/10/11/05/59143_98_68.jpg",
					"dataRating": 4.375
				},
				{
					"license": "http://creativecommons.org/licenses/by-sa/3.0/",
					"mediaURL": "http://upload.wikimedia.org/wikipedia/commons/5/5f/Great_male_Leopard_in_South_Afrika.JPG",
					"eolMediaURL": "http://media.eol.org/content/2012/06/15/10/36939_orig.jpg",
					"rightsHolder": "",
					"vettedStatus": "Trusted",
					"source": "http://commons.wikimedia.org/wiki/File:Great_male_Leopard_in_South_Afrika.JPG",
					"eolThumbnailURL": "http://media.eol.org/content/2012/06/15/10/36939_98_68.jpg",
					"dataRating": 4.16667
				},
				{
					"license": "http://creativecommons.org/licenses/by-sa/2.0/",
					"mediaURL": "https://farm8.staticflickr.com/7197/6861336273_4e231b57df_o.jpg",
					"eolMediaURL": "http://media.eol.org/content/2015/03/11/01/76782_orig.jpg",
					"rightsHolder": "Bernard DUPONT",
					"vettedStatus": "Trusted",
					"source": "https://www.flickr.com/photos/berniedup/6861336273/",
					"eolThumbnailURL": "http://media.eol.org/content/2015/03/11/01/76782_98_68.jpg",
					"dataRating": 4.0
				},
				{
					"license": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
					"mediaURL": "https://farm8.staticflickr.com/7197/6861336273_4e231b57df_o.jpg",
					"eolMediaURL": "http://media.eol.org/content/2015/03/11/01/76782_orig.jpg",
					"rightsHolder": "Bernard DUPONT",
					"vettedStatus": "Trusted",
					"source": "https://www.flickr.com/photos/berniedup/6861336273/",
					"eolThumbnailURL": "http://media.eol.org/content/2015/03/11/01/76782_98_68.jpg",
					"dataRating": 4.0
				}
			],
			"searched_name": "Panthera pardus",
			"total_images": 5,
			"eol_id": 328673,
			"matched_name": "Panthera pardus (Linnaeus, 1758)"
		}
	]
}
```

__Alternative Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/images>

__HTTP Method:__ 		POST

__Input Format:__ 		application/json

__Output Format:__ 		application/json 


__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">species</span> 
  * __Category:__  	mandatory
  * __Data Type:__  list of strings
  * __Description:__ list of species names.
 				
 				
__Example Commands/Requests:__

1. 
```bash
curl -X POST http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/images -H 'content-type:application/json' -d '{"species": ["Catopuma badia","Catopuma temminckii"]}'
```

__Example Results:__

1. 
```json
{
	"input_species": [
		"Catopuma badia",
		"Catopuma temminckii"
	],
	"status_code": 200,
	"message": "Success",
	"meta_data": {
		"execution_time": 4.93,
		"creation_time": "2017-10-21T09:03:00.978899",
		"source_urls": [
			"http://eol.org"
		]
	},
	"species": [
		{
			"images": [
				{
					"license": "http://creativecommons.org/publicdomain/mark/1.0/",
					"mediaURL": "http://upload.wikimedia.org/wikipedia/commons/b/b7/Chat_Bai_1874.jpg",
					"eolMediaURL": "http://media.eol.org/content/2014/01/04/04/58116_orig.jpg",
					"rightsHolder": "",
					"vettedStatus": "Trusted",
					"source": "http://commons.wikimedia.org/wiki/File:Chat_Bai_1874.jpg",
					"eolThumbnailURL": "http://media.eol.org/content/2014/01/04/04/58116_98_68.jpg",
					"dataRating": 2.0
				},
				{
					"license": "http://creativecommons.org/licenses/by-sa/3.0/",
					"mediaURL": "http://upload.wikimedia.org/wikipedia/commons/1/1e/Bay_cat_1_Jim_Sanderson.jpg",
					"eolMediaURL": "http://media.eol.org/content/2013/11/25/12/14465_orig.jpg",
					"rightsHolder": "",
					"vettedStatus": "Unreviewed",
					"source": "http://commons.wikimedia.org/wiki/File:Bay_cat_1_Jim_Sanderson.jpg",
					"eolThumbnailURL": "http://media.eol.org/content/2013/11/25/12/14465_98_68.jpg",
					"dataRating": 2.5
				},
				{
					"license": "http://creativecommons.org/licenses/by-sa/3.0/",
					"mediaURL": "http://upload.wikimedia.org/wikipedia/commons/b/ba/Bay_cat_1_Jim_Sanderson-cropped.jpg",
					"eolMediaURL": "http://media.eol.org/content/2013/11/25/18/76434_orig.jpg",
					"rightsHolder": "",
					"vettedStatus": "Unreviewed",
					"source": "http://commons.wikimedia.org/wiki/File:Bay_cat_1_Jim_Sanderson-cropped.jpg",
					"eolThumbnailURL": "http://media.eol.org/content/2013/11/25/18/76434_98_68.jpg",
					"dataRating": 2.5
				},
				{
					"license": "http://creativecommons.org/licenses/by-sa/3.0/",
					"mediaURL": "http://upload.wikimedia.org/wikipedia/commons/a/aa/Catopuma_badia_John_Gray.jpg",
					"eolMediaURL": "http://media.eol.org/content/2013/11/15/02/44565_orig.jpg",
					"rightsHolder": "",
					"vettedStatus": "Unreviewed",
					"source": "http://commons.wikimedia.org/wiki/File:Catopuma_badia_John_Gray.jpg",
					"eolThumbnailURL": "http://media.eol.org/content/2013/11/15/02/44565_98_68.jpg",
					"dataRating": 2.5
				}
			],
			"searched_name": "Catopuma badia",
			"total_images": 4,
			"eol_id": 311552,
			"matched_name": "Catopuma badia (Gray, 1874)"
		},
		{
			"images": [
				{
					"license": "http://creativecommons.org/licenses/by-sa/3.0/",
					"mediaURL": "http://upload.wikimedia.org/wikipedia/commons/0/0f/Asiatische-Goldkatze-Catopuma-temminckii-tier-katze-0001_2.JPG",
					"eolMediaURL": "http://media.eol.org/content/2012/06/15/04/63856_orig.jpg",
					"rightsHolder": "",
					"vettedStatus": "Trusted",
					"source": "http://commons.wikimedia.org/wiki/File:Asiatische-Goldkatze-Catopuma-temminckii-tier-katze-0001_2.JPG",
					"eolThumbnailURL": "http://media.eol.org/content/2012/06/15/04/63856_98_68.jpg",
					"dataRating": 2.71429
				},
				{
					"license": "http://creativecommons.org/licenses/by-nc-sa/3.0/",
					"mediaURL": "http://csdb.ioz.ac.cn/images/Upload_images/Animalia/Chordata/Mammalia/CARNIVORA/Felidae/Catopuma/temminckii/7FCF470A-A4CF-4258-B673-8E0CD67DC607.jpg",
					"eolMediaURL": "http://media.eol.org/content/2012/06/27/23/19948_orig.jpg",
					"rightsHolder": "上海科学技术出版社",
					"vettedStatus": "Trusted",
					"source": null,
					"eolThumbnailURL": "http://media.eol.org/content/2012/06/27/23/19948_98_68.jpg",
					"dataRating": 2.5
				},
				{
					"license": "http://creativecommons.org/licenses/by/3.0/",
					"mediaURL": "http://calphotos.berkeley.edu/imgs/512x768/0000_0000/0714/0105.jpeg",
					"eolMediaURL": "http://media.eol.org/content/2014/07/07/00/87109_orig.jpg",
					"rightsHolder": "2014 Simon J. Tonge",
					"vettedStatus": "Trusted",
					"source": "http://calphotos.berkeley.edu/cgi/img_query?seq_num=607590&one=T",
					"eolThumbnailURL": "http://media.eol.org/content/2014/07/07/00/87109_98_68.jpg",
					"dataRating": 2.5
				},
				{
					"license": "http://creativecommons.org/licenses/by-nc/4.0/",
					"mediaURL": "http://static.inaturalist.org/photos/1723499/original.JPG?1429042450",
					"eolMediaURL": "http://media.eol.org/content/2016/07/24/13/02661_orig.jpg",
					"rightsHolder": "bangladeshpythonproject",
					"vettedStatus": "Trusted",
					"source": "http://www.inaturalist.org/photos/1723499",
					"eolThumbnailURL": "http://media.eol.org/content/2016/07/24/13/02661_98_68.jpg",
					"dataRating": 2.5
				},
				{
					"license": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
					"mediaURL": "http://farm2.staticflickr.com/1314/5179859836_13027f2c30_o.jpg",
					"eolMediaURL": "http://media.eol.org/content/2013/06/04/06/52233_orig.jpg",
					"rightsHolder": "Smithsonian Wild",
					"vettedStatus": "Trusted",
					"source": "http://www.flickr.com/photos/smithsonianwild/5179859836/",
					"eolThumbnailURL": "http://media.eol.org/content/2013/06/04/06/52233_98_68.jpg",
					"dataRating": 2.0
				}
			],
			"searched_name": "Catopuma temminckii",
			"total_images": 5,
			"eol_id": 311553,
			"matched_name": "Catopuma temminckii (Vigors and Horsfield, 1827)"
		}
	]
}
```

__Citation/Source:__  	 	
- http://eol.org/api

__Service Quality:__

 * *Restrictions on capacity:*  __maximum 30 species allowed__
 * *Expected response time:*  	__1s~25s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. specis)  | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /getimag)| 404             | Error: Could not find the requested resource URI |
   | Reached maximum input limit                        | 403             | Error: Currently more than 30 species is not supported |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_species_) will be an empty list.

---

__Service Name:__  	 	Info_url_species

__Service Description:__ 	A service to get information urls of a list of species using EOL services.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/sl/eol/get_links>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">species</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  list of species names delimited by pipe "|".
 				
  > __Note__: The service expects already resolved species names as input to provide the correct output.


__Example Commands/Requests:__

1. 

```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/sl/eol/get_links?species=Dendrocygna bicolor|Anser albifrons|Cygnus buccinator
```


__Example Results:__

1. 

```json
{
	"input_species": [
		"Dendrocygna bicolor",
		"Anser albifrons",
		"Cygnus buccinator"
	],
	"status_code": 200,
	"message": "Success",
	"meta_data": {
		"execution_time": 5.97,
		"creation_time": "2017-10-21T09:27:32.037761",
		"source_urls": [
			"http://eol.org"
		]
	},
	"species": [
		{
			"species_info_link": "http://eol.org/914528?action=overview&controller=taxa",
			"searched_name": "Dendrocygna bicolor",
			"eol_id": 914528,
			"matched_name": "Dendrocygna bicolor (Vieillot, 1816)"
		},
		{
			"species_info_link": "http://eol.org/1048438?action=overview&controller=taxa",
			"searched_name": "Anser albifrons",
			"eol_id": 1048438,
			"matched_name": "Anser albifrons (Scopoli, 1769)"
		},
		{
			"species_info_link": "http://eol.org/913233?action=overview&controller=taxa",
			"searched_name": "Cygnus buccinator",
			"eol_id": 913233,
			"matched_name": "Cygnus buccinator Richardson, 1831"
		}
	]
}
```

__Alternative Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/sl/eol/links>

__HTTP Method:__ 		POST

__Input Format:__ 		application/json

__Output Format:__ 		application/json 


__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">species</span> 
  * __Category:__  	mandatory
  * __Data Type:__  list of strings
  * __Description:__ list of species names.
 				
 				
__Example Commands/Requests:__

1. 
```bash
curl -X POST http://phylo.cs.nmsu.edu:5004/phylotastic_ws/si/eol/images -H 'content-type:application/json' -d '{"species": ["Melanerpes erythrocephalus","Melanerpes uropygialis"]}'
```

__Example Results:__

1. 
```json
{
	"input_species": [
		"Melanerpes erythrocephalus",
		"Melanerpes uropygialis"
	],
	"status_code": 200,
	"message": "Success",
	"meta_data": {
		"execution_time": 0.55,
		"creation_time": "2017-10-21T09:33:21.431243",
		"source_urls": [
			"http://eol.org"
		]
	},
	"species": [
		{
			"species_info_link": "http://eol.org/917154?action=overview&controller=taxa",
			"searched_name": "Melanerpes erythrocephalus",
			"eol_id": 917154,
			"matched_name": "Melanerpes erythrocephalus (Linnaeus, 1758)"
		},
		{
			"species_info_link": "http://eol.org/912554?action=overview&controller=taxa",
			"searched_name": "Melanerpes uropygialis",
			"eol_id": 912554,
			"matched_name": "Melanerpes uropygialis (S. F. Baird, 1854)"
		}
	]
}
```

__Citation/Source:__  	 	
- http://eol.org/api

__Service Quality:__

 * *Restrictions on capacity:*  __maximum 50 species allowed__
 * *Expected response time:*  	__1s~25s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. specis)  | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /getlink)| 404             | Error: Could not find the requested resource URI |
   | Reached maximum input limit                        | 403             | Error: Currently more than 50 species is not supported |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_species_) will be an empty list.

---

## <a name='commonname'></a>Common Name to Scientific Name

__Service Name:__  	 	NCBI_common_name

__Service Description:__ 	A service to get scientific name of a species from its common name(vernacular name) using NCBI services.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5004/phylotastic_ws/cs/ncbi/get_scientific_name>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">common_name</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  a common name for which to find scientific name.
 				
  
__Example Commands/Requests:__

1. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/cs/ncbi/get_scientific_name?common_name=dog
```

2. 
```
http://phylo.cs.nmsu.edu:5004/phylotastic_ws/cs/ncbi/get_scientific_name?common_name=tiger
```


__Example Results:__

1. 
```json
{
	"input_common_name": "dog",
	"ncbi_info_url": "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=9615",
	"scientific_name": "Canis lupus familiaris",
	"status_code": 200,
	"meta_data": {
		"execution_time": 5.68,
		"creation_time": "2017-10-21T12:17:59.713335",
		"source_urls": [
			"https://www.ncbi.nlm.nih.gov/taxonomy"
		]
	},
	"message": "Success",
	"extra_info": {
		"genbank_common_name": "dog",
		"inherited_blast_name": " carnivores",
		"rank": " subspecies"
	}
}
```

2. 
```json
{
	"input_common_name": "tiger",
	"ncbi_info_url": "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=9694",
	"scientific_name": "Panthera tigris",
	"status_code": 200,
	"meta_data": {
		"execution_time": 4.58,
		"creation_time": "2017-10-21T12:15:56.749299",
		"source_urls": [
			"https://www.ncbi.nlm.nih.gov/taxonomy"
		]
	},
	"message": "Success",
	"extra_info": {
		"genbank_common_name": "tiger",
		"inherited_blast_name": " carnivores",
		"rank": " species"
	}
}
```

__Citation/Source:__         https://www.ncbi.nlm.nih.gov/taxonomy

__Service Quality:__

 * *Restrictions on capacity:*  __unknown__
 * *Expected response time:*  	__1s~15s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. common)  | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid method name in resource URI (e.g. /scname) | 404             | Error: Could not find the requested resource URI |
   | Internal server error                              | 500             |  |

  > __Note__: In case of error conditions in source web services, their HTTP status codes are returned. When the request was executed successfully, but no result was produced then the response status will still be 200 and the corresponding output field(_scientific_name_) will be an empty string.


---

**[Species List services](#specieslist)** :  services to publish/remove/update/access lists of species owned by a phylotastic web application/services user.



---

## <a name='specieslist'></a>Species List Manipulation

__Service Name:__  	 	Add_new_list

__Service Description:__ 	A service to insert a new list of species into the phylotastic list server.

__Resource URI:__  	<http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/insert_list>

__HTTP Method:__ 		POST

__Input Format:__ 		application/json

__Output Format:__ 		application/json 
  				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">user_id</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  unique id (valid gmail address) of a phylotastic web application/services user.

2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">list</span> 
  * __Category:__  	mandatory
  * __Data Type:__  complex json object
  * __Description:__  unique id (valid gmail address) of a phylotastic web application/services user.

All data and metadata related to the new list of species encapsulated in a complex json object. The complex json object has the following properties:--
  + Property name: __list_title__ 
    + Data type: string
    + Category: mandatory
    + Description: title of the new list. 
  + Property name: __list_description__
    + Data type: string
    + Category: optional
    + Description: description of the new list.
  + Property name: __list_author__
    + Data type: a list of strings
    + Category: optional
    + Description: names of the original authors who prepared the list.
  + Property name: __list_date_published__
    + Data type: string (format: *mm-dd-yyyy*)
    + Category: optional
    + Description: date when the new list is being posted.
  + Property name: __list_curator__
    + Data type: string
    + Category: mandatory
    + Description: name of the curator of the new list.
  + Property name: __list_curation_date__
    + Data type: string (format: *mm-dd-yyyy*)
    + Category: mandatory
    + Description: date when the new list is being curated.
  + Property name: __list_source__
    + Data type: string
    + Category: mandatory
    + Description: source of the new list (url, publication).
  + Property name: __list_keywords__
    + Data type: a list of strings
    + Category: optional
    + Description: keywords related to the new list.
  + Property name: __list_focal_clade__
    + Data type: string
    + Category: optional
    + Description:  focal_clade of the new list.
  + Property name: __list_extra_info__
    + Data type: string
    + Category: optional
    + Description:  extra information about the new list.
  + Property name: __list_origin__
    + Data type: string
    + Category: mandatory
    + Description:  the origin from where the new list is being posted. (Permitted values: `webapp` or `mobileapp` or `script`).
  + Property name: __is_list_public__
    + Data type: boolean
    + Category: optional
    + Description:  By default `false`. Set to `true` if the new list posted can be viewed by public. 
  + Property name: __list_species__
    + Data type: a list of [json species object](#jsonspecies)
    + Category: mandatory
    + Description:  the data about species belonging to the list.

<a name="jsonspecies">The json species object</a> contains the actual data (species). It has the following properties:

+ Property name: __vernacular_name__ 
    + Data type: string
    + Category: mandatory
    + Description: vernacular name of the species. 
+ Property name: __scientific_name__
    + Data type: string
    + Category: mandatory
    + Description: scientific name of the species.
+ Property name: __scientific_name_authorship__
    + Data type: string
    + Category: optional
    + Description: authorship of the scientific name of the species.
+ Property name: __family__
    + Data type: string
    + Category: optional
    + Description: the taxonomic rank family where the species belongs to.
+ Property name: __order__
    + Data type: string
    + Category: optional
    + Description: the taxonomic rank order where the species belongs to.
+ Property name: __class__
    + Data type: string
    + Category: optional
    + Description: the taxonomic rank class where the species belongs to.
+ Property name: __phylum__
    + Data type: string
    + Category: optional
    + Description: the taxonomic rank phylum where the species belongs to.
+ Property name: __nomenclature_code__
    + Data type: string
    + Category: optional
    + Description: the nomenclatural code of the species.


__Example Commands/Requests:__ 

1. 
```bash
curl -X POST http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/insert_list -H 'content-type:application/json' -d '{"user_id": "hdail.laughinghouse@gmail.com", "list": {"list_extra_info": "", "list_description": "A list of the bird species and their endangered, threatened or invasive status", "list_keywords": ["Bird", "Endangered species", "Everglades"], "list_curator": "HD Laughinghouse", "list_origin": "script", "list_curation_date": "02-24-2016", "list_source": "Des", "list_focal_clade": "Aves", "list_title": "Bird Species List for Everglades National Park", "list_author": ["Bass, O.", "Cunningham, R."], "is_list_public": true, "list_species": [{"family": "Anatidae", "scientific_name": "Aix sponsa", "vernacular_name": "Wood Duck", "nomenclature_code": "ICZN", "order": "Anseriformes"}, {"family": "Anatidae", "scientific_name": "Anas strepera", "vernacular_name": "Gadwall", "nomenclature_code": "ICZN", "order": "Anseriformes"}, {"family": "Caprimulgidae", "scientific_name": "Caprimulgus vociferus", "scientific_name_authorship": "", "vernacular_name": "Whip-poor-will","nomenclature_code": "ICZN", "order": "Caprimulgiformes"}]}}'
```

__Example Results:__

1. 
```json
{
	"status_code": 200,
	"message": "Success",
	"user_id": "hdail.laughinghouse@gmail.com",
	"list_id": 24
}
```

__Service Quality:__

 * *Restrictions on capacity:*  __none__
 * *Expected response time:*  	__1s~5s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. user)    | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid input JSON data                            | 400             | Invalid JSON document |
   | Invalid method name in resource URI (e.g. /insert) | 404             | Error: Could not find the requested resource URI |
   | Internal server error                              | 500             |  |

  > __Note__: Validity of the user_id (_gmail address_) in the input request is not checked by the service. The user needs to provide a valid id to retrieve the list later using __list_id__ value returned by the service. 


---

__Service Name:__  	 	 Get_list

__Service Description:__ 	A service to get public lists of species or private lists of species owned by a phylotastic web application/services user.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/get_list>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">user_id</span> 
  * __Category:__  	mandatory/optional
  * __Data Type:__  string
  * __Description:__  unique id (valid gmail address) of a phylotastic web application/services user.

  > __Note__: *user_id* parameter is mandatory only if a user wants to view all the lists (public/private) owned by the *user_id*  **OR** if a user wants to view a specific private list owned by the *user_id*. 

  > *user_id* parameter is not needed if a user wants to view all available public lists.
 
2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">list_id</span> 
  * __Category:__  	mandatory/optional
  * __Data Type:__  integer
  * __Description:__  list id of a specific list.

  > __Note__: *list_id* parameter is mandatory only if a user wants to view a specific private list identified by *list_id* and owned by the *user_id* **OR** if a user wants to view a specific public list identified by *list_id* and owned by other user.

3. Parameter details:
  * __Name:__ 	 	<span style="color:blue">access_token</span> 
  * __Category:__  	mandatory/optional
  * __Data Type:__  string
  * __Description:__  access token for the user with *user_id* (valid gmail address).

  > __Note__: *access_token* parameter is used for authenticating the user with valid gmail address. It is mandatory only if a user wants to view all the lists (public/private) owned by the *user_id* **OR** if a user wants to view a specific private list identified by *list_id* and owned by the *user_id*.

4. Parameter details:
  * __Name:__ 	 	<span style="color:blue">verbose</span> 
  * __Category:__  	optional
  * __Data Type:__  boolean
  * __Description:__  It is an optional parameter which is by default *false* and shows minimal meta-data of the list. When given *true* it will display all meta-data related to that list and species collection.

5. Parameter details:
  * __Name:__ 	 	<span style="color:blue">content</span> 
  * __Category:__  	optional
  * __Data Type:__  boolean
  * __Description:__  It is an optional parameter which is by default *true* and shows the species collection of the list. When given *false* it will not display any species collection of the list.


__Example Commands/Requests:__ 

> __Note__: *access_token* values presented below is just used as an example. Testing the urls in the examples using these tokens will not work. The user has to provide a valid unexpired access token for his/her gmail address. The procedure for getting an *access_token* can be found [here](https://github.com/phylotastic/phylo_services_docs/blob/master/SpeciesListServer/AccessToken.md#how-to-get-access-token-to-use-in-species-list-web-services).


1. To get all the public lists available:
```
http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/get_list
```
2. To get a specific public list with ID 24:
```
http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/get_list?list_id=24
```
3. To get all lists of user with ID *hdail.laughinghouse@gmail.com*:
```
http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/get_list?user_id=hdail.laughinghouse@gmail.com&access_token=ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA
```
4. To get a specific private list with ID 20 and owned by hdail.laughinghouse@gmail.com:
```
http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/get_list?user_id=hdail.laughinghouse@gmail.com&list_id=20&access_token=ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA
```
5. To get a specific private list (including all metadata available) with ID 20 and owned by hdail.laughinghouse@gmail.com:
```
http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/get_list?user_id=hdail.laughinghouse@gmail.com&list_id=20&verbose=true&access_token=ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA

__Example Results:__

2. 
```json
{
	"status_code": 200,
	"message": "Success",
	"list": {
		"list_title": "Bird Species List for Everglades National Park",
		"list_species": [
			"Aix sponsa",
			"Anas strepera",
			"Caprimulgus vociferus"
		],
		"list_id": 24
	}
}
```

__Service Quality:__

 * *Restrictions on capacity:*  __none__
 * *Expected response time:*  	__1s~5s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. token)   | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid input JSON data                            | 400             | Invalid JSON document |
   | Invalid or expired _access_token_ value            | 401             |  |
   | Invalid method name in resource URI (e.g. /getlist)| 404             | Error: Could not find the requested resource URI |
   | Nonexistent _user_id_ or _list_id_ value           | 409             |  |
   | Internal server error                              | 500             |  |


---

__Service Name:__  	 	 Replace_species_list 

__Service Description:__ 	A service to replace the [species objects](#jsonspecies) of an existing list with new species objects.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/replace_species>

__HTTP Method:__ 		POST

__Input Format:__ 		application/json

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">user_id</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  unique id (valid gmail address) of a phylotastic web application/services user.

2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">list_id</span> 
  * __Category:__  	mandatory
  * __Data Type:__  integer
  * __Description:__  unique id of an existing list.

3. Parameter details:
  * __Name:__ 	 	<span style="color:blue">access_token</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  access token for the user with *user_id* (valid gmail address).

4. Parameter details:
  * __Name:__ 	 	<span style="color:blue">species</span> 
  * __Category:__  	mandatory
  * __Data Type:__  a list of [json species object](#jsonspecies)
  * __Description:__  a list of json species objects to replace the existing species objects.

 
__Example Commands/Requests:__ 

1. 
```bash
curl -X POST http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/replace_species -H 'content-type:application/json' -d '{"user_id": "hdail.laughinghouse@gmail.com", "access_token": "ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA", "list_id": 24, "species":[{"family": "Columbidae", "scientific_name": "Columba livia", "vernacular_name": "Rock Dove", "nomenclature_code": "ICZN", "order": "Columbiformes", "class": "Aves"}, {"family": "Alcedinidae", "scientific_name": "Megaceryle alcyon", "vernacular_name": "Belted Kingfisher", "phylum": "Chordata", "nomenclature_code": "ICZN", "order": "Coraciiformes"}, {"family": "Aramidae", "scientific_name": "Aramus guarauna", "vernacular_name": "Limpkin", "nomenclature_code": "ICZN", "order": "Gruiformes", "class": "Aves"}]}'
```

__Example Results:__

1. 
```json
{
	"user_id": "hdail.laughinghouse@gmail.com",
	"date_modified": "2017-10-22T22:37:57.947308",
	"status_code": 200,
	"old_species": [
		{
			"family": "Anatidae",
			"scientific_name": "Aix sponsa",
			"scientific_name_authorship": "NA",
			"order": "Anseriformes",
			"vernacular_name": "Wood Duck",
			"phylum": "NA",
			"nomenclature_code": "ICZN",
			"class": "NA"
		},
		{
			"family": "Anatidae",
			"scientific_name": "Anas strepera",
			"scientific_name_authorship": "NA",
			"order": "Anseriformes",
			"vernacular_name": "Gadwall",
			"phylum": "NA",
			"nomenclature_code": "ICZN",
			"class": "NA"
		},
		{
			"family": "Caprimulgidae",
			"scientific_name": "Caprimulgus vociferus",
			"scientific_name_authorship": "",
			"order": "Caprimulgiformes",
			"vernacular_name": "Whip-poor-will",
			"phylum": "NA",
			"nomenclature_code": "ICZN",
			"class": "NA"
		}
	],
	"new_species": [
		{
			"family": "Columbidae",
			"scientific_name": "Columba livia",
			"scientific_name_authorship": "NA",
			"order": "Columbiformes",
			"vernacular_name": "Rock Dove",
			"phylum": "NA",
			"nomenclature_code": "ICZN",
			"class": "Aves"
		},
		{
			"family": "Alcedinidae",
			"scientific_name": "Megaceryle alcyon",
			"scientific_name_authorship": "NA",
			"class": "NA",
			"vernacular_name": "Belted Kingfisher",
			"phylum": "Chordata",
			"nomenclature_code": "ICZN",
			"order": "Coraciiformes"
		},
		{
			"family": "Aramidae",
			"scientific_name": "Aramus guarauna",
			"scientific_name_authorship": "NA",
			"order": "Gruiformes",
			"vernacular_name": "Limpkin",
			"phylum": "NA",
			"nomenclature_code": "ICZN",
			"class": "Aves"
		}
	],
	"list_id": 24,
	"list_title": "Bird Species List for Everglades National Park",
	"message": "Success"
}
```

__Service Quality:__

 * *Restrictions on capacity:*  __none__
 * *Expected response time:*  	__1s~5s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. token)   | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid input JSON data                            | 400             | Invalid JSON document |
   | Invalid or expired _access_token_ value            | 401             |  |
   | Invalid method name in resource URI (e.g. /getlist)| 404             | Error: Could not find the requested resource URI |
   | Nonexistent _user_id_ or _list_id_ value           | 409             |  |
   | Internal server error                              | 500             |  |


---

__Service Name:__  	 	 Update_metadata_list 

__Service Description:__ 	A service to update properties (metadata) of an existing list.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/update_list>

__HTTP Method:__ 		POST

__Input Format:__ 		application/json

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">user_id</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  unique id (valid gmail address) of a phylotastic web application/services user.

2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">list_id</span> 
  * __Category:__  	mandatory
  * __Data Type:__  integer
  * __Description:__  unique id of an existing list.

3. Parameter details:
  * __Name:__ 	 	<span style="color:blue">access_token</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  access token for the user with *user_id* (valid gmail address).

4. Parameter details:
  * __Name:__ 	 	<span style="color:blue">list</span> 
  * __Category:__  	mandatory
  * __Data Type:__  a json list __sub-object__ consisting of a subset of list properties.
  * __Description:__  an object consisting of a subset of list properties (metadata) that need to be updated.

 
__Example Commands/Requests:__ 

1. To change the source and date_published of a list with ID 24.
```bash
curl -X POST http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/update_list -H 'content-type:application/json' -d '{"user_id": "hdail.laughinghouse@gmail.com", "access_token": "ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA", "list_id": 24, "list": {"list_source": "Bass, O. & Cunningham, R. (2006) Everglades National Park Bird Checklist. Miami: Everglades Association", "list_date_published": "05-02-2006"}}'
```

2. To change type of a list with ID 24 from "public" to "private":
```bash
curl -X POST http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/update_list -H 'content-type:application/json' -d '{"user_id": "hdail.laughinghouse@gmail.com", "access_token": "ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA", "list_id": 24, "list": {"is_list_public": false}}'
```

__Example Results:__

1. 
```json
{
	"user_id": "hdail.laughinghouse@gmail.com",
	"date_modified": "2017-10-22T23:05:53.240754",
	"status_code": 200,
	"modified_content": {
		"list_source": "Bass, O. & Cunningham, R. (2006) Everglades National Park Bird Checklist. Miami: Everglades Association",
		"list_date_published": "05-02-2006"
	},
	"list_id": 24,
	"list_title": "Bird Species List for Everglades National Park",
	"message": "Success"
}
```

__Service Quality:__

 * *Restrictions on capacity:*  __none__
 * *Expected response time:*  	__1s~5s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. token)   | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid input JSON data                            | 400             | Invalid JSON document |
   | Invalid or expired _access_token_ value            | 401             |  |
   | Invalid method name in resource URI (e.g. /getlist)| 404             | Error: Could not find the requested resource URI |
   | Nonexistent _user_id_ or _list_id_ value           | 409             |  |
   | Internal server error                              | 500             |  |


---

__Service Name:__  	 	 Remove_list 

__Service Description:__ 	A service to remove an existing list.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/remove_list>

__HTTP Method:__ 		GET or POST

__Input Format:__ 		application/x-www-form-urlencoded

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">user_id</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  unique id (valid gmail address) of a phylotastic web application/services user.

2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">list_id</span> 
  * __Category:__  	mandatory
  * __Data Type:__  integer
  * __Description:__  unique id of an existing list.

3. Parameter details:
  * __Name:__ 	 	<span style="color:blue">access_token</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  access token for the user with *user_id* (valid gmail address).


__Example Commands/Requests:__ 

1. 
```
http://phylo.cs.nmsu.edu:5005/phylotastic_ws/sls/remove_list?user_id=hdail.laughinghouse@gmail.com&list_id=24&access_token=ya29..zQLmLjbyujJjwV6RVSM2sy-mkeaKu-9_n7y7iB6uKuL-rHDGp3W2_hPWUSO5uX_OcA
```

__Example Results:__

1.  
```json
{
	"user_id": "hdail.laughinghouse@gmail.com",
	"status_code": 200,
	"list_id": 24,
	"date_removed": "2017-10-22T23:22:03.032718",
	"list_title": "Bird Species List for Everglades National Park",
	"message": "Success"
}
```

__Service Quality:__

 * *Restrictions on capacity:*  __none__
 * *Expected response time:*  	__1s~5s__
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. token)   | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid input JSON data                            | 400             | Invalid JSON document |
   | Invalid or expired _access_token_ value            | 401             |  |
   | Invalid method name in resource URI (e.g. /getlist)| 404             | Error: Could not find the requested resource URI |
   | Nonexistent _user_id_ or _list_id_ value           | 409             |  |
   | Internal server error                              | 500             |  |

---

## <a name='treescaling'></a>Tree Scaling

__Service Name:__  	 	 Datelife_scale_tree 

__Service Description:__ 	A service to get Phylogenetic Trees with branch lengths using Datelife R package.

__Resource URI:__  		<http://phylo.cs.nmsu.edu:5009/phylotastic_ws/sc/scale>

__HTTP Method:__ 		POST

__Input Format:__ 		application/json

__Output Format:__ 		application/json 
 				
__Parameters:__

1. Parameter details:
  * __Name:__ 	 	<span style="color:blue">newick</span> 
  * __Category:__  	mandatory
  * __Data Type:__  string
  * __Description:__  tree in newick string format.

2. Parameter details:
  * __Name:__ 	 	<span style="color:blue">method</span> 
  * __Category:__  	optional
  * __Data Type:__  string
  * __Description:__  a string value to specify which method should be used for scaling. Valid values include `median` or `sdm`. `median` is the default scaling method which uses the median of all source chronograms. `sdm` method uses SDM supertree method (Criscuolo et al. 2006).


__Example Commands/Requests:__ 

1. 
```bash
curl -X POST http://phylo.cs.nmsu.edu:5009/phylotastic_ws/sc/scale -H 'content-type:application/json' -d '{"newick": "((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);", "method": "sdm"}'
```

2. 
```bash
curl -X POST http://phylo.cs.nmsu.edu:5009/phylotastic_ws/sc/scale -H 'content-type:application/json' -d '{"newick": "(((((Canis lupus pallipes,Melursus ursinus)Caniformia,((Panthera tigris,Panthera pardus)Panthera,Herpestes fuscus))Carnivora,(Macaca mulatta,Homo sapiens)Catarrhini)Boreoeutheria,Elephas maximus)Eutheria,Haliastur indus)Amniota;"}'
```


__Example Results:__

1. 
```json
{
	"method_used": "sdm",
	"status_code": 200,
	"scaled_tree": "(Solanum lycopersicum:141.8861801,((Zea mays:106.2589771,Oryza sativa:106.2589771):35.62720301,(Arabidopsis thaliana:117.1887019,(Glycine max:97.3424611,Medicago sativa:97.3424611):19.84624085):24.69747818):0);",
	"meta_data": {
		"execution_time": "3.26",
		"creation_time": "2017-10-23T07:49:51.503483",
		"source_urls": [
			"http://datelife.org/"
		]
	},
	"input_tree": "((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);",
	"message": "Success"
}
```

2. 
```json
{
	"method_used": "median",
	"status_code": 200,
	"scaled_tree": "((((Homo sapiens:29.126382,Macaca mulatta:29.126382):69.773618,(((Panthera pardus:6.4,Panthera tigris:6.4):34.300001,Herpestes fuscus:40.700001):24.199999,(Canis lupus pallipes:16.775,Melursus ursinus:16.775):48.125):34):10.65,Elephas maximus:109.55):17.078571,Haliastur indus:126.628571);",
	"meta_data": {
		"execution_time": "3.16",
		"creation_time": "2017-10-23T07:50:31.586571",
		"source_urls": [
			"http://datelife.org/"
		]
	},
	"input_tree": "(((((Canis lupus pallipes,Melursus ursinus)Caniformia,((Panthera tigris,Panthera pardus)Panthera,Herpestes fuscus))Carnivora,(Macaca mulatta,Homo sapiens)Catarrhini)Boreoeutheria,Elephas maximus)Eutheria,Haliastur indus)Amniota;",
	"message": "Success"
}
```

__Citation/Source:__  	 	http://datelife.org/


__Service Quality:__

 * *Restrictions on capacity:*  __unknown__ (_depends on the source_)
 * *Expected response time:*  	__1s~10s__ (_might be longer depending on the input tree_)
 * *Informative message/status:*
   | Case                                               | HTTP status code| Message
   | ---------------------------------------------------|:---------------:| -------------:|
   | Successful                                         | 200             | Success       |
   | Missing value of mandatory parameter               | 400             | Error: '_parameter name_' parameter must have a valid value |
   | Invalid name of mandatory parameter (e.g. newik)   | 400             | Error: Missing parameter '_parameter name_' |
   | Invalid input JSON data                            | 400             | Invalid JSON document |
   | Invalid method name in resource URI (e.g. /scal)   | 404             | Error: Could not find the requested resource URI |
   | Internal server error                              | 500             |  |


---

