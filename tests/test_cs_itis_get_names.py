# cs/ncbi/get_scientific_names
# ITIS: get scientific names of a list of species from its common names

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5013, "ITIS_common_name", 'cs/itis/get_scientific_names')

class ITISCommonNameTester(webapp.WebappTestCase):

    def test_no_parameter(self):
        """Test no parameters"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, {}).exchange()
        mess = x.json().get(u'message')
        self.assert_response_status(x, 400)
        self.assertTrue('Missing parameter "commonnames" in "%s"' % x.json()[u'message'])
        

    def test_bad_parameter(self):
        """Test wrong parameter name"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, {'common_name': "fish|dog"}).exchange()

        self.assert_response_status(x, 400)
        # Check for informativeness
        mess = x.json()[u'message']
        self.assertTrue(u'parameter' in mess,
                        'no "parameter" in "%s"' % mess)

  
    def test_bad_common_name(self):
        """Test nonexistant common name"""

        service = self.__class__.get_service()
        request = self.__class__.com_name_request(['Nosuchtaxon', 'nonexistant'])
        x = request.exchange()
        #x = service.get_request(m, {u'species': u'Nosuchtaxonia notatall'}).exchange()
        # json.dump(x.to_dict(), sys.stdout, indent=2)
        self.assert_success(x)
        self.assertEqual(x.json()[u'result'][0][u'matched_names'], [])
        self.assertEqual(x.json()[u'result'][1][u'matched_names'], [])



class TestCsGetITIS(ITISCommonNameTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'GET'
    
    
    @classmethod
    def com_name_request(cls, cnlist):
        return service.get_request('GET', {'commonnames': '|'.join(cnlist)})


    def test_example_1(self):
        x = self.start_request_tests(example_1)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        # Check whether the number of names in the result is more than the minimum expected
        #self.assertTrue(len(x.json()[u'result'][0][u'matched_names']) >= 1)
        # Check whether result is what it should be according to docs
        #self.assertEqual(x.json()[u'result'][0][u'matched_names'][0]['scientific_name'], 'Ursus arctos arctos')

        self.assertTrue(len(x.json()[u'result'][1][u'matched_names']) >= 1)
        # Check whether result is what it should be according to docs
        if x.json()[u'result'][1][u'matched_names'][0]['common_name'] == "Gray Wolf":
        	self.assertEqual(x.json()[u'result'][1][u'matched_names'][0]['scientific_name'], 'Canis lupus')

    

null=None; false=False; true=True

example_1 = service.get_request('GET', {u'commonnames': 'Brown bear|Gray wolf'})


if __name__ == '__main__':
    print >>sys.stdout, '\n=================ITIS_common_name(GET)=========================' 
    webapp.main()
