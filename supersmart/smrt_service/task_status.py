from .celery import app
import sys

# Add the smrt_service package folder path to the sys.path list
sys.path.append('/var/web_service/supersmart/smrt_service/')
import db_task

def get_task_status(task_id):
	task = app.AsyncResult(task_id)
	
	if task.state == 'PENDING':
		# job has not started yet
		response = {
			'job_state': task.state,
			'current_step': 0,
			'total_steps': 12,
			'status_code': 200,
			'job_status': 'job has not started yet..',
            'message': "Success"
		}
	elif task.state == 'PROGRESS': #custom state name
		response = {
			'tree_id': task.info['tree_id'],           
			'current_step': task.info['current_step'],
			'total_steps': task.info['total_steps'], 
			'job_state' : task.state,
			'status_code' : 200,    
			'job_status' : task.info['status'],
            'message': "Success"          
		}
	else:
		response = {
			'total_steps': 12,
			'status_code': 200,
            'message': "Success"
		}  
		tree_id, job_status, cur_step, ex_time = db_task.query_jid_db(task_id)
		if tree_id is not None:
			if cur_step == 12:
				response['job_state'] = "SUCCESS"
				response['job_status'] = "completed"
				response['execution_time'] = ex_time
				response['tree_id'] = tree_id
			else:
				response['job_status'] = "Error in step %d: %s"%(cur_step+1, job_status)
				response['job_state'] = "FAILURE"
		else:
			response['status_code'] = 500
			response['message'] = "Could not retrieve any status"
	'''   
	else:
		# something went wrong in the background job
		response = {
			'job_state': task.state,
			'current_step': 0,
			'status_code': 200,
			'total_steps': 12,
			'job_status': str(task.info),  # this is the exception raised
            'message': "Success" 
	    }
	#except KeyError, e:   
	#	return {'job_state':"Error: %s"%str(e)}
	'''

	return response

