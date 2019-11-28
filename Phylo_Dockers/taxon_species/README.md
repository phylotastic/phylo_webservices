### Instructions to setup taxon_species app docker for the first time. 

**1.** Download the directory named *taxon_species*.

**2.** Open the *docker-compose.yml* file. Find the `device` key in the `volumes` section. Replace the default path `/tmp/backups` with the full path where database backups will be stored. The full path must exist in the local host system.

**3.** Go to the *taxon_species* directory and run the following command:

``
docker-compose build
``
> To rebuild everything use `--no-cache` at the end of the above command.

**4.** Now run the container using the following command.

``
docker-compose up
``

> When running the docker image for the first time, it will import some seed data into the database and start taking backup of the database weekly (every 604800 seconds). The backup files will be stored as `.tgz` format in the host directory which is set at step 2. The backup interval can be changed by modifying the `INTERVAL` value in the `start.sh` script which is located inside **mongo-seed** directory.

**5.** Now open a new terminal and test the service using the following commands:

> Assuming that the exposed host port is 5053. 

#### Example 1:
``
curl -X GET 'http://localhost:5053/phylotastic_ws/ts/ot/all_species?taxon=Vulpes'
``

#### Example 2:
``
curl -X GET 'http://localhost:5053/phylotastic_ws/ts/ncbi/genome_species?taxon=Rodentia'
``


### Instructions to setup taxon_species app docker second time using a backup database. 

> Assuming that the docker has been run at least once and there exists some backup of the database.

**1.** Find the latest `*.tgz` backup file from the host directory which was set earlier.

**2.** Extract the backup file and copy all the files inside the *TaxonSpecies* directory to the *seed* directory that is located inside the **mongo-seed** directory. 

**3.** Go to the *taxon_species* directory and rebuild the image using the following command.

``
docker-compose build --no-cache
``

**4.** Now run the docker container using the following command.

``
docker-compose up
``
