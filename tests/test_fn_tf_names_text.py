# 4. fn/tf/names_text

# Parameters: text (required)

import sys, os, unittest, json, codecs
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5004, "TaxonFinder_wrapper_text", 'fn/tf/names_text')

the_sample = None

def get_sample():
    global the_sample
    if the_sample == None:
        with codecs.open(webapp.find_resource('text-sample.txt'), 'r', 'latin-1') as infile: 
            the_sample = infile.read()
    return the_sample

class TestFnNamesText(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    def test_no_parameter(self):
        """Try a call with No parameters."""

        request = service.get_request('GET', {})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue('Missing parameter "text" in "%s"' % x.json()[u'message'])


    def test_edge_case(self):
        """Test edge case: parameter name 'text' is supplied, but there is no value.
        """

        request = service.get_request('GET', {u'text': u''})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        self.assertTrue(x.status_code < 500)

    
    @unittest.skip("temporarily to save time")
    def test_large_input(self):
        """Test large input.
        40000 characters fails; 30000 succeeds.
        """

        request = service.get_request('GET', {u'text': get_sample()[0:30000]})
        x = self.start_request_tests(request)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'scientificNames']) > 10)
        self.assertTrue(u'Papilio' in x.json()[u'scientificNames'])
    
    def test_example_1(self):
        """Test example_1 from the documentation."""

        x = self.start_request_tests(example_1)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'scientificNames']) >= 2)
        self.assertTrue(u'Columbidae' in x.json()[u'scientificNames'])


    def test_example_2(self):
        """Test example_2 from the documentation."""
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        self.assertTrue(len(x.json()[u'scientificNames']) >= 5)
        self.assertTrue(u'Formica polyctena' in x.json()[u'scientificNames'])


null=None; false=False; true=True

example_2 = service.get_request('GET', {u'text': u'Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries.'})
example_1 = service.get_request('GET', {u'engine': u'2', u'text': u'The lemon dove (Columba larvata) is a species of bird in the pigeon family Columbidae found in montane forests of sub-Saharan Africa.'})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================TaxonFinder_wrapper_text=========================' 
    webapp.main()
