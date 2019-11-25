### Instructions to setup name_resolver app docker. 

**1.** Download the directory named *name_resolver*.

**2.** Go to the *name_resolver* directory and run the following command:

``
docker build -t name_resolver:v0.0.1 .
``
> To rebuild everything use `--no-cache` at the end of the above command.

**3.** Check whether the docker image *name_resolver* has been built by listing all containers:

``
docker images
``

**4.**  Run the docker image by mapping exposed docker port 5051 to internal service port 5051 by using the following command. 


``
docker run -p 5051:5051 name_resolver:v0.0.1
``

**5.** Now open a new terminal and test the service using the following commands:

#### Example 1: 
``
curl -X GET 'http://localhost:5051/phylotastic_ws/tnrs/ot/resolve?names=Formica%20polyctena|Formica%20exsectoides|Formica%20pecefica%27'
``

#### Example 2: 
``
curl -X POST "http://localhost:5051/phylotastic_ws/tnrs/gnr/names" -H "content-type:application/json" -d '{"scientificNames": ["Rana Temporaria"],"fuzzy_match":true, "multiple_match":false}'
``

