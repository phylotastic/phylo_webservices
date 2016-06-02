import helper

files_list = helper.get_filepaths("GNRDTestCases")
print files_list
input_files = helper.filter_files(files_list, "input")
output_files = helper.filter_files(files_list, "output")
print input_files
print output_files

