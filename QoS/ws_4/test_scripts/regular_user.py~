import requests
import time


class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        self.query_param = {'names': "Setophaga striata|Setophaga megnolia|Setophaga angilae|Setophaga plumbea|Setophaga virens"}

    def run(self):
        start_timer = time.time()
        response = requests.get('http://phylo.cs.nmsu.edu:5004/phylotastic_ws/tnrs/gnr/resolve', params=self.query_param)
        latency = time.time() - start_timer

        self.custom_timers['Latency'] = latency
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    #print trans.custom_timers
