# 2. fn/names_text

# Parameters: text (required), engine (optional)

import sys, os, unittest, json, codecs
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5004, "GNRD_wrapper_text", 'fn/names_text')

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
        N.b. the input is copied to the output (u'input_text' result field).  
        That seems like a bad idea.
        """

        request = service.get_request('GET', {u'text': get_sample()[0:30000]})
        x = self.start_request_tests(request)
        self.assert_success(x)
        # Check whether the number of names in the result is more than the minimum expected
        self.assertTrue(len(x.json()[u'scientificNames']) > 10)
        # Check whether result is what it should be according to docs
        self.assertTrue(u'Papilio' in x.json()[u'scientificNames'])
    

    
    def test_engines(self):
        """Test engine parameter with valid(e.g. 1,2) and invalid(e.g. 5,6) values.
        """

        for engine in range(0, 6):
            request = service.get_request('GET', {u'engine': engine, u'text': "Whales are a widely distributed and diverse group of fully aquatic placental marine mammals. They are an informal grouping within the infraorder Cetacea, usually excluding dolphins and porpoises. Whales, dolphins and porpoises belong to the order Cetartiodactyla with even-toed ungulates and their closest living relatives are the hippopotamuses, having diverged about 40 million years ago. The two parvorders of whales, baleen whales (Mysticeti) and toothed whales (Odontoceti), are thought to have split apart around 34 million years ago. The whales comprise eight extant families: Balaenopteridae (the rorquals), Balaenidae (right whales), Cetotheriidae (the pygmy right whale), Eschrichtiidae (the grey whale), Monodontidae (belugas and narwhals), Physeteridae (the sperm whale), Kogiidae (the dwarf and pygmy sperm whale), and Ziphiidae (the beaked whales)."})
            x = self.start_request_tests(request)
            if engine >= 0 and engine <= 2:
               self.assert_success(x)
               self.assertTrue(len(x.json()[u'scientificNames']) >= 5)
               self.assertTrue(u'Balaenidae' in x.json()[u'scientificNames'])
            else:
               self.assertTrue(x.status_code >= 400)

   
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
        # Check whether the number of names in the result is more than the minimum expected
        self.assertTrue(len(x.json()[u'scientificNames']) >= 5)
        # Check whether result is what it should be according to docs
        self.assertTrue(u'Formica polyctena' in x.json()[u'scientificNames'])


null=None; false=False; true=True

example_2 = service.get_request('GET', {u'text': u'Formica polyctena is a species of European red wood ant in the genus Formica. The pavement ant, Tetramorium caespitum is an ant native to Europe. Pseudomyrmex is a genus of stinging, wasp-like ants. Adetomyrma venatrix is an endangered species of ants endemic to Madagascar. Carebara diversa is a species of ants in the subfamily Formicinae. It is found in many Asian countries.'})
example_1 = service.get_request('GET', {u'engine': u'2', u'text': u'The lemon dove (Columba larvata) is a species of bird in the pigeon family Columbidae found in montane forests of sub-Saharan Africa.'})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================GNRD_wrapper_text=========================' 
    webapp.main()
