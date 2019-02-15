# gt/pm/tree

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_gt_pm_get_tree import TestGtPmTreeTester

service = webapp.get_service(80, "Phylomatic_wrapper_Tree", 'gt/pm/tree')

class TestGtPmPostTree(TestGtPmTreeTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(cls):
        return 'POST'

    
    def test_example_1(self):
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        self.assertTrue(u'newick' in x.json())
        self.assertTrue(u'Rangifer_tarandus' in x.json()[u'newick'])
        self.assertTrue(u'Canis_latrans' in x.json()[u'newick'])


    def test_example_2(self):
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        self.assertTrue(u'newick' in x.json())
        self.assertTrue(u'Passiflora_edulis' in x.json()[u'newick'])



null=None; false=False; true=True

example_1 = service.get_request('POST', {u'taxa': [u'Rangifer tarandus', u'Ursus americanus', u'Canis latrans', u'Vulpes vulpes',
u'Lepus americanus']})
example_2 = service.get_request('POST', {u'taxa': [u'Helianthus annuus', u'Passiflora edulis', u'Rosa arkansana', u'Saccharomyces cerevisiae']})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================Phylomatic_wrapper_Tree(POST)=========================' 
    webapp.main()
