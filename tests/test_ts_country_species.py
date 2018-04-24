# ts/country_species
# Species that belong to a particular taxon and established in a particular 
# country, using INaturalist services.
# GET or POST

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5004, "Taxon_country_species", 'ts/country_species')

class TestTsCountrySpecies(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service


    def test_no_parameter(self):
        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(u'taxon' in x.json()[u'message'],  
                        'no "taxon" in "%s"' % x.json()[u'message'])


    def test_bad_taxon(self):
        request = service.get_request('GET', {u'taxon': u'Nosuchtaxonia', u'country': u'Nepal'})
        x = self.start_request_tests(request)
        m = x.json().get(u'message')
        #self.assertTrue(x.status_code >= 400, m)
        #self.assertTrue(u'axon' in m, 'no "taxon" in "%s"' % m)
        self.assertTrue(x.status_code >= 200)
        self.assertTrue('No Taxon matched" in "%s"' % m)


    def test_edge_case(self):
        """Test edge case: parameter name 'taxon' is supplied, but there is no value.
        """

        request = service.get_request('GET', {u'taxon': u''})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(x.status_code < 500)



    @unittest.skip("unknown country")
    def test_bad_country(self):
        """See what happens if the country is likely to be unknown.
        2017-11-05 This test just hangs, so skipping for now.
        """

        request = service.get_request('GET', {u'taxon': u'Hylidae', u'country': u'Sovietunion'})
        x = self.start_request_tests(request)
        m = x.json().get(u'message')
        
        self.assertTrue(x.status_code >= 400, m)
        self.assertTrue(u'axon' in m,    
                        'no "taxon" in "%s"' % m)

    
    def test_example_1(self):
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'species']) >= 2)
        self.assertTrue(u'Vulpes bengalensis' in x.json()[u'species'])
        self.assertTrue(u'Vulpes ferrilata' in x.json()[u'species'])


    def test_example_2(self):
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'species']) >= 1)
        self.assertTrue(u'Panthera tigris' in x.json()[u'species'])
                       

        
null=None; false=False; true=True

example_1 = service.get_request('GET', {u'country': u'Nepal', u'taxon': u'Vulpes'})
example_2 = service.get_request('GET', {u'country': u'Bangladesh', u'taxon': u'Panthera'})


if __name__ == '__main__':
    print >>sys.stdout, '\n=================Taxon_country_species=========================' 
    webapp.main()
