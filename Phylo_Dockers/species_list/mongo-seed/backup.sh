#!/bin/sh
backups=$dir"/species_list/backups"
PREFIX="mongodb"
HOST="mongodb"
INTERVAL=10

echo "Backup Directory: "$backups
echo "Backups: host=${HOST} prefix=${PREFIX}, interval=${INTERVAL}"

while true; do
  ts=$(date -Iseconds)
  archive="${backups}/${PREFIX}-${ts}"

  if mongodump --host=${HOST} --out "${archive}" "$@"; then
    if [ -d ${archive} ]; then
      tar -C ${archive} -c -f ${archive}.tgz . && rm -rf ${archive}
      echo "Created backup: ${archive}.tgz"
    else
      echo "ERROR: failed to create backup $archive"
    fi
  else
    echo "ERROR ($?) : failed to create backup"
  fi

  if [ ${INTERVAL} -gt 0 ]; then
    sleep ${INTERVAL}
  else
    break
  fi
done
