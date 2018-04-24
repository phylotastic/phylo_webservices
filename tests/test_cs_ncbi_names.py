# cs/ncbi/scientific_names - POST
# STUB

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_cs_ncbi_get_names import TestCsGetNCBI

service = webapp.get_service(5013, "NCBI_common_name", 'cs/ncbi/scientific_names')

class TestCsNCBINames(TestCsGetNCBI):
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
        self.assertEqual(x.json()[u'result'][0][u'matched_names'][0]['scientific_name'], 'Bos taurus')
        self.assertEqual(x.json()[u'result'][1][u'matched_names'][0]['scientific_name'], 'Felis catus')
        self.assertEqual(x.json()[u'result'][2][u'matched_names'][0]['scientific_name'], 'Capra hircus')
        self.assertEqual(x.json()[u'result'][3][u'matched_names'][0]['scientific_name'], 'Sus scrofa')


null=None; false=False; true=True

example_2 = service.get_request('POST', {u'commonnames': ["cattle", "cat", "goat", "pig", "sheep", "duck", "chicken", "horse"]})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================NCBI_common_name(POST)========================='
    webapp.main()
