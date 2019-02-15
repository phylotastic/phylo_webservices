# 10 continued. sl/eol/links - POST
# STUB

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_sl_eol_get_links import SlEolGetLinksTester

service = webapp.get_service(80, "Info_url_species", 'sl/eol/links')

class TestSlEolLinks(SlEolGetLinksTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'POST'

    @classmethod
    def bad_sl_request(cls, names):
        return service.get_request('POST', {'bad_parameter': names})

    @classmethod
    def sl_request(cls, names):
        return service.get_request('POST', {'species': names})


    def test_example_2(self):
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        self.assertEqual(x.json()[u'species'][0][u'matched_name'], u'Melanerpes erythrocephalus')
        self.assertEqual(x.json()[u'species'][0][u'species_info_link'], u'https://eol.org/pages/45509726') 

        self.assertEqual(x.json()[u'species'][1][u'species_info_link'], u'https://eol.org/pages/45509736')
        self.assertEqual(x.json()[u'species'][1][u'matched_name'], u'Melanerpes uropygialis')


null=None; false=False; true=True

example_2 = service.get_request('POST', {u'species': ["Melanerpes erythrocephalus","Melanerpes uropygialis"]})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================Info_url_species(POST)========================='
    webapp.main()
