### Instructions to setup image_info_retrieval app docker. 

**1.** Download the directory named *image_info_retrieval*.

**2.** Go to the *image_info_retrieval* directory and run the following command:

``
docker build -t image_info_retrieval:v0.0.1 .
``
> To rebuild everything use `--no-cache` at the end of the above command.

**3.** Check whether the docker image *image_info_retrieval* has been built by listing all containers:

``
docker images
``

**4.**  Run the docker image by mapping exposed docker port 5054 to internal service port 5054 by using the following command. 

``
docker run -p 5054:5054 image_info_retrieval:v0.0.1
``

**5.** Now test the service using the following commands:

#### Example 1: 
``
curl -X POST http://localhost:5054/phylotastic_ws/si/eol/images -H 'content-type:application/json' -d '{"species": ["Catopuma badia","Catopuma temminckii"]}'
``

#### Example 2: 
``
curl -X POST http://localhost:5054/phylotastic_ws/sl/eol/links -H 'content-type:application/json' -d '{"species": ["Melanerpes erythrocephalus","Melanerpes uropygialis"]}'
``

**6.** To stop the service press `CTRL+C`.

**7.** To run the docker image in background mode, use the following command.

``
docker run -d --rm -p 5054:5054 --name image_info_retrieval image_info_retrieval:v0.0.1
`` 

**8.** To check whether the docker image is running in the background, use the following command.

``
docker ps
``

**9.** To stop the docker image from running, use the following command.

``
docker stop <IMAGE_ID>
``

