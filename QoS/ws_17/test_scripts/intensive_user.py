import requests
import time
import json
from os.path import dirname, abspath

class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        
        self.post_body = {"list":["Delphinidae","Delphinus capensis","Delphinus delphis","Tursiops truncatus","Tursiops aduncus","Sotalia fluviatilis","Sousa chinensis"], "list_type": "taxa"}

    
    def run(self):
        start_timer = time.time()
        jsonPayload = json.dumps(self.post_body)
        response = requests.post("http://phylo.cs.nmsu.edu:5006/phylotastic_ws/md/studies", data=jsonPayload, headers={'content-type': 'application/json'})
        latency = time.time() - start_timer

        self.custom_timers['Latency'] = latency
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    #print trans.custom_timers
