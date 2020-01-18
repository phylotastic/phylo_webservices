### Instructions to setup tree_scale app docker. 

**1.** Download the directory named *tree_scale*.

**2.** Go to the *tree_scale* directory and run the following command:

``
docker build -t tree_scale:v0.0.1 .
``
> To rebuild everything use `--no-cache` at the end of the above command.

> *Building the image may take approximately an hour or more to finish.*

**3.** Check whether the docker image *tree_scale* has been built by listing all containers:

``
docker images
``

**4.**  Run the docker image by mapping exposed docker port 5056 to internal service port 5056 by using the following command. 


``
docker run -p 5056:5056 tree_scale:v0.0.1
``

**5.** Now open a new terminal and test the service using the following commands:

#### Example 1: 
``
curl -X POST http://localhost:5056/phylotastic_ws/sc/scale -H 'content-type:application/json' -d '{"newick": "((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);", "method": "sdm"}'
``

#### Example 2: 
``
curl -X POST http://localhost:5056/phylotastic_ws/sc/ot/scale -H 'content-type:application/json' -d '{"newick": "(Aulacopone_relicta,(((Myrmecia_gulosa,(Aneuretus_simoni,Dolichoderus_mariae)),((Ectatomma_ruidum,Huberia_brounii),Formica_rufa)),Apomyrma_stygia),Martialis_heureka)Formicidae;"}'
``
**6.** To stop the service press `CTRL+C`.

**7.** To run the docker image in background mode, use the following command.

``
docker run -d --rm -p 5056:5056 --name tree_scale tree_scale:v0.0.1
`` 

**8.** To check whether the docker image is running in the background, use the following command.

``
docker ps
``

**9.** To stop the docker image from running, use the following command.

``
docker stop <IMAGE_ID>
``
