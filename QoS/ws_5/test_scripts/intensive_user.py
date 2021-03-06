import requests
import time
import json
from os.path import dirname, abspath

class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        d = dirname(dirname(dirname(abspath(__file__)))) # get parent of parent of current directory
        names_list = self.read_data(d+"/test_data/seaweed_plants.txt")
        
        sc_names = ""
        for indx, name in enumerate(names_list):
            sc_names += name
            if indx != len(names_list)-1:
               sc_names += "|"
 
        self.query_param = {'taxa': sc_names}
        

    def read_data(self,file_path):
        text_file = open(file_path, "r")
        data_list = text_file.read().split('\n')
        #print len(data_list)
        text_file.close()
       
        return data_list


    def run(self):
        start_timer = time.time()
        response = requests.get('http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/ot/get_tree', params=self.query_param)

        latency = time.time() - start_timer

        self.custom_timers['Latency'] = latency
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    #print trans.custom_timers
