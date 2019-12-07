### Instructions to setup tree_viewer_app

1. Build the image first.

``
docker-compose build
``

2. Run the container.

``
docker-compose up
``
  
### Test

``
curl -X POST http://localhost:8989/ete_pro/get_tree_image -H "content-type:application/json" -d '{"tree_newick": "(((Rangifer tarandus, Cervus elaphus)Cervidae, (Bos taurus, Ovis orientalis)Bovidae), (Suricata suricatta, (Cistophora cristata,Mephitis mephitis))Carnivora);" ,"tree_id": 12, "actions": ""}'
``

