### Instructions to setup name_finder app docker. 

**1.** Download the directory named *name_finder*.

**2.** Go to the *name_finder* directory and run the following command:

``
docker build -t name_finder:v0.0.1 .
``
> To rebuild everything use `--no-cache` at the end of the above command.

**3.** Check whether the docker image *name_finder* has been built by listing all containers:

``
docker images
``

**4.**  To use files as input to the app, this docker must mount a local host directory and run the docker image using the following command.

> Replace the */tmp* with the complete path of the localhost directory.

``
docker run -it --volume /tmp:/name_finder/data -p 5050:5050 name_finder:v0.0.1
``

> Assuming that the exposed host port is 5050. 


**5.** Now open a new terminal and test the service using the following commands:

#### Example 1: (input file)

> To test this example, use the terminal to first go to the directory where the input file *scnames.txt* is located and run the command from there.

``
curl -X POST 'http://localhost:5050/phylotastic_ws/fn/names_file' -F 'inputFile=@scnames.txt' -F 'engine=1'
``

#### Example 2: (input url)
``
curl -X GET 'http://localhost:5050/phylotastic_ws/fn/names_url?url=https://en.wikipedia.org/wiki/Plain_pigeon&engine=1'
``

**6.** To stop the service press `CTRL+C`.

**7.** To run the docker image in background mode, use the following command.

``
docker run -d --rm --volume /tmp:/name_finder/data -p 5050:5050 --name name_finder name_finder:v0.0.1
`` 

**8.** To check whether the docker image is running in the background, use the following command.

``
docker ps
``

**9.** To stop the docker image from running, use the following command.

``
docker stop <IMAGE_ID>
``


