### Build the docker image
```bash
$ sudo docker build -t phylor . 
```
(where . – the current directory – is the directory where that Dockerfile is stored).

---

### List docker images to check the recent image built
```bash
$ sudo docker images
```
---

### Run the docker image, passing in the application’s directory as a volume
```bash
$ sudo docker run --rm -p 8000:8000 -v `pwd`/supertree_service.R:/plumber.R -v /var/web_service/treebase/data/output:/data/output phylor:latest /plumber.R
```

---

### Check the docker container
```bash
$ sudo docker ps
```

---

### Stop daemonized docker container
```bash
$ sudo docker stop <image id>
```

---

### Remove docker image
```bash
$ sudo docker rmi <image id>
```
---


### Check the status of treebase in phylor
```bash
$ curl "http://phylo.cs.nmsu.edu:8000/treebase_status"
```

### Example command to invoke treebase service  
```bash
$ curl -X POST "http://phylo.cs.nmsu.edu:5012/phylotastic_ws/gt/tb/tree" -H "content-type:application/json" -d '{"taxa":["Panthera pardus", "Taxidea taxus", "Enhydra lutris", "Lutra lutra", "Canis latrans", "Canis lupus", "Mustela altaica", "Mustela eversmanni", "Martes americana", "Ictonyx striatus", "Canis anthus", "Lycalopex vetulus", "Lycalopex culpaeus", "Puma concolor", "Felis catus","Leopardus jacobita"]}'
```

