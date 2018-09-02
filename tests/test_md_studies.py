# ms/studies

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_md_get_studies import TestMdGetStudies

service = webapp.get_service(5006, "OToL_supported_studies", 'md/studies')

class TestMdStudies(TestMdGetStudies):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'POST'

    
    def test_example_1(self):
        x = self.start_request_tests(example_1)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        # Check whether the number of studies in the result is more than the minimum expected
        self.assertTrue(len(x.json()[u'studies']) >= 1)
        # Check whether result is what it should be according to docs
        self.assertTrue(u'http://dx.doi.org/10.1016/j.ympev.2009.08.018' in x.json()[u'studies'][0]['PublicationDOI'])

        
    #@unittest.skip("temporarily to fix later")
    def test_example_2(self):
        x = self.start_request_tests(example_2)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        
        # Check whether the number of studies in the result is more than the minimum expected
        self.assertTrue(len(x.json()[u'studies']) >= 1)
        # Check whether result is what it should be according to docs
        self.assertTrue(u'http://dx.doi.org/10.1016/j.ympev.2009.08.018' in x.json()[u'studies'][0]['PublicationDOI'])


null=None; false=False; true=True

example_1 = service.get_request('POST', {u'list': [1094064, 860906, 257323, 698438, 698406, 187220, 336231, 124230], u'list_type': u'ottids'})

example_2 = service.get_request('POST', {u'list': [u'Delphinidae', u'Delphinus capensis', u'Delphinus delphis', u'Tursiops truncatus', u'Tursiops aduncus', u'Sotalia fluviatilis', u'Sousa chinensis'], u'list_type': u'taxa'})


if __name__ == '__main__':
    print >>sys.stdout, '\n=================OToL_supported_studies(POST)=========================' 
    webapp.main()
