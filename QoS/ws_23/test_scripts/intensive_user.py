import requests
import time
import json
from os.path import dirname, abspath

class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        d = dirname(dirname(dirname(abspath(__file__)))) # get parent of parent of current directory
        names_list = self.read_data(d+"/test_data/plants.txt")
        self.post_body = {"scientificNames": names_list}
        

    def read_data(self,file_path):
        text_file = open(file_path, "r")
        data_list = text_file.read().split('\n')
        #print len(data_list)
        text_file.close()
       
        return data_list


    def run(self):
        start_timer = time.time()
        jsonPayload = json.dumps(self.post_body)
        response = requests.post("http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/ip/names", data=jsonPayload, headers={'content-type': 'application/json'})

        latency = time.time() - start_timer

        self.custom_timers['Latency'] = latency
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    #print trans.custom_timers
