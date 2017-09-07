import time
import datetime
from database import DatabaseAPI

#-----------------------------------------
def compute_avlty(sid):
    
	db_result = {}
    #create a database connection
	db = DatabaseAPI("qos")
    #query the table
	query_result = db.query_db("qos_session", ["session_id", "session_start_time"], extra="ORDER BY session_start_time DESC")
	sessionID = int(query_result[0][0])
	sessionStart_str = query_result[0][1].strftime("%Y-%m-%d %H:%M:%S")
	sessionStart = datetime.datetime.strptime(sessionStart_str, "%Y-%m-%d %H:%M:%S")
	#print sessionID
	up_times = get_updown_timestamps(sessionID, sid, "U")
	if len(up_times) == 0:
		db_result['message'] = "No Availability measure found."
		db_result['status_code'] = 204
	else:
		down_times = get_updown_timestamps(sessionID, sid, "D")
		total_down_time = compute_downtime(up_times, down_times)
		#print "Total downtime: %d"%total_down_time	
		monitoring_time = (datetime.datetime.now() - sessionStart).total_seconds()
		#print "Total Monitoring time: %d"%monitoring_time	
		total_uptime = monitoring_time - total_down_time	
		#print "Total uptime: %d"%total_uptime

		availability = (total_uptime / float(monitoring_time))*100
		print "Availability: %f"%(availability)
       
		db_result['message'] = "Success"
		db_result['status_code'] = 200
		db_result['qos_result'] = {'qos_parameter': "availability", 'qos_value': float("{0:.2f}".format(availability)), 'qos_unit': "percentage", 'qos_date_updated': datetime.datetime.now().strftime('%m-%d-%Y')} 
	
	db_result['service_id'] = sid       
	
	return db_result
	
#---------------------------------------------
def get_updown_timestamps(sessionID, sid, state):
	db = DatabaseAPI("qos")
	query_result = db.query_db("qos_updown", ["state", "state_updated"], "session_id = %s AND ws_id = %s AND state = %s", (sessionID, sid, state))
	timestamp_list = []
	for result in query_result:
		# date string to datetime object
		date_str = result[1].strftime("%Y-%m-%d %H:%M:%S")
		dt_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
		#print repr(dt_obj)
		timestamp_list.append(dt_obj)

	return timestamp_list

#---------------------------------------------
def compute_downtime(up_times, down_times):
	total_down_time = 0
	# case 1: when there is no uptime for a webservice that went down last time and the web service went down at least twice
	if len(up_times) == len(down_times) and len(up_times) != 1:
		for indx, ut in enumerate(up_times):
			if indx == 0:
				continue #skip the first time stamp which is the intial timestamp
			time_diff = ut - down_times[indx-1]
			#print time_diff.total_seconds()
	 		total_down_time += time_diff.total_seconds()
			
			if indx == len(down_times)-1:
				time_diff = datetime.datetime.now() - down_times[indx] 
				#print time_diff.total_seconds()
				total_down_time += time_diff.total_seconds()
	# case 2: when there is no uptime for a webservice that went down last time and the web service went down for the first time
	elif len(up_times) == len(down_times) and len(up_times) == 1:
		time_diff = datetime.datetime.now() - down_times[0] 
		#print time_diff.total_seconds()
		total_down_time += time_diff.total_seconds() 
	# case 3: when there is uptime for a webservice that went down at least once
	elif len(up_times) != len(down_times) and len(up_times) != 1:
		for indx, ut in enumerate(up_times):
			if indx == 0:
				continue #skip the first time stamp which is the intial timestamp
			time_diff = ut - down_times[indx-1]
			#print time_diff.total_seconds()
	 		total_down_time += time_diff.total_seconds()
	# case 4: when there is no downtime for a webservice
	elif len(up_times) != len(down_times) and len(down_times) == 0:		
		total_down_time = 0.0
	else:
		total_down_time = 0.0	

	return total_down_time

#--------------------------------------------------------
def compute_rspt(sid):
	table_name = "qos_resptime"
	table_fields = ["ws_id","resp_time","result_updated"]
	table_condition = "ws_id = %s ORDER BY result_updated DESC"

	db_result = {}
	#create a database connection
	db = DatabaseAPI("qos")
	#query the table
	query_result = db.query_db(table_name, table_fields, table_condition, (sid, ))
	if len(query_result) == 0:
		db_result['message'] = "No Response time measure found"
		db_result['status_code'] = 204
	else:
		db_result['message'] = "Success"
		db_result['status_code'] = 200
		db_result['qos_result'] = {'qos_parameter': "response time", 'qos_value': float("{0:.2f}".format(query_result[0][1])), "qos_unit": "seconds" ,'qos_date_updated': query_result[0][2].strftime('%m-%d-%Y')}
 
	db_result['service_id'] = sid

	return db_result

#-------------------------------------------------
def compute_thrpt(sid):
	table_name = "qos_throughput"
	table_fields = ["ws_id","total_requests","failed_requests","duration","thrpt_updated"] 
	table_condition = "ws_id = %s ORDER BY thrpt_updated DESC"

	db_result = {}
	#create a database connection
	db = DatabaseAPI("qos")
    #query the table
	query_result = db.query_db(table_name, table_fields, table_condition, (sid, ))
	if len(query_result) == 0:
		db_result['message'] = "No Throughput measure found"
		db_result['status_code'] = 204
	else:
		db_result['message'] = "Success"
		db_result['status_code'] = 200
       
		total_req = int(query_result[0][1])
		failed_req = int(query_result[0][2])
		duration = float(query_result[0][3])
		throughput_value = (total_req-failed_req)/duration
		db_result['qos_result'] = {'qos_parameter': "throughput", 'qos_value': float("{0:.2f}".format(throughput_value)), 'qos_unit': "requests per second (RPS)", 'qos_date_updated': query_result[0][4].strftime('%m-%d-%Y')} 

	db_result['service_id'] = sid	
	
	return db_result

#---------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':
	#print compute_availability("test2")
