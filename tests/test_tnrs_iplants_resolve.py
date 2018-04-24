#tnrs/ip/resolve

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp
from test_tnrs_ot_resolve import TnrsTester

service = webapp.get_service(5004, "iPlant_TNRS_wrapper", 'tnrs/ip/resolve')

class TestTnrsIplant(webapp.WebappTestCase):

    def test_no_parameter(self):
        """Test no parameter
        Ensure that we get failure if names parameter is not supplied because names parameter is 'mandatory'.
        """

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, {}).exchange()
        
        self.assert_response_status(x, 400)

        # Test for informativeness
        self.assertTrue('Missing parameter "names" in "%s"' % x.json()[u'message'])

    
    def test_misspelled(self):
        """Test misspelled names in the input.
        There's no such thing as 'Quarcus nygra'."""

        namesx = [(u'Persea americana', True),
                  (u'Quarcus nygra', False), # Correct name: Quercus nigra
                  ]
        self.try_names(namesx)


    def try_names(self, namesx):
        """Utility for some of the tests; weak test of correct returned value"""
        m = self.http_method()
        request = self.__class__.tnrs_request([name for (name, tf) in namesx])
        x = request.exchange()
        self.assert_success(x)
        matched_names = self.all_matched_names(x)
        for (name, tf) in namesx:
            outcome = ((name in matched_names) == tf)
            if not outcome:
                print name, 'not in matched_names'
                print 'json:'
                json.dump(x.json(), sys.stdout, indent=2)
            self.assertTrue(outcome)

    def all_matched_names(self, x):
        """Utility for some of the tests; weak test of correct returned value"""

        j = x.json()
        self.assertTrue(u'resolvedNames' in j)
        matches = j[u'resolvedNames']
        names = []
        for m in matches:
            self.assertTrue(u'matched_results' in m,
                            'no matched_results key in %s' % list(m.keys()))
            for r in m[u'matched_results']:
                self.assertTrue(u'matched_name' in r,
                                'no matched_name key in %s' % list(r.keys()))
                names.append(r[u'matched_name'])
                self.assertTrue(u'synonyms' in r,
                                'no synonyms key in %s' % list(r.keys()))
                names.extend(r[u'synonyms'])
        return names

    
class TestTnrsIpResolve(TestTnrsIplant):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(cls):
        return 'GET'


    @classmethod
    def namelist(cls, x):
        return x.json()[u'names'].split('|')


    @classmethod
    def tnrs_request(cls, names):
        return service.get_request('GET', {'names': u'|'.join(names)})

    
    def test_example_1(self):
        """Test example from the documentation."""
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        expected_names = [u'Acanthophyllum albidum', u'Acanthostachys pitcairnioides', u'Acanthostyles buniifolius']
        matched_names = self.all_matched_names(x)
        for name in expected_names:
            self.assertTrue(name in matched_names)


null=None; false=False; true=True

example_1 = service.get_request('GET', {u'names': u'Acanthophyllum albidum|Acanthostachys pitcairnioides|Acanthostyles buniifolius', u'fuzzy_match': True, u'multiple_match': False})


if __name__ == '__main__':
    print >>sys.stdout, '\n=================iPlant_TNRS_wrapper(GET)========================='
    webapp.main()

