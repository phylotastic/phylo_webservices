import requests
import time


class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        self.query_param = {'text': "Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries."}

    def run(self):
        start_timer = time.time()
        response = requests.get('http://phylo.cs.nmsu.edu:5004/phylotastic_ws/fn/names_text', params=self.query_param)
        latency = time.time() - start_timer

        self.custom_timers['Latency'] = latency
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    #print trans.custom_timers
