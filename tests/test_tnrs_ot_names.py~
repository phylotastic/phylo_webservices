# 3 (continued). tnrs/ot/names

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_tnrs_ot_resolve import TnrsTester

service = webapp.get_service(5004, "OToL_TNRS_wrapper", 'tnrs/ot/names')

class TestTnrsOtNames(TnrsTester):
    @classmethod
    def get_service(cls):
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

    def test_2(self):
        """Test parameter name 'scientificNames' is supplied, but there is no value."""

        request = self.__class__.tnrs_request([])
        x = request.exchange()
        #print x.json()
        self.assert_response_status(x, 400)
        self.assertTrue('"scientificNames" parameter must have a valid value in "%s"' % x.json()[u'message'])

    
    def test_example_1(self):
        """Test example from the documentation."""
        x = self.start_request_tests(example_1)

        self.assert_success(x)
        expected_names = [u'Formica exsectoides', u'Formica polyctena']
        matched_names = self.all_matched_names(x)
        for name in expected_names:
            self.assertTrue(name in matched_names)


null=None; false=False; true=True

example_1 = service.get_request('POST', {u'scientificNames': [u'Formica exsectoides', u'Formica pecefica', u'Formica polyctena']})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================OToL_TNRS_wrapper(POST)========================='
    webapp.main()
