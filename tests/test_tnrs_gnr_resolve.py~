#tnrs/gnr/resolve

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_tnrs_ot_resolve import TnrsTester

service = webapp.get_service(5004, "GNR_TNRS_wrapper", 'tnrs/gnr/resolve')

class TestTnrsGnrResolve(TnrsTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(cls):
        return 'GET'

    @classmethod
    def namelist(cls, x):
        return x.json()[u'names'].split('|')

    @classmethod
    def tnrs_request(cls, names):
        return service.get_request('GET', {'names': u'|'.join(names)})

    
    def test_example_1(self):
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        name = u'Setophaga striata'
        matched_names = self.all_matched_names(x)
        self.assertTrue(name in matched_names)


    def test_example_2(self):
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        expected_names = [u'Formica exsectoides', u'Formica polyctena']
        matched_names = self.all_matched_names(x)
        for name in expected_names:
            self.assertTrue(name in matched_names)

null=None; false=False; true=True

example_1 = service.get_request('GET', {u'names': u'Setophaga striata|Setophaga megnolia|Setophaga angilae|Setophaga plumbea|Setophaga virens'})
example_2 = service.get_request('GET', {u'names': u'Formica polyctena|Formica exsectoides|Formica pecefica'})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================GNR_TNRS_wrapper(GET)========================='
    webapp.main()

