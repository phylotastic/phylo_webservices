# 3. tnrs/ot/resolve
# GET

import sys, os, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(5004, "OToL_TNRS_wrapper", 'tnrs/ot/resolve')

class TnrsTester(webapp.WebappTestCase):
    
    def test_no_parameter(self):
        """Test no parameter
        Ensure that we get failure if names parameter is unsupplied because names parameter is 'mandatory'."""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, {}).exchange()
        
        self.assert_response_status(x, 400)

        # Test for informativeness
        #self.assertTrue('ame' in x.json()[u'message'])
        self.assertTrue('Missing parameter "names" in "%s"' % x.json()[u'message'])

    def test_3(self):
        """Test that returned result is 'correct' per documentation.
        """

        name = u'Pseudacris crucifer'
        m = self.http_method()
        request = self.__class__.tnrs_request(['Pseudacris crucifer'])
        x = request.exchange()
        self.assert_success(x)
        # Check that Pseudacris crucifer is among the matched names
        matched_names = self.all_matched_names(x)
        self.assertTrue(name in matched_names)

    def test_4(self):
        """Test misspelled names in the input.
        There's no such thing as 'Setophaga megnolia'."""

        namesx = [(u'Setophaga striata', True),
                  (u'Setophaga megnolia', False),
                  (u'Setophaga angilae', False),
                  (u'Setophaga plumbea', True),
                  (u'Setophaga virens', True)]
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

    def test_5(self):
        namesx = [(u'Formica polyctena', True),
                  (u'Formica exsectoides', True),
                  (u'Formica pecefica', False)]
        self.try_names(namesx)

    @unittest.skip("temporarily to save time")
    def test_big_request(self):
        """Try a request with many copies of the same name.
        128 copies succeeds, 256 fails (assuming GET - POST might be 
        more capacious)."""
        n = 1
        names = [u'Formica polyctena']
        m = self.http_method()
        while True:
            print >>sys.stderr, 'Testing big request %s' % n
            request = self.__class__.tnrs_request(names)
            x = request.exchange()
            if x.status_code != 200:
                print >>sys.stderr, 'Big request status %s at %s names' % (x.status_code, n)
                print >>sys.stderr, x.text
                break
            n = n * 2
            if n > 10000000: break
            names = names + names


class TestTnrsOtResolve(TnrsTester):
    @classmethod
    def get_service(cls):
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

    def test_2(self):
        """Test edge case: parameter name 'names' is supplied, but there is no value.
        """

        m = self.http_method()
        request = self.__class__.tnrs_request([])
        x = request.exchange()
        self.assert_response_status(x, 400)
        #print x.json()[u'message']
        self.assertTrue('"names" parameter must have a valid value in "%s"' % x.json()[u'message'])

    def test_example_1(self):
        """Test example from the documentation."""
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        name = u'Setophaga striata'
        matched_names = self.all_matched_names(x)
        self.assertTrue(name in matched_names)
        

    def test_example_2(self):
        """Test example from the documentation."""
        x = self.start_request_tests(example_2)
        self.assert_success(x)
        expected_names = [u'Formica exsectoides', u'Formica polyctena']
        matched_names = self.all_matched_names(x)
        for name in expected_names:
            self.assertTrue(name in matched_names)


null=None; false=False; true=True

example_1 = service.get_request('GET', {u'names': u'Setophaga striata|Setophaga megnolia|Setophaga angilae|Setophaga plumbea|Setophaga virens'})
example_2 = service.get_request('GET', {u'names': u'Formica polyctena|Formica exsectoides|Formica pecefica'})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================OToL_TNRS_wrapper(GET)========================='
    webapp.main()
