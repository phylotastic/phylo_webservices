# ts/ncbi/genome_species


# Get species (in a taxon) that have a genome sequence in NCBI.
# Parameter: taxon - a single taxon name.

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(80, "Taxon_genome_species", 'ts/ncbi/genome_species')

class TestTsNcbiGenomeSpecies(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameter(self):
        """Test no parameters"""

        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        mess = x.json().get(u'message')
        self.assertEqual(x.status_code, 400, mess)
        self.assertTrue(u'taxon' in mess,
                        'no "taxon" in "%s"' % mess)


    def test_edge_case(self):
        """Test parameter name 'taxon' is supplied, but there is no value.
        """

        request = service.get_request('GET', {u'taxon': u''})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(x.status_code < 500)


    def test_bad_parameter_name(self):
        """Test an unknown parameter name
        """

        request = service.get_request('GET', {u'rubbish': 25})
        x = self.start_request_tests(request)
        mess = x.json().get(u'message')
        self.assertEqual(x.status_code, 400, mess)
        self.assertTrue(u'parameter' in mess,
                        'no "parameter" in "%s"' % mess)

    def test_bad_taxon(self):
        """Test bad taxon
        """

        request = service.get_request('GET', {u'taxon': u'Unknownia'})
        x = self.start_request_tests(request)
        mess = x.json().get(u'message')
        #self.assertEqual(x.status_code, 400, mess)
        self.assertTrue(x.status_code >= 200)
        self.assertTrue('No match found" in "%s"' % mess)

        # 'No match found for term Unknownia'
        #self.assertTrue(u'taxon' in mess,  'no "taxon" in "%s"' % mess)

    
    def test_example_1(self):
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        n = len(x.json()[u'species'])
        self.assertTrue(n >= 35, str(n))
        self.assertTrue(u'Ellobius talpinus' in x.json()[u'species'])
        self.assertTrue(u'Microtus agrestis' in x.json()[u'species'])
        self.assertTrue(u'Mus musculus' in x.json()[u'species'])


    
    def test_example_2(self):
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        n = len(x.json()[u'species'])
        self.assertTrue(n >= 2, str(n))
        self.assertTrue('Patagioenas fasciata' in x.json()[u'species'])
        self.assertTrue('Columba livia' in x.json()[u'species'])

    
    
null=None; false=False; true=True

example_2 = service.get_request('GET', {u'taxon': u'Columbidae'})
example_1 = service.get_request('GET', {u'taxon': u'Rodentia'})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================Taxon_genome_species=========================' 
    webapp.main()
