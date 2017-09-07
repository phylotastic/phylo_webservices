import os
import sys
import json
import time
import datetime
import csv
from os.path import dirname, abspath

from database import DatabaseAPI 

#---------------------------------------------
def get_subdirectories(dir_path):
	sub_dirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
	#print sub_dirs
	return sub_dirs  

#-------------------------------------------
def read_results_file(ws_Id, file_path):
	fail_count = 0
	total_count = 0
	with open(file_path+"/"+"results.csv", 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar="'")
		for row in csvreader:
			total_count += 1
			if row[5] != "":
				fail_count += 1
			duration = float(row[1])

	success_count = total_count-fail_count
	
	record = {}
	#print "Total number of requests: %d"%total_count	
	#print "Number of failed requests: %d"%fail_count
	#print "Number of successful requests: %d"%(success_count)
	#print "Total duration: %f"%duration
	#print "Throughput: %f RPS"%(float(success_count)/duration)

	record['ws_id'] = ws_Id
	record['total_req'] = total_count
	record['fail_req'] = fail_count
	record['duration'] = duration
	
	ts = time.time()
	update_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')	
	record['date'] = update_time

	return record

#------------------------------------------
def insert_record_db(data_row):
	
	#create a database connection
	db = DatabaseAPI("qos")

	#insert all data rows into database
	db.insert_db_single( "qos_throughput", ["ws_id", "total_requests", "failed_requests", "duration", "thrpt_updated"], (data_row['ws_id'],data_row['total_req'], data_row['fail_req'], data_row['duration'], data_row['date']) )

#-----------------------------------------
def get_result_dir(dpath):
	result_dir = None
	sub_dirs = get_subdirectories(dpath)
	#print sub_dirs
	#convert current date to string
	str_date = datetime.datetime.now().strftime("%Y.%m.%d")
	#print str_date
	for sb_dr in sub_dirs:
		#print sb_dr 
		if str_date in sb_dr:
			result_dir = sb_dr
			break
	
	return result_dir

#---------------------------------------
if __name__ == "__main__":

	ws = sys.argv[1] #web service id
	
	d = dirname(abspath(__file__)) # get current directory
	
	#print "Collecting results for webservice %s"%ws
	dpath = d + "/" + ws + "/results/"
	result_dir = get_result_dir(dpath)
	if result_dir is None:
		print "No results directory found for %s"%ws	
	else:
		file_path = dpath + result_dir 
		data_record = read_results_file(ws, file_path)
		insert_record_db(data_record)
	
