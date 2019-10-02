# ms/get_studies
# Get supported studies of an induced tree from OpenTreeOfLife.

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(80, "OToL_supported_studies", 'md/get_studies')

class MdStudiesTester(webapp.WebappTestCase):

    def test_no_parameter(self):
        """Test no parameters"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, {}).exchange()
        mess = x.json().get(u'message')
        self.assert_response_status(x, 400)
        self.assertTrue('Missing parameter "list" in "%s"' % x.json()[u'message'])
        

    def test_bad_parameter(self):
        """Test wrong parameter name"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, {'bad_param': "532117|42322"}).exchange()

        self.assert_response_status(x, 400)
        # Check for informativeness
        mess = x.json()[u'message']
        self.assertTrue(u'parameter' in mess,
                        'no "parameter" in "%s"' % mess)

  
    def test_invalid_parameter_value(self):
        """Test invalid parameter value
        """

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        print m
        request = self.__class__.studies_request(m, {'list': [532117,42322,42324,563151,42314], 'list_type': 'invalidtype'})
        x = request.exchange()

        mess = x.json().get(u'message')
        self.assertEqual(x.status_code, 400, mess)
        #self.assertTrue(u'valid value' in mess, '"list_type" parameter in "%s"' % mess)
        self.assertTrue(u'parameter' in mess,
                        'no "parameter" in "%s"' % mess)



class TestMdGetStudies(MdStudiesTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'GET'
    
    
    @classmethod
    def studies_request(cls, m, params):
        if m == 'POST':
           return service.get_request('POST', {'list': params['list'], 'list_type': params['list_type']})
        else:
           return service.get_request('GET', {'list': '|'.join(str(lstid) for lstid in params['list']), 'list_type': params['list_type']})


    def test_example_1(self):
        x = self.start_request_tests(example_1)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        # Check whether the number of studies in the result is more than the minimum expected
        self.assertTrue(len(x.json()[u'studies']) >= 1)
        # Check whether result is what it should be according to docs
        self.assertTrue(u'http://dx.doi.org/10.1126/science.1122277' in x.json()[u'studies'][1]['PublicationDOI'])
                          

    #@unittest.skip("temporarily to fix later")
    def test_example_2(self):
        x = self.start_request_tests(example_2)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        # Check whether the number of studies in the result is more than the minimum expected
        self.assertTrue(len(x.json()[u'studies']) >= 2)
        # Check whether result is what it should be according to docs
        self.assertTrue(u'http://dx.doi.org/10.1642/auk-14-110.1' in x.json()[u'studies'][0]['PublicationDOI'])



null=None; false=False; true=True

example_1 = service.get_request('GET', {u'list': u'532117|42322|42324|563151|42314', u'list_type': u'ottids'})
example_2 = service.get_request('GET', {u'list': u'Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens', u'list_type': u'taxa'})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================OToL_supported_studies(GET)=========================' 
    webapp.main()
