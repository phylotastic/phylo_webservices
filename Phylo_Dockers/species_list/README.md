### Instructions to setup species_list app docker. 

**1.** Download the directory named *species_list*.

**2.** Go to the *species_list* directory and run the following command:

``
docker-compose build
``
> To rebuild everything use `--no-cache` at the end of the above command.

**3.** Now run the container using the following command.
``
docker-compose up
``

> Assuming that the exposed host port is 5055. 


**5.** Now test the service using the following commands:

#### Example 1: (get all public lists)
``
curl -X GET 'http://localhost:5055/phylotastic_ws/sls/get_list'
``


