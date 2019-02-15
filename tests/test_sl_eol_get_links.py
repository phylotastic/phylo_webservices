# sl/eol/get_links

import sys, unittest, json
sys.path.append('./')
sys.path.append('../')
import webapp

service = webapp.get_service(80, "Info_url_species", 'sl/eol/get_links')

class SlEolGetLinksTester(webapp.WebappTestCase):
    def test_no_parameter(self):
        """Test no parameters"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        x = service.get_request(m, {}).exchange()
        mess = x.json().get(u'message')
        self.assert_response_status(x, 400)
        self.assertTrue('Missing parameter "species" in "%s"' % x.json()[u'message'])
        #self.assertTrue(u'species' in mess, 'no "species" in "%s"' % mess)


    def test_bad_parameter(self):
        """Test wrong parameter name"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        request = self.__class__.bad_sl_request(['Nosuchtaxonia notatall'])
        x = request.exchange()
        #x = service.get_request(m, {u'bad_parameter': u'Nosuchtaxonia notatall'}).exchange()
        self.assert_response_status(x, 400)
        # Check for informativeness
        mess = x.json()[u'message']
        self.assertTrue(u'parameter' in mess,
                        'no "parameter" in "%s"' % mess)


    def test_bad_species(self):
        """Test bad species name"""

        m = self.__class__.http_method()
        service = self.__class__.get_service()
        request = self.__class__.sl_request(['Nosuchtaxonia notatall'])
        x = request.exchange()
        #x = service.get_request(m, {u'species': u'Nosuchtaxonia notatall'}).exchange()
        # json.dump(x.to_dict(), sys.stdout, indent=2)
        self.assert_success(x)
        self.assertEqual(x.json()[u'species'][0][u'matched_name'], '')

    

class TestSlEolGetLinks(SlEolGetLinksTester):
    @classmethod
    def get_service(self):
        return service

    @classmethod
    def http_method(self):
        return 'GET'


    @classmethod
    def bad_sl_request(cls, names):
        return service.get_request('GET', {'bad_parameter': u'|'.join(names)})

    @classmethod
    def sl_request(cls, names):
        return service.get_request('GET', {'species': u'|'.join(names)})


    def test_example_1(self):
        x = self.start_request_tests(example_1)
        self.assert_success(x)
        self.assertEqual(x.json()[u'species'][0][u'matched_name'], u'Dendrocygna bicolor')
        self.assertEqual(x.json()[u'species'][0][u'eol_id'], 45510523) 

        self.assertEqual(x.json()[u'species'][1][u'matched_name'], u'Anser albifrons')
        self.assertEqual(x.json()[u'species'][1][u'eol_id'], 45510529)

        self.assertEqual(x.json()[u'species'][2][u'species_info_link'], u'https://eol.org/pages/45510544')
        self.assertEqual(x.json()[u'species'][2][u'eol_id'], 45510544)


null=None; false=False; true=True

example_1 = service.get_request('GET', {u'species': u'Dendrocygna bicolor|Anser albifrons|Cygnus buccinator'})

if __name__ == '__main__':
    print >>sys.stdout, '\n=================Info_url_species(GET)=========================' 
    webapp.main()
