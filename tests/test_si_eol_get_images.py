# si/eol/get_images

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(80, "Image_url_species", 'si/eol/get_images')

class SiEolImagesTester(webapp.WebappTestCase):

    @unittest.skip("temporarily to fix later")
    def test_bad_method(self):
        """Test invalid HTTP method
        """
        request = service.get_request('POST', {})
        x = self.start_request_tests(request)
        self.assertEqual(x.status_code, 405)
        

    def test_no_parameter(self):
        """Test no parameters"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, {}).exchange()
        mess = x.json().get(u'message')
        self.assert_response_status(x, 400)
        self.assertTrue('Missing parameter "species" in "%s"' % mess)


    def test_bad_parameter(self):
        """Test wrong parameter name"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        request = self.__class__.bad_si_request(m, ['Panthera leo'])
        x = request.exchange()
        self.assert_response_status(x, 400)
        # Check for informativeness
        mess = x.json()[u'message']
        self.assertTrue(u'parameter' in mess, 'no "parameter" in "%s"' % mess)

    '''
    def test_bad_value_type(self):
        """Test the value of parameter as a single species name instead of a list
        """

        request = service.get_request('GET', {u'species': u'Nosuchtaxonia mistakea'})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code % 100 == 4, x.status_code)
        m = x.json().get(u'message')
        self.assertTrue(u'species' in m,    #informative?
                        'no "species" in "%s"' % m)
    '''

    def test_bad_name(self):
        """Test bad species name"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, {'species': [u'Nosuchtaxonia mistakea']}).exchange()
        #x = request.exchange()

        m = x.json().get(u'message')
        self.assert_success(x, m)
        self.assertTrue(u'species' in x.json())
        self.assertEqual(len(all_images(x)), 0, "number of images")

    
class TestSiEolGetImages(SiEolImagesTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'GET'

    @classmethod
    def bad_si_request(cls, m, names):
        if m == 'POST':
           return service.get_request(m, {'bad_parameter': names})
        else:
           return service.get_request(m, {'bad_parameter': u'|'.join(names)})


    @classmethod
    def si_request(cls, m, names):
        if m == 'POST':
           return service.get_request(m, {'species': names})
        else:
           return service.get_request(m, {'species': u'|'.join(names)})

    '''
    def test_bad_method(self):
        """What if you do a GET when the service is expecting a POST?
        (Hoping for 405.)"""

        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        # GET method not allowed
        self.assertEqual(x.status_code, 405)
        # TBD: check for informativeness
        json.dump(x.to_dict(), sys.stdout, indent=2)
    '''

    def test_example_1(self):
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        self.assertEqual(len(all_images(x)), 15, "number of images")


def all_images(x):
    return [image for source in x.json()[u'species'] for image in source[u'images']]

example_1 = service.get_request('GET', {u'species': u'Panthera leo|Panthera onca|Panthera pardus'})



if __name__ == '__main__':
    print >>sys.stdout, '\n=================Image_url_species(GET)=========================' 
    webapp.main()
