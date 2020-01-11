### Instructions to setup species_list app docker for the first time. 

**1.** Download the directory named *species_list*.

**2.** Open the *docker-compose.yml* file. Find the `device` key in the `volumes` section. Replace the default path `/tmp/backups` with the full path where database backups will be stored.

**3.** Go to the *species_list* directory and run the following command:

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

> Assuming that the exposed host port is 5055. 

#### Example 1: (get all public lists)
``
curl -X GET 'http://localhost:5055/phylotastic_ws/sls/get_list'
``

**6.** To stop the docker container press `CTRL+C`.

**7.** To run the docker image in background mode, use the following command.

``
docker-compose up -d
`` 

**8.** To check whether the docker image is running in the background, use the following command.

``
docker ps
``

### Instructions to setup species_list app docker second time using a backup database. 

> Assuming that the docker has been run at least once and there exists some backup of the database.

**1.** Find the latest `*.tgz` backup file from the host directory which was set earlier.

**2.** Extract the backup file and copy all the files inside the *Specieslist* directory to the *seed* directory that is located inside the **mongo-seed** directory. 

**3.** Go to the *species_list* directory and rebuild the image using the following command.

``
docker-compose build --no-cache
``

**4.** Now run the docker container using the following command.

``
docker-compose up
``
