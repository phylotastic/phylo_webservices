import os
import json

def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                # Join the two strings in order to form the full filepath.
            	filepath = os.path.join(root, filename)
            	file_paths.append(filepath)  # Add it to the list.
    
    #print file_paths
    return file_paths

#-------------------------------------------
def filter_files(file_list, filter_str):
 	files = []
 	for filename in file_list:
 		if (filename.find(filter_str)>=0):
 			files.append(filename)
 	return files

#-----------------------------------------
def find_outputfile(file_list, file_num):
 	outputfile = "output_" + str(file_num)
 	for filename in file_list:
 		if (filename.find(outputfile)>=0):
 			return filename

#-----------------------------------------
def get_file_num(filename):
 	index_ext = filename.rfind(".")
 	index_unds = filename.rfind("_")

 	return filename[index_unds+1:index_ext]

#-------------------------------------------
def create_list_file(filename):
 	file_content_lst = [] 	
 	fileObj = open(filename, 'r')

 	for line in fileObj:
 		file_content_lst.append(line.strip())
 	
 	fileObj.close()

 	return file_content_lst 	

#-------------------------------------------
def create_content_file(filename): 	
 	fileObj = open(filename, 'r')
 	file_content = fileObj.read()  
 	fileObj.close()

 	return file_content 	

#-----------------------------------------
def prepare_json_input(init_str, input_list):
	json_input = init_str
	count = 0	
	for item in input_list:
		json_input = json_input + '"' + item + '"'
		count = count + 1 
		if count != len(input_list):
			json_input = json_input + ","

	json_input = json_input + "]}"
	return json_input
