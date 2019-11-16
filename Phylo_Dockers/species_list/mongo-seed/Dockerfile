FROM mongo

#COPY userSpecieslist.json /userSpecieslist.json
COPY . /

CMD mongoimport --host mongodb --db SpeciesList --mode upsert --type json --file /seed/userSpecieslist.json

CMD mongoimport --host mongodb --db SpeciesList --mode upsert --type json --file /seed/listCounter.json

#CMD mongorestore --host mongodb /seed/

RUN chmod +x /backup.sh

#ENTRYPOINT ["./backup.sh &"]

#RUN nohup bash -c "sh /backup.sh &"
CMD ["/backup.sh"]


