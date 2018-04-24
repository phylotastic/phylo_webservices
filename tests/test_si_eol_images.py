# si/eol/images


import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_si_eol_get_images import TestSiEolGetImages

service = webapp.get_service(5004, "Image_url_species", 'si/eol/images')

class TestSiEolImages(TestSiEolGetImages):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'POST'

    
    def test_example_2(self):
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        # There should be at least one image per species
        self.assertTrue(len(all_images(x)) >= len(example_2.parameters[u'species']))


def all_images(x):
    return [image for source in x.json()[u'species'] for image in source[u'images']]


example_2 = service.get_request('POST', {u'species': [u'Catopuma badia', u'Catopuma temminckii']})


if __name__ == '__main__':
    print >>sys.stdout, '\n=================Image_url_species(POST)========================='  
    webapp.main()
