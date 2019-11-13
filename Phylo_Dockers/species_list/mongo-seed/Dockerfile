FROM mongo

COPY userSpecieslist.json /userSpecieslist.json

CMD mongoimport --host mongodb --db SpeciesList --mode upsert --type json --file /userSpecieslist.json
#CMD mongorestore --host=127.0.0.1 --port=27017 /mongo_seed/



