### Instructions to setup name_converter app docker. 

**1.** Download the directory named *name_converter*.

**2.** Go to the *name_converter* directory and run the following command:

``
docker build -t name_converter:v0.0.1 .
``
> To rebuild everything use `--no-cache` at the end of the above command.

**3.** Check whether the docker image *name_converter* has been built by listing all containers:

``
docker images
``

**4.**  Run the docker image by mapping exposed docker port 5057 to internal service port 5057 by using the following command. 

``
docker run -p 5057:5057 name_converter:v0.0.1
``

> Assuming that the exposed host port is 5057. 


**5.** Now open a new terminal and test the service using the following commands:

#### Example 1:

``
curl -X POST "http://localhost:5057/phylotastic_ws/cs/ncbi/scientific_names" -H "content-type:application/json" -d '{"commonnames": ["cattle", "cat", "goat", "pig", "sheep", "duck", "chicken", "horse", "domestic dog"]}'
``

#### Example 2: 
``
curl -X POST "http://localhost:5057/phylotastic_ws/ss/gnr/common_names" -H "content-type:application/json" -d '{"scientific_names": ["Felis catus", "Bos taurus"]}'
``

**6.** To stop the service press `CTRL+C`.

**7.** To run the docker image in background mode, use the following command.

``
docker run -d --rm -p 5057:5057 --name name_converter name_converter:v0.0.1
`` 

**8.** To check whether the docker image is running in the background, use the following command and check the <IMAGE_ID>.

``
docker ps
``

**9.** To stop the docker image from running, use the following command.

``
docker stop <IMAGE_ID>
``

