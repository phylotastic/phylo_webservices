### Instructions to setup tree_retrieval app docker. 

**1.** Download the directory named *tree_retrieval*.

**2.** Go to the *tree_retrieval* directory and run the following command:

``
docker build -t tree_retrieval:v0.0.1 .
``
> To rebuild everything use `--no-cache` at the end of the above command.

**3.** Check whether the docker image *tree_retrieval* has been built by listing all containers:

``
docker images
``

**4.** Run the docker image by mapping exposed docker port 5052 to internal service port 5052 by using the following command. 

``
docker run -p 5052:5052 tree_retrieval:v0.0.1
``

**5.** Now test the service using the following commands:

#### Example 1:

``
curl -X POST "http://localhost:5052/phylotastic_ws/gt/ot/tree" -H "content-type:application/json" -d '{"taxa": ["Setophaga striata","Setophaga magnolia","Setophaga angelae","Setophaga plumbea","Setophaga virens"]}'
``

#### Example 2:

``
curl -X GET 'http://localhost:5052/phylotastic_ws/gt/ot/get_tree?taxa=Panthera%20pardus|Taxidea%20taxus|Lutra%20lutra|Canis%20lupus|Mustela%20altaica&studies=true'
``

#### Example 3:
``
curl -X POST "http://localhost:5052/phylotastic_ws/gt/pm/tree" -H "content-type:application/json" -d '{"taxa": ["Helianthus annuus","Passiflora edulis", "Rosa arkansana", "Saccharomyces cerevisiae"]}'
``

**6.** To stop the service press `CTRL+C`.

**7.** To run the docker image in background mode, use the following command.

``
docker run -d --rm -p 5052:5052 --name tree_retrieval tree_retrieval:v0.0.1
`` 

**8.** To check whether the docker image is running in the background, use the following command.

``
docker ps
``

**9.** To stop the docker image from running, use the following command.

``
docker stop <IMAGE_ID>
``
