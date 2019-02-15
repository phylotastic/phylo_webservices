# gt/pt/tree

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_gt_pt_get_tree import TestGtPtTreeTester


service = webapp.get_service(80, "PhyloT_wrapper_Tree", 'gt/pt/tree')

class TestGtPtPostTree(TestGtPtTreeTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(cls):
        return 'POST'

    @unittest.skip("temporarily to fix later")
    def test_example_2(self):
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        self.assertTrue(u'newick' in x.json())
        self.assertTrue(u'Aix_sponsa' in x.json()[u'newick'])
        self.assertTrue(u'Anas_acuta' in x.json()[u'newick'])
        self.assertTrue(u'Dendrocygna_bicolor' in x.json()[u'newick'])


null=None; false=False; true=True


example_2 = service.get_request('POST', {u'taxa': [u"Aix sponsa", u"Anas acuta", u"Anas americana", u"Aythya americana", u"Branta canadensis", u"Bucephala albeola", u"Dendrocygna autumnalis", u"Dendrocygna bicolor"]})


if __name__ == '__main__':
    print >>sys.stdout, '\n=================PhyloT_wrapper_Tree(POST)=========================' 
    webapp.main()
