from __future__ import absolute_import, unicode_literals
from __future__ import with_statement
from .celery import app

import celery
import os
import sys
import time
from os.path import dirname, abspath
from datetime import datetime


# Add the smrt_service package folder path to the sys.path list
sys.path.append('/var/web_service/supersmart/smrt_service/')
import smrt_vm_api as vm
import nexus_and_newick
import db_task

#===========================================================
@app.task(bind=True)
def get_species_tree(self, species_list):
	vm_host_dir = get_smrt_vm_dir()
	#job_id = app.current_task.task_id
	job_id = str(self.request.id)	
	#print job_id
	out_dir_name = log_job_timestamp(job_id)
	input_file_name = prepare_input(vm_host_dir, out_dir_name, species_list)
	total = 12
	current_step = 1
	start = time.time()	
	
	job_status_msg = "Pending"

	mkdir_status, copy_status = False, False 
	#-------Make Job Directory--------------
	mkdir_status = vm.execute_smrt_task("mkdir", [out_dir_name])
	if mkdir_status:
		current_step += 1
		job_status_msg = "created directory for supersmart job"
		self.update_state(state='PROGRESS', meta={'tree_id': out_dir_name,'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
		#-------Copy Input File------------------
		copy_status = vm.execute_smrt_task("cp", [out_dir_name, "/vagrant/input/"+input_file_name, "/home/vagrant/"+out_dir_name+"/"+input_file_name])
		if copy_status:
			current_step += 1
			job_status_msg = "copied input file to supersmart job directory"
			self.update_state(state='PROGRESS', meta={'tree_id': out_dir_name,'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
		else:
			job_status_msg = "failed to copy input file to supersmart job directory"
			#self.update_state(state=celery.states.FAILURE, meta={'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
	else:
		job_status_msg = "failed to create directory for supersmart job"
		#self.update_state(state=celery.states.FAILURE, meta={'current_step': current_step, 'total_steps': total, 'status': job_status_msg})		
		
	#-----Run smrt commands---------------
	taxize_status, align_status, orthologize_status,  bbmerge_status, bbinfer_status, bbreroot_status, consense_status, output_ready = False, False, False, False, False, False, False, False
	if mkdir_status and copy_status:
		#-------Run taxize Command-------------
		taxize_status = vm.execute_smrt_task("taxize", [out_dir_name, input_file_name])
		if taxize_status:
			current_step += 1
			job_status_msg = "ran smrt taxize command"
			self.update_state(state='PROGRESS', meta={'tree_id': out_dir_name,'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
		else:
			job_status_msg = "failed running smrt taxize command"
			#self.update_state(state=celery.states.FAILURE, meta={'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
		#---------------------------------------	
		if taxize_status:
			#-------Run align Command--------------
			align_status = vm.execute_smrt_task("align", [out_dir_name])
			if align_status:
				current_step += 1
				job_status_msg = "ran smrt align command"
				self.update_state(state='PROGRESS', meta={'tree_id': out_dir_name,'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			else:
				job_status_msg = "failed running smrt align command"
				#self.update_state(state=celery.states.FAILURE, meta={'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			#------------------------------------------			
		if taxize_status and align_status:		
			#-------Run orthologize Command--------
			orthologize_status = vm.execute_smrt_task("orthologize", [out_dir_name])
			if orthologize_status:
				current_step += 1
				job_status_msg = "ran smrt orthologize command"
				self.update_state(state='PROGRESS', meta={'tree_id': out_dir_name,'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			else:
				job_status_msg = "failed running smrt orthologize command"	
				#self.update_state(state=celery.states.FAILURE, meta={'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			#--------------------------------------			
		if taxize_status and align_status and orthologize_status:				
			#-------Run bbmerge Command------------
			bbmerge_status = vm.execute_smrt_task("bbmerge", [out_dir_name])
			if bbmerge_status:
				current_step += 1
				job_status_msg = "ran smrt bbmerge command"
				self.update_state(state='PROGRESS', meta={'tree_id': out_dir_name,'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			else:
				job_status_msg = "failed running smrt bbmerge command"
				#self.update_state(state=celery.states.FAILURE, meta={'current_step': current_step, 'total_steps': total, 'status': })
			#--------------------------------------			
		if taxize_status and align_status and orthologize_status and bbmerge_status:
			#-------Run bbinfer Command------------
			bbinfer_status = vm.execute_smrt_task("bbinfer", [out_dir_name])
			if bbinfer_status:
				current_step += 1
				job_status_msg = "ran smrt bbinfer command"
				self.update_state(state='PROGRESS', meta={'tree_id': out_dir_name,'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			else:
				job_status_msg = "failed running smrt bbinfer command"
				self.update_state(state=celery.states.FAILURE, meta={'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			#--------------------------------------			
		if taxize_status and align_status and orthologize_status and bbmerge_status and bbinfer_status:
			#-------Run bbreroot Command-----------
			bbreroot_status = vm.execute_smrt_task("bbreroot", [out_dir_name])
			if bbreroot_status:
				current_step += 1
				job_status_msg = "ran smrt bbreroot command"
				self.update_state(state='PROGRESS', meta={'tree_id': out_dir_name,'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			else:
				job_status_msg = "failed running smrt bbreroot command"
				self.update_state(state=celery.states.FAILURE, meta={'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			#--------------------------------------
		if taxize_status and align_status and orthologize_status and bbmerge_status and bbinfer_status and bbreroot_status:			
			#-------Run consense Command-----------
			consense_status = vm.execute_smrt_task("consense", [out_dir_name])
			if consense_status:
				current_step += 1
				job_status_msg = "ran smrt consense command"
				self.update_state(state='PROGRESS', meta={'tree_id': out_dir_name,'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			else:
				job_status_msg = "failed running smrt consense command"
				self.update_state(state=celery.states.FAILURE, meta={'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			#--------------------------------------			
		if taxize_status and align_status and orthologize_status and bbmerge_status and bbinfer_status and bbreroot_status and consense_status:
			#-------Change file permissions---------
			chmod_1 = vm.execute_smrt_task("chmod", [out_dir_name, "consensus.nex"])
			chmod_2 = vm.execute_smrt_task("chmod", [out_dir_name, "backbone.dnd"])
			chmod_3 = vm.execute_smrt_task("chmod", [out_dir_name, "backbone-rerooted.dnd"])
			if chmod_1 and (chmod_2 or chmod_3):
				output_ready = True
				current_step += 1
				job_status_msg = "changed output file permissions"
				self.update_state(state=celery.states.FAILURE, meta={'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
			else:
				job_status_msg = "failed changing output file permissions"
				self.update_state(state='PROGRESS', meta={'tree_id': out_dir_name,'current_step': current_step, 'total_steps': total, 'status': job_status_msg})
				output_ready = False
					
		if output_ready:
			#-------Copy output files--------------- 
			chmod_4 = vm.execute_smrt_task("cp", [out_dir_name, "/home/vagrant/"+out_dir_name+"/consensus.nex", "/vagrant/output/"+out_dir_name+"_consensus.nex"])
			if chmod_4:
				current_step += 1
				job_status_msg = "Completed"
				self.update_state(state='SUCCESS', meta={'current_step': current_step, 'total_steps': total, 'status': job_status_msg, 'tree_id': out_dir_name})	 
				output_tree_newick, output_tree_nexus = read_output(vm_host_dir, out_dir_name)

	end = time.time()
	execution_time = (end-start)
	
	db_task.insert_db(out_dir_name, job_id, job_status_msg, execution_time, current_step)
	
	#print "Total time: %d seconds"%(execution_time)
	
#--------------------------------------------------
def log_job_timestamp(job_id):
	dt = datetime.now()
	dt_str = dt.strftime('%m%d%Y%H%M%S')
	sys.stdout.write("starting "+job_id+" execution\n")
	sys.stdout.write("=========="+dt_str+"==========\n")
	sys.stderr.write("starting "+job_id+" execution\n")
	sys.stderr.write("=========="+dt_str+"==========\n")
	dir_name = job_id[:5] + "-" + dt_str

	return dir_name

#--------------------------------------------------
def get_smrt_vm_dir():
	smrt_vm_dir = dirname(dirname(abspath(__file__)))	
	#print smrt_vm_dir
	return smrt_vm_dir

#--------------------------------------------------
def prepare_input(host_dir, dir_name, species_list):
	input_file_name = dir_name+"_input.txt"
	total = len(species_list)
	with open(host_dir+"/input/"+input_file_name, "w") as in_file:
		count = 0
		for sp in species_list:
			in_file.write(sp)
			count += 1
			if count != total:
				in_file.write("\n")

	return input_file_name

#-------------------------------------------------
def read_output(host_dir, dir_name):
	newick_tree, nexus_tree_block = None, None 
	nexus_and_newick.nexus_to_newick_file(host_dir+"/output/", dir_name+"_consensus.nex", host_dir+"/output/", dir_name+"_consensus.nhx")
	newick_tree = nexus_and_newick.read_newick_tree(host_dir+"/output/", dir_name+"_consensus.nhx")	
	nexus_tree_block = nexus_and_newick.read_nexus_tree(host_dir+"/output/", dir_name+"_consensus.nex")

	return newick_tree, nexus_tree_block

#--------------------------------------------------

