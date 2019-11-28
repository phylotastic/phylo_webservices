## Phylotastic-Dockers. 

This repository contains the docker files for the core groups of phylotastic services. Each group is organized into separate folders. 
  

**1.** To setup the dockers, please install docker in the system.
 - [Install Docker for Mac](https://docs.docker.com/v17.12/docker-for-mac/install/)
 - [Install Docker for Ubuntu](https://docs.docker.com/v17.12/install/linux/docker-ce/ubuntu/)

**2.** To setup the services, please follow instructions for each group available inside the corresponding folders.

The services available in each group are listed below:

| Group      | List of services |
| ----------- | ----------- |
| name_finder | GNRD_wrapper_URL, GNRD_wrapper_text, GNRD_wrapper_file, TaxonFinder_wrapper_URL, TaxonFinder_wrapper_text |
| name_resover| OToL_TNRS_wrapper, GNR_TNRS_wrapper, iPlant_TNRS_wrapper|
| tree_retrieval| OToL_wrapper_Tree, Phylomatic_wrapper_Tree|
| taxon_species| Taxon_all_species, Taxon_country_species, Taxon_genome_species, Taxon_popular_species|
| tree_scale| Datelife_scale_tree, OToL_scale_tree|
| image_info_retrieval| Image_url_species, Info_url_species|
| name_converter| NCBI_common_name, EBI_commmon_name, ITIS_common_name, TROPICOS_commmon_name, GNR_scientific_name, EOL_scientific_name, NCBI_scientific_name|
| species_list| Add_new_list, Get_list, Replace_species_list, Update_metadata_list, Remove_list|


> Details about the services can be found [here](https://github.com/phylotastic/phylo_services_docs/tree/master/ServiceDescription#servicesdocumentation).


 
