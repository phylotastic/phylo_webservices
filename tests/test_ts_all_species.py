# ts/all_species
# Get all species that belong to a particular Taxon.

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(80, "Taxon_all_species", 'ts/ot/all_species')

class TestTsAllSpecies(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameter(self):
        """Test a call with No parameters.
        """

        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(u'taxon' in x.json()[u'message'],    
                        'no "taxon" in "%s"' % x.json()[u'message'])  

    def test_bad_name(self):
        """Test a call with a Bad name.
        """

        request = service.get_request('GET', {u'taxon': u'Nosuchtaxonia'})
        x = self.start_request_tests(request)
        m = x.json().get(u'message')
        self.assertTrue(x.status_code >= 200)
        self.assertTrue('No Taxon matched" in "%s"' % m)


    def test_edge_case(self):
        """Test edge case: parameter name 'taxon' is supplied, but there is no value.
        """

        request = service.get_request('GET', {u'taxon': u''})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(x.status_code < 500)


    def taxon_tester(self, name):
        request = service.get_request('GET', {u'taxon': name})
        x = self.start_request_tests(request)
        self.assert_success(x, name)
        print '%s: %s %s' % (name, len(x.json()[u'species']), x.time)

    # Found this taxon lineage sequence using the 'lineage' script in 
    # opentreeoflife/reference-taxonomy/bin
    @unittest.skip("temporarily skipped")
    def test_nested_sequence(self):
        """Try progressively larger taxa to see when the service breaks."""

        self.taxon_tester('Apis mellifera')
        self.taxon_tester('Apis')
        self.taxon_tester('Apini')
        self.taxon_tester('Apinae')
        # Apidae at 5680 species is a struggle
        self.taxon_tester('Apidae')
        if False:
            # Apoidea: 19566 takes 223 seconds
            self.taxon_tester('Apoidea')
            # Aculeata fails after 339 seconds
            self.taxon_tester('Aculeata')
            self.taxon_tester('Apocrita')
            self.taxon_tester('Hymenoptera')
            self.taxon_tester('Endopterygota')
            self.taxon_tester('Neoptera')
            self.taxon_tester('Pterygota')
            self.taxon_tester('Dicondylia')
            self.taxon_tester('Insecta')
            self.taxon_tester('Hexapoda')
            self.taxon_tester('Pancrustacea')
            self.taxon_tester('Mandibulata')
            self.taxon_tester('Arthropoda')
            self.taxon_tester('Panarthropoda')
            self.taxon_tester('Ecdysozoa')
            self.taxon_tester('Protostomia')
            self.taxon_tester('Bilateria')
            self.taxon_tester('Eumetazoa')
            self.taxon_tester('Metazoa')
            self.taxon_tester('Holozoa')
            self.taxon_tester('Opisthokonta')
            self.taxon_tester('Eukaryota')

    @unittest.skip("takes too long")
    def test_big_family(self):
        """Test the service on big families.
        So try it on a big family (>60,000 species) to what happens.
        As of 2017-11-05, this fails after crunching for 22 minutes - 
        returns with a non-200 status code."""

        self.taxon_tester('Staphylinidae')

    
    def test_example_1(self):
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'species']) > 10)
        self.assertTrue(u'Vulpes pallida' in x.json()[u'species'])
        self.assertTrue(u'Vulpes bengalensis' in x.json()[u'species'])
        self.assertTrue(u'Vulpes rueppellii' in x.json()[u'species'])


    def test_example_2(self):
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'species']) > 100)
        self.assertTrue(u'Rhizocyon oregonensis' in x.json()[u'species'])
        self.assertTrue(u'Paraenhydrocyon robustus' in x.json()[u'species'])
        self.assertTrue(u'Carpocyon compressus' in x.json()[u'species'])


null=None; false=False; true=True

example_1 = service.get_request('GET', {u'taxon': u'Vulpes'})
example_2 = service.get_request('GET', {u'taxon': u'Canidae'})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================Taxon_all_species=========================' 
    webapp.main()
