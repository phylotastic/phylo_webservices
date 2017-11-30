import os
import sys
import time
import vagrant
import tee
from fabric.api import env, execute, task, run
from fabric.api import settings, abort
from fabric.context_managers import cd
from datetime import datetime
from os.path import dirname, abspath

#==================================================
@task
def taxize_task(vm_host_dir, output_dir_name, input_file_name):
	with tee.StdoutTee(vm_host_dir+"/log/"+output_dir_name+"_access.txt", mode="a"), tee.StderrTee(vm_host_dir+"/log/"+output_dir_name+"_error.txt", mode="a"):
		dt = datetime.now()
		dt_str = dt.strftime('%m-%d-%Y %H:%M:%S')
		sys.stdout.write("====start taxize execution====\n")
		sys.stdout.write("======"+dt_str+"======\n")
		#logging in stderr
		sys.stderr.write("====start taxize execution====\n")
		sys.stderr.write("======"+dt_str+"======\n")

		with settings(warn_only=True):
			with cd('/home/vagrant/'+output_dir_name+'/'):
				run_status = run('smrt taxize -i '+input_file_name)
				if run_status.failed:
					return False
				else:
					return True

#----------------------------------------------------
@task
def align_task(vm_host_dir, output_dir_name, input_file_name="species.tsv"):
	with tee.StdoutTee(vm_host_dir+"/log/"+output_dir_name+"_access.txt", mode="a"), tee.StderrTee(vm_host_dir+"/log/"+output_dir_name+"_error.txt", mode="a"):
		dt = datetime.now()
		dt_str = dt.strftime('%m-%d-%Y %H:%M:%S')
		sys.stdout.write("====start align execution====\n")
		sys.stdout.write("======"+dt_str+"======\n")
		#logging in stderr
		sys.stderr.write("====start align execution====\n")
		sys.stderr.write("======"+dt_str+"======\n")

		with settings(warn_only=True):
			with cd('/home/vagrant/'+output_dir_name+'/'):
				run_status = run('smrt align --infile '+input_file_name)
				if run_status.failed:
					return False
				else:
					return True

#-----------------------------------------------------
@task
def orthologize_task(vm_host_dir, output_dir_name, input_file_name="aligned.txt"):
	with tee.StdoutTee(vm_host_dir+"/log/"+output_dir_name+"_access.txt", mode="a"), tee.StderrTee(vm_host_dir+"/log/"+output_dir_name+"_error.txt", mode="a"):
		dt = datetime.now()
		dt_str = dt.strftime('%m-%d-%Y %H:%M:%S')
		sys.stdout.write("====start orthologize execution====\n")
		sys.stdout.write("======"+dt_str+"======\n")
		#logging in stderr
		sys.stderr.write("====start orthologize execution====\n")
		sys.stderr.write("======"+dt_str+"======\n")

		with settings(warn_only=True):
			with cd('/home/vagrant/'+output_dir_name+'/'):
				run_status = run('smrt orthologize --infile '+input_file_name)
				if run_status.failed:
					return False
				else:
					return True

#-----------------------------------------------------
@task
def bbmerge_task(vm_host_dir, output_dir_name, input_file_name="species.tsv"):
	with tee.StdoutTee(vm_host_dir+"/log/"+output_dir_name+"_access.txt", mode="a"), tee.StderrTee(vm_host_dir+"/log/"+output_dir_name+"_error.txt", mode="a"):
		dt = datetime.now()
		dt_str = dt.strftime('%m-%d-%Y %H:%M:%S')
		sys.stdout.write("====start bbmerge execution====\n")
		sys.stdout.write("======"+dt_str+"======\n")
		#logging in stderr
		sys.stderr.write("====start bbmerge execution====\n")
		sys.stderr.write("======"+dt_str+"======\n")

		with settings(warn_only=True):
			with cd('/home/vagrant/'+output_dir_name+'/'):
				run_status = run('smrt bbmerge --alnfile merged.txt --taxafile '+input_file_name)
				if run_status.failed:
					return False
				else:
					return True

#---------------------------------------------------
@task
def bbinfer_task(vm_host_dir, output_dir_name):
	with tee.StdoutTee(vm_host_dir+"/log/"+output_dir_name+"_access.txt", mode="a"), tee.StderrTee(vm_host_dir+"/log/"+output_dir_name+"_error.txt", mode="a"):
		dt = datetime.now()
		dt_str = dt.strftime('%m-%d-%Y %H:%M:%S')
		sys.stdout.write("====start bbinfer execution====\n")
		sys.stdout.write("======"+dt_str+"======\n")
		#logging in stderr
		sys.stderr.write("====start bbinfer execution====\n")
		sys.stderr.write("======"+dt_str+"======\n")

		with settings(warn_only=True):
			with cd('/home/vagrant/'+output_dir_name+'/'):
				run_status = run('smrt bbinfer --supermatrix supermatrix.phy --inferencetool exabayes --cleanup')
				if run_status.failed:
					return False
				else:
					return True

#------------------------------------------------
@task
def bbreroot_task(vm_host_dir, output_dir_name, input_file_name="species.tsv"):
	with tee.StdoutTee(vm_host_dir+"/log/"+output_dir_name+"_access.txt", mode="a"), tee.StderrTee(vm_host_dir+"/log/"+output_dir_name+"_error.txt", mode="a"):
		dt = datetime.now()
		dt_str = dt.strftime('%m-%d-%Y %H:%M:%S')
		sys.stdout.write("====start bbreroot execution====\n")
		sys.stdout.write("======"+dt_str+"======\n")
		#logging in stderr
		sys.stderr.write("====start bbreroot execution====\n")
		sys.stderr.write("======"+dt_str+"======\n")

		with settings(warn_only=True):
			with cd('/home/vagrant/'+output_dir_name+'/'):
				run_status = run('smrt bbreroot --backbone backbone.dnd --taxafile '+input_file_name+' --smooth')
				if run_status.failed:
					return False
				else:
					return True

#----------------------------------------------------
@task
def consense_task(vm_host_dir, output_dir_name, input_file_name="backbone-rerooted.dnd"):
	with tee.StdoutTee(vm_host_dir+"/log/"+output_dir_name+"_access.txt", mode="a"), tee.StderrTee(vm_host_dir+"/log/"+output_dir_name+"_error.txt", mode="a"):
		dt = datetime.now()
		dt_str = dt.strftime('%m-%d-%Y %H:%M:%S')
		sys.stdout.write("====start consense execution====\n")
		sys.stdout.write("======"+dt_str+"======\n")
		#logging in stderr
		sys.stderr.write("====start consense execution====\n")
		sys.stderr.write("======"+dt_str+"======\n")

		with settings(warn_only=True):
			with cd('/home/vagrant/'+output_dir_name+'/'):
				run_status = run('smrt consense -i '+input_file_name)
				if run_status.failed:
					return False
				else:
					return True

#-----------------------------------------------------
@task
def mkdir_task(vm_host_dir, output_dir_name):
	with tee.StdoutTee(vm_host_dir+"/log/"+output_dir_name+"_access.txt", mode="a"), tee.StderrTee(vm_host_dir+"/log/"+output_dir_name+"_error.txt", mode="a"):
		dt = datetime.now()
		dt_str = dt.strftime('%m-%d-%Y %H:%M:%S')
		sys.stdout.write("====start mkdir execution====\n")
		sys.stdout.write("======"+dt_str+"======\n")
		#logging in stderr
		sys.stderr.write("====start mkdir execution====\n")
		sys.stderr.write("======"+dt_str+"======\n")

		with settings(warn_only=True):
			run_status = run("mkdir -p /home/vagrant/"+output_dir_name)
			if run_status.failed:
				return False
			else:
				return True

#-------------------------------------------------------
@task
def cp_task(vm_host_dir, output_dir_name, source, destination):
	with tee.StdoutTee(vm_host_dir+"/log/"+output_dir_name+"_access.txt", mode="a"), tee.StderrTee(vm_host_dir+"/log/"+output_dir_name+"_error.txt", mode="a"):
		dt = datetime.now()
		dt_str = dt.strftime('%m-%d-%Y %H:%M:%S')
		sys.stdout.write("====start cp execution====\n")
		sys.stdout.write("======"+dt_str+"======\n")
		#logging in stderr
		sys.stderr.write("====start cp execution====\n")
		sys.stderr.write("======"+dt_str+"======\n")

		with settings(warn_only=True):
			run_status = run('cp '+ source + ' '+ destination)
			if run_status.failed:
				return False
			else:
				return True

#===================================================
@task
def chmod_task(vm_host_dir, output_dir_name, file_name, permissions="666"):
	with tee.StdoutTee(vm_host_dir+"/log/"+output_dir_name+"_access.txt", mode="a"), tee.StderrTee(vm_host_dir+"/log/"+output_dir_name+"_error.txt", mode="a"):
		dt = datetime.now()
		dt_str = dt.strftime('%m-%d-%Y %H:%M:%S')
		sys.stdout.write("====start chmod execution====\n")
		sys.stdout.write("======"+dt_str+"======\n")
		#logging in stderr
		sys.stderr.write("====start chmod execution====\n")
		sys.stderr.write("======"+dt_str+"======\n")

		with settings(warn_only=True):
			with cd('/home/vagrant/'+output_dir_name+'/'):
				run_status = run('chmod '+ permissions + ' '+ file_name)
				if run_status.failed:
					return False
				else:
					return True

#--------------------------------------------------
def execute_smrt_task(task_name, task_args=None):
	#get the host directory path where Vagrantfile is located
	smrt_vm_host_dir = dirname(dirname(abspath(__file__)))
	#initialize the virtual machine directory and host name
	v = vagrant.Vagrant(root=smrt_vm_host_dir)
	env.hosts = [v.user_hostname_port()]
	env.key_filename = v.keyfile()

	if task_name == "taxize":	
		result = execute(taxize_task, smrt_vm_host_dir, task_args[0], task_args[1])
	elif task_name == "align":	
		result = execute(align_task, smrt_vm_host_dir, task_args[0])
	elif task_name == "orthologize":	
		result = execute(orthologize_task, smrt_vm_host_dir, task_args[0])
	elif task_name == "bbmerge":	
		result = execute(bbmerge_task, smrt_vm_host_dir, task_args[0])
	elif task_name == "bbinfer":	
		result = execute(bbinfer_task, smrt_vm_host_dir, task_args[0])
	elif task_name == "bbreroot":	
		result = execute(bbreroot_task, smrt_vm_host_dir, task_args[0])
	elif task_name == "consense":	
		result = execute(consense_task, smrt_vm_host_dir, task_args[0])
	elif task_name == "mkdir":	
		result = execute(mkdir_task, smrt_vm_host_dir, task_args[0])
	elif task_name == "cp":	
		result = execute(cp_task, smrt_vm_host_dir, task_args[0], task_args[1], task_args[2])
	elif task_name == "chmod":	
		result = execute(chmod_task, smrt_vm_host_dir, task_args[0], task_args[1])

	# output returned by execute: {'vagrant@127.0.0.1:2222': True} or {'vagrant@127.0.0.1:2222': False}
	return result[v.user_hostname_port()] 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':
	#print execute_smrt_task("mkdir", ["Arctocephalus"])
	#print execute_smrt_task("cp", ["Arctocephalus", "/vagrant/input/seal_species_Arctocephalus.txt", "/home/vagrant/Arctocephalus/seal_species_Arctocephalus.txt"])
	#print execute_smrt_task("taxize", ["Arctocephalus", "seal_species_Arctocephalus.txt"])
	#print execute_smrt_task("align", ["Arctocephalus"])
	#print execute_smrt_task("orthologize", ["Arctocephalus"])
	#print execute_smrt_task("bbmerge", ["Arctocephalus"])
	#print execute_smrt_task("bbinfer", ["Arctocephalus"])
	#print execute_smrt_task("bbreroot", ["Arctocephalus"])
	#print execute_smrt_task("consense", ["Arctocephalus"])
