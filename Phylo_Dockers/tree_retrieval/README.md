### Instructions to setup tree_retrieval app docker. 

**1.** Download the directory named *tree_retrieval*.

**2.** Go to the *tree_retrieval* directory and run the following command:

``
docker build -t tree_retrieval:v0.0.1 .
``

**3.** Check whether the docker image *tree_retrieval* has been built by listing all containers:

``
docker images
``

**4.** Run the docker image by mapping exposed docker port 80 to internal service port 5052 by using the following command. If port 80 is already in use by another app, then just replace the port number 80 with another port number.

``
docker run -p 80:5052 tree_retrieval:v0.0.1
``

**5.** Now test the service using the following command:

``
curl -X POST "http://localhost:5052/phylotastic_ws/gt/ot/tree" -H "content-type:application/json" -d '{"taxa": ["Setophaga striata","Setophaga magnolia","Setophaga angelae","Setophaga plumbea","Setophaga virens"]}'
``
