import requests
import time
import json
from os.path import dirname, abspath

class Transaction(object):
    def __init__(self):
        self.custom_timers = {}
        
        self.post_body = {'tree1_nwk':"(((((Glycine_max_ott681762,Carica_papaya_ott429474),Vitis_vinifera_ott756728),(Solanum_tuberosum_ott494835,Lactuca_sativa_ott515700))Pentapetalae_ott5316182,Oryza_sativa_ott709894),Physcomitrella_patens_ott821359)Embryophyta_ott56610;", 'tree2_nwk':"(((((Glycine_max_ott681762,Prunus_persica_ott259054),(Theobroma_cacao_ott388185,Carica_papaya_ott429474)),Vitis_amurensis_ott805071),Solanum_lycopersicum_ott378964)Pentapetalae_ott5316182,(Musa_balbisiana_ott225973,Oryza_sativa_ott709894));"}

    
    def run(self):
        start_timer = time.time()
        jsonPayload = json.dumps(self.post_body)
        response = requests.post("http://phylo.cs.nmsu.edu:5006/phylotastic_ws/compare_trees", data=jsonPayload, headers={'content-type': 'application/json'})
        latency = time.time() - start_timer

        self.custom_timers['Latency'] = latency
        assert (response.status_code == 200), 'Bad Response: HTTP %s' % response.status_code
        

if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    #print trans.custom_timers
