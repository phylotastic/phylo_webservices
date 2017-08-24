import os
import json
import time
import datetime
import csv

#---------------------------------------------
file_path = "/home/tayeen/TayeenFolders/PythonFiles/qos/ws_3/results/"
#---------------------------------------------
def get_subdirectories():
	sub_dirs = [d for d in os.listdir(file_path) if os.path.isdir(os.path.join(file_path, d))]
	#print sub_dirs
	return sub_dirs  

#-------------------------------------------
def read_results_file(file_name):
	sub_dirs = get_subdirectories()
	fail_count = 0
	total_count = 0
	with open(file_path+sub_dirs[0]+"/"+file_name, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar="'")
		for row in csvreader:
			total_count += 1
			if row[5] != "":
				fail_count += 1
			duration = float(row[1])

	success_count = total_count-fail_count
	print "Total number of requests: %d"%total_count	
	print "Number of failed requests: %d"%fail_count
	print "Number of successful requests: %d"%(success_count)
	print "Total duration: %f"%duration
	print "Throughput: %f RPS"%(float(success_count)/duration)

#------------------------------------------

#-----------------------------------------

if __name__ == "__main__":

	read_results_file("results.csv")
	
	
	
