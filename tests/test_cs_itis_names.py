# cs/itis/scientific_names - POST
# STUB

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_cs_itis_get_names import TestCsGetITIS

service = webapp.get_service(5013, "ITIS_common_name", 'cs/itis/scientific_names')

class TestCsITISNames(TestCsGetITIS):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'POST'

    @classmethod
    def com_name_request(cls, cnlist):
        return service.get_request('POST', {'commonnames': cnlist})
        
    
    def test_example_2(self):
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        # Check whether result is what it should be according to docs
        self.assertEqual(x.json()[u'result'][0][u'matched_names'][0]['scientific_name'], 'Cornus florida')
        self.assertEqual(x.json()[u'result'][1][u'matched_names'][0]['scientific_name'], 'Quercus alba')
        self.assertEqual(x.json()[u'result'][2][u'matched_names'][0]['scientific_name'], 'Pseudotsuga menziesii')
        self.assertEqual(x.json()[u'result'][3][u'matched_names'][0]['scientific_name'], 'Conocarpus erectus')


null=None; false=False; true=True

example_2 = service.get_request('POST', {u'commonnames': ["Flowering dogwood", "White oak", "Oregon pine", "Button mangrove"]})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================ITIS_common_name(POST)========================='
    webapp.main()
