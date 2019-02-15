# sc/scale

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(80, "Datelife_scale_tree", 'sc/scale')

class TestScScale(webapp.WebappTestCase):
    @classmethod
    def get_service(self):
        return service

    
    def test_no_parameters(self):
        x = self.start_request_tests(service.get_request('POST', {}))
        self.assert_response_status(x, 400)
        mess = x.json().get(u'message')
        self.assertTrue('newick' in mess, mess)


    def test_wrong_parameter(self):
        """Test wrong parameter name"""

        x = self.start_request_tests(service.get_request('POST', {u'bad_parameter': '((a,b)c)'}))
        self.assert_response_status(x, 400)
        # Check for informativeness
        mess = x.json()[u'message']
        self.assertTrue(u'parameter' in mess,
                        'no "parameter" in "%s"' % mess)    


    @unittest.skip("temporarily to fix later")
    def test_bogus_newick(self):
        x = self.start_request_tests(service.get_request('POST', {u'newick': '(a,b)c);'}))
        # Issue: 500 Error: Failed to scale from datelife R package
        self.assert_response_status(x, 400)
        # json.dump(x.json(), sys.stdout, indent=2)
        mess = x.json().get(u'message')
        # Not clear what the message ought to say; be prepared to change the 
        # following check to match the message that eventually gets chosen.
        self.assertTrue('yntax' in mess, mess)

    
    def test_example_1(self):
        x = self.start_request_tests(example_1)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        self.assertTrue(u'median' in x.json()['method_used'])
        self.assertTrue(u'Macaca mulatta' in x.json()[u'scaled_tree'])


    def test_example_2(self):
        x = self.start_request_tests(example_2)
        mess = x.json().get(u'message')
        self.assert_success(x, mess)
        #self.assertTrue(u'median' in x.json()['method_used'])
        self.assertTrue(u'Solanum lycopersicum' in x.json()[u'scaled_tree'])
        self.assertTrue(u'Arabidopsis thaliana' in x.json()[u'scaled_tree'])



null=None; false=False; true=True

example_1 = service.get_request('POST', {u'newick': u'(((((Canis lupus pallipes,Melursus ursinus)Caniformia,((Panthera tigris,Panthera pardus)Panthera,Herpestes fuscus))Carnivora,(Macaca mulatta,Homo sapiens)Catarrhini)Boreoeutheria,Elephas maximus)Eutheria,Haliastur indus)Amniota;'})
example_2 = service.get_request('POST', {u'method': u'sdm', u'newick': u'((Zea mays,Oryza sativa),((Arabidopsis thaliana,(Glycine max,Medicago sativa)),Solanum lycopersicum)Pentapetalae);'})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================Datelife_scale_tree========================='  
    webapp.main()
