# gt/pm/get_tree

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp


service = webapp.get_service(5004, "Phylomatic_wrapper_Tree", 'gt/pm/get_tree')

class TestGtPmTreeTester(webapp.WebappTestCase):

    def test_no_parameter(self):
        """Test no parameters.
        """

        request = service.get_request(self.__class__.http_method(), {})
        x = self.start_request_tests(request)
        self.assert_response_status(x, 400)

        # Test for informativeness
        self.assertTrue('Missing parameter "taxa" in "%s"' % x.json()[u'message'])
       

    def test_no_taxa(self):
        """Test edge case: parameter name 'taxa' is supplied, but there is no value.
        """

        request = service.get_request(self.__class__.http_method(), {'taxa': ''})
        x = self.start_request_tests(request)
        self.assertTrue(x.status_code >= 400)
        # Error: 'taxa' parameter must have a valid value
        self.assertTrue(u'taxa' in x.json()[u'message'], 'no "taxa" in "%s"' % x.json()[u'message'])


    def test_misspelled_parameter(self):
        """Test edge case: parameter name 'taxa' is misspelled.
        """

        request = service.get_request(self.__class__.http_method(), {'tax': "Setophaga striata|Setophaga magnolia|Setophaga angelae|Setophaga plumbea|Setophaga virens"})
        x = self.start_request_tests(request)
        self.assert_response_status(x, 400)
        self.assertTrue('Missing parameter "taxa" in "%s"' % x.json()[u'message'])



    def test_example_1(self):
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        self.assertTrue(u'newick' in x.json())
        self.assertTrue(u'Helianthus_annuus' in x.json()[u'newick'])

    def test_example_2(self):
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        self.assertTrue(u'newick' in x.json())
        self.assertTrue(u'Panthera_tigris' in x.json()[u'newick'])


class TestGtPmGetTree(TestGtPmTreeTester):

    @classmethod
    def get_service(cls):
        """Class method so that the superclass can tell which service we're testing."""

        return service

    @classmethod
    def http_method(cls):
        """Class method so that the superclass can tell which HTTP method should be used."""

        return 'GET'

    
null=None; false=False; true=True

example_1 = service.get_request('GET', {u'taxa': u'Helianthus annuus|Passiflora edulis|Rosa arkansana|Saccharomyces cerevisiae'})
example_2 = service.get_request('GET', {u'taxa': u'Panthera leo|Panthera onca|Panthera tigris|Panthera uncia'})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================Phylomatic_wrapper_Tree(GET)========================='  
    webapp.main()
