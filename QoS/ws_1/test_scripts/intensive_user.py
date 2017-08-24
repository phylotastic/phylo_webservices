import requests
import time


class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        #self.post_body = {"species": ["Catopuma badia","Catopuma temminckii"]}
        self.query_param = {'url': 'http://en.wikipedia.org/wiki/Ant'}

    def run(self):
        #payload = {'url': 'https://en.wikipedia.org/wiki/Plain_pigeon'}
        start_timer = time.time()
        response = requests.get('http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_url', params=self.query_param)
        latency = time.time() - start_timer

        #jsonPayload = json.dumps(self.post_body)
        #response = requests.post("http://127.0.0.1:5000/payload", data=jsonPayload, headers={'content-type': 'application/json'})
        
        self.custom_timers['Latency'] = latency
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
