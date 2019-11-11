###Instructions to setup name_finder app docker. 

**1.** Download the directory named *name_finder*.

**2.** Go to the *name_finder* directory and run the following command:

``
docker build -t name_finder:v0.0.1 .
``

**3.** Check whether the docker image *name_finder* has been built by listing all containers:

``
docker images

``

**4.** Run the docker image by mapping exposed docker port 80 to internal service port 5050 by using the following command. If port 80 is already in use by another app, then just replace the port number 80 with another port number.

``
docker run -p 80:5050 name_finder:v0.0.1
``

**5.** Now test the service using the following command:

Note> Assuming that the exposed host port is 5050. 
 
``
curl -X GET 'http://localhost:5050/phylotastic_ws/fn/names_url?url=https://en.wikipedia.org/wiki/Plain_pigeon&engine=1'
``

**6.**  To use files as input to the app, mount a local host directory containing the input files and run the docker image using the following command.

Note> Replace the <host directory> with the complete path of the input directory in localhost.

``
docker run -it --volume <host directory>:/name_finder/data -p 5050:5050 name_finder:v0.0.1
``

**7.** Now test the service with an input file using the following command:

Note> Replace the <input file> with the input file name that resides in the input directory of the localhost.

``
curl -X GET 'http://localhost:5050/phylotastic_ws/fn/names_file?file_name=<input file>
``

