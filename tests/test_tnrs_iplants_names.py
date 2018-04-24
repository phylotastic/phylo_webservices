#tnrs/ip/names (POST version of service)

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_tnrs_iplants_resolve import TestTnrsIpResolve


service = webapp.get_service(5004, "iPlant_TNRS_wrapper", 'tnrs/ip/names')

class TestTnrsIpNames(TestTnrsIpResolve):
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
        name = u'Acidoton lanceolatus'
        matched_names = self.all_matched_names(x)
        self.assertTrue(name in matched_names)


null=None; false=False; true=True

example_1 = service.get_request('POST', {u'scientificNames': [u'Acianthera angusti', u'Acidoton lanceolatus'], "fuzzy_match": True, "multiple_match": False})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================iplant_TNRS_wrapper(POST)========================='
    webapp.main()
