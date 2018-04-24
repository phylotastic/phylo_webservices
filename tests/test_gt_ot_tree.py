# gt/ot/tree
# Like gt/ot/get_tree, but using POST instead of GET

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_gt_ot_get_tree import GtTreeTester

service = webapp.get_service(5004, "OToL_wrapper_Tree", 'gt/ot/tree')

class TestGtOtTree(GtTreeTester):
    @classmethod
    def http_method(cls):
        return 'POST'

    @classmethod
    def get_service(cls):
        return service

    @classmethod
    def tree_request(cls, names):
        return service.get_request('POST', {'taxa': names})
    

    def test_example_1(self):
        x = self.start_request_tests(example_1)
        if x.status_code != 200:
            json.dump(x.to_dict(), sys.stdout, indent=2)
        self.assert_success(x)
        self.assertTrue(u'newick' in x.json())
        self.assertTrue(u'ott285198' in x.json()[u'newick'])
        self.assertTrue(u'tree_metadata' in x.json())
        m = x.json()[u'tree_metadata']
        self.assertTrue(u'supporting_studies' in m)
        self.assertTrue(len(m[u'supporting_studies']) > 1)

   
    
null=None; false=False; true=True


example_1 = service.get_request('POST', {"taxa": ["Setophaga striata","Setophaga magnolia","Setophaga angelae","Setophaga plumbea","Setophaga virens"]})


if __name__ == '__main__':
    print >>sys.stdout, '\n=================OToL_wrapper_Tree(POST)========================='
    webapp.main()
