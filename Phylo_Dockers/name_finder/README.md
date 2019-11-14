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

**4.**  To use files as input to the app, this docker must mount a local host directory containing the input files and run the docker image using the following command.

> Replace the *host-directory* with the complete path of the input directory in localhost.

``
docker run -it --volume <host-directory>:/name_finder/data -p 5050:5050 name_finder:v0.0.1
``

> Assuming that the exposed host port is 5050. 


**5.** Now test the service using the following commands:

#### Example 1: (input file)
``
curl -X POST 'http://localhost:5050/phylotastic_ws/fn/names_file' -F 'inputFile=@scnames.txt' -F 'engine=2'
``

#### Example 2: (input url)
``
curl -X GET 'http://localhost:5050/phylotastic_ws/fn/names_url?url=https://en.wikipedia.org/wiki/Plain_pigeon&engine=1'
``

