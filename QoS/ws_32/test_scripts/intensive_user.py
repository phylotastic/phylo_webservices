import requests
import time
import json
from os.path import dirname, abspath

class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        
        self.post_body = {'species': ["Ursus maritimus", "Ailuropoda melanoleuca", "Vulpes lagopus", "Delphinapterus leucas", "Diceros bicornis", "Balaenoptera musculus", "Pan paniscus", "Balaena mysticetus", "Pan troglodytes", "Balaenoptera physalus", "Carcharodon carcharias", "Chelonia mydas", "Hippopotamus amphibius", "Orcaella brevirostris", "Panthera onca", "Dermochelys coriacea", "Ara ararauna", "Amblyrhynchus cristatus"]}

    
    def run(self):
        start_timer = time.time()
        jsonPayload = json.dumps(self.post_body)
        response = requests.post("http://phylo.cs.nmsu.edu:5013/phylotastic_ws/sd/ecos/conservation", data=jsonPayload, headers={'content-type': 'application/json'})
        latency = time.time() - start_timer

        self.custom_timers['Latency'] = latency
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    #print trans.custom_timers
