#tnrs/gnr/resolve (POST version of service)

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_tnrs_ot_resolve import TnrsTester


service = webapp.get_service(5004, "GNR_TNRS_wrapper", 'tnrs/gnr/names')

class TestTnrsGnrNames(TnrsTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(cls):
        return 'POST'

    @classmethod
    def namelist(cls, x):
        return x.json()[u'scientificNames']

    @classmethod
    def tnrs_request(cls, names):
        return service.get_request('POST', {'scientificNames': names})

    
    def test_example_1(self):
        """Test example from the documentation."""
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        name = u'Rana temporaria'
        matched_names = self.all_matched_names(x)
        self.assertTrue(name in matched_names)


null=None; false=False; true=True

example_1 = service.get_request('POST', {u'scientificNames': [u'Rana Temporaria'], "fuzzy_match": True, "multiple_match": False})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================GNR_TNRS_wrapper(POST)========================='
    webapp.main()
