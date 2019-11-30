import subprocess
import os
# Define command and arguments
command = 'Rscript'

path2script = os.getcwd() +"/" +"service/"

#https://www.r-bloggers.com/integrating-python-and-r-part-ii-executing-r-from-python-and-vice-versa/
def remove_singleton(tree_nwk):

	script_name = 'remove_singleton.R'
	# Build subprocess command
	cmd = [command, path2script + script_name, tree_nwk]
	
	# check_output will run the command and store to result
	#x = subprocess.check_output(cmd, shell=True, universal_newlines=True)
	
	process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	returncode = process.wait()
	print('cmd returned {0}'.format(returncode))
	x = process.stdout.read()
	#print(x)
	return x

#----------------------------------------------------

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#if __name__ == '__main__':
#	input_tree = "((((Setophaga_striata_ott60236)mrcaott22834ott60236)mrcaott22834ott455853)mrcaott22834ott285200,Setophaga_plumbea_ott45750,Setophaga_angelae_ott381849,Setophaga_magnolia_ott532751,Setophaga_virens_ott1014098)Setophaga_ott285198;"
#	remove_singleton(input_tree)
#	input_tree = "((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);"

