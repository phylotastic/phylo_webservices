FROM mongo

COPY . /

#run the script to import mongodb data and start backing up data
RUN chmod +x /start.sh

CMD ["/start.sh"]

