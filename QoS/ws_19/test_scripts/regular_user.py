import requests
import time


class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        self.query_param = {'taxa': "Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens"}

    def run(self):
        start_timer = time.time()
        response = requests.get('http://phylo.cs.nmsu.edu:5004/phylotastic_ws/gt/pt/get_tree', params=self.query_param)
        latency = time.time() - start_timer

        self.custom_timers['Latency'] = latency
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    #print trans.custom_timers
