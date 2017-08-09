from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
import credentials #for database credentials

DB_NAME = 'qos'

TABLES = {}
TABLES['qos_session'] = (
    "CREATE TABLE `qos_session` ("
    "  `qos_id` int(11) NOT NULL,"
    "  `session_id` int(11) NOT NULL,"
    "  `session_start_time` datetime NOT NULL,"
    "  PRIMARY KEY (`qos_id`, `session_id`)"
    ") ENGINE=InnoDB")


TABLES['qos_updown'] = (
    "CREATE TABLE `qos_updown` ("
	"  `updown_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `ws_id` varchar(8) NOT NULL,"
	"  `qos_id` int(11) NOT NULL,"
    "  `session_id` int(11) NOT NULL,"
    "  `state` char(1) NOT NULL,"
    "  `state_updated` datetime NOT NULL,"
    "  PRIMARY KEY (`updown_id`),"
    "  CONSTRAINT `wsid_qsid_sessid_fk` FOREIGN KEY (`qos_id`, `session_id`) "
    "     REFERENCES `qos_session` (`qos_id`, `session_id`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")



db_user = credentials.mysql['user']
db_pass = credentials.mysql['password']

cnx = mysql.connector.connect(user=db_user,password=db_pass,host='localhost')

cursor = cnx.cursor()

try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

print ("Connected")

for name, ddl in TABLES.iteritems():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()

#-------------------------
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

