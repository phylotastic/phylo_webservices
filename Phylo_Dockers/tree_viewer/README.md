### Instructions to setup tree_viewer_app

**1.** Download the directory named *tree_viewer*.

**2.** Open the *docker-compose.yml* file. Find the `device` key in the `backup` section under `volumes`. Replace the default path `/var/web_services/tree_backups` with the full path where database backups will be stored. The full path must exist in the local host system.
 
**3.** Run the following command to build the image first.

``
docker-compose build
``

**4.** Run the container using the following command.

``
docker-compose up
``
  
**5.** To stop the docker container press `CTRL+C`.

**6.** To run the docker image in background mode, use the following command.

``
docker-compose up -d
`` 

**7.** To check whether the docker image is running in the background, use the following command.

``
docker ps
``


### Test the app using command

``
curl -X POST http://localhost:8989/ete_pro/get_tree_image -H "content-type:application/json" -d '{"tree_newick": "(((Rangifer tarandus, Cervus elaphus)Cervidae, (Bos taurus, Ovis orientalis)Bovidae), (Suricata suricatta, (Cistophora cristata,Mephitis mephitis))Carnivora);" ,"tree_id": 12, "actions": ""}'
``

### Test the app using site

Setup the site according to the instructions in [**tree_viewer_test**](https://github.com/phylotastic/phylo_webservices/tree/master/Phylo_Dockers/tree_viewer_test) to test the treeviewer service. 
