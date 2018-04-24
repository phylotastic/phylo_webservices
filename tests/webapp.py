"""Classes for web services, HTTP requests, and HTTP exchanges.
Also a testing superclass for use by all the specific service test classes.

This utility is specific to the phylotastic web API, not a
completely general tool."""

import sys, os, requests, time, unittest, json, time

# The content-type that we anticipate getting from the web services
# when the content is json.
anticipated_content_type = 'application/json'

# Ensure unique instantiation of each service object

services_registry = {}    # url -> Service
requests_registry = {}    # label -> Request

def get_service(group, service_name, specific_path):
    """Retrieve or create a Service object for a single URL.
    'group' is actually a port number (5004 etc.).
    'specific_path' is the part of the path in the URL
    following the part that is shared by all the services, e.g.
    'fn/names_url'. """

    url = str('http://phylo.cs.nmsu.edu:%s/phylotastic_ws/%s' % (group, specific_path))
    
    if url in services_registry:
        return services_registry[url]
    service = Service(url, service_name)
    services_registry[url] = service
    return service

def parse_service_url(url):
    """Given a URL, extract the 'group' and 'specific_path'
    (See the get_service function.)"""

    parts = url.split('/phylotastic_ws/')
    #return parts[0], parts[1]    
    return (parts[0].split(':')[1], parts[1])

def get_request(label):
    """Retrieve an existing Request object having the given label."""
    return requests_registry.get(str(label))

class Service():
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.requests = {}  # maps (method, parameters) to Request

    def get_request(self, method='GET', parameters={},
                    label=None, source=None, expect_status=None):
        key = (method, json.dumps(parameters, sort_keys=True))
        r = self.requests.get(key)	
        if r == None:
            r = Request(self, method, parameters, label, source=source, expect_status=expect_status)
            self.requests[key] = r
        elif label != None:
            # Add label to existing Request that has none
            r.label = label
            requests_registry[str(label)] = r
        
        return r

    # exchange blob
    def get_request_from_blob(self, blob):
        return self.get_request(blob[u'method'],
                                (blob[u'parameters']
                                 if u'parameters' in blob
                                 else blob[u'data']),
                                label=blob[u'label'],
                                source=blob[u'source'])

    def name(self):
        return self.url.split('phylotastic_ws/')[-1]

    def get_examples(self):
        return [r for r in self.requests.values() if r.examplep]

    def get_times():
        times = []
        for r in requests.values():
            for x in r.exchanges:
                times.append(x.time)
        return times

class Request():
    """Every Service has a set of requests that can be (or have been) made.
    It's useful to keep track of them, e.g. so that we can do timing profiles.
    Typically a Request is a test or example."""

    def __init__(self, service, method, parameters, label, source=None, expect_status=None):
        self.service = service
        self.method = method
        self.parameters = parameters
        self.label = label
        if label != None:
            requests_registry[str(label)] = self
        self.source = source
        self.expect_status = expect_status
        self.exchanges = []   # ?
        
    def exchange(self):
        """Perform a single exchange for this request (method, url, query)"""

        time1 = time.time()      # in seconds, floating point
        if self.method == 'GET':
            # should we set an accept: header here?
            # in theory, yes.
            # but no, because the documentation never sets one.
            resp = requests.get(self.service.url,
                                params=self.parameters,
                                headers={'Accept': 'application/json,*/*;q=0.1'})
        elif self.method == 'POST':
            resp = requests.post(self.service.url,
                                 headers={'Content-type': 'application/json',
                                          'Accept': 'application/json,*/*;q=0.1'},
                                 data=json.dumps(self.parameters))
        else:
            print >>sys.stderr, '** unrecognized method:', self.method
        time2 = time.time()
        x = Exchange(self, response=resp, time=(time2 - time1))
        self.exchanges.append(x) # for timing analysis
        return x

    def stringify(self):
        return('%s %s?%s' %
               (self.method,
                self.service.url,
                json.dumps(self.parameters)[0:60]))

    def to_dict(self):
        return {'label': self.label,
                'service': self.service.url,
                'method': self.method,
                'parameters': self.parameters,
                'source': self.source,
                'expect_status': self.expect_status}

def to_request(blob):
    if isinstance(blob, unicode):
        # blob is a label and is globally unique
        r = get_request(blob)
        if r == None:
            print >>sys.stderr, '** No such request:', label
        return r
    else:
        (group, specific_path) = parse_service_url(blob[u'service'])
        service = get_service(group, specific_path)
        return service.get_request(method=blob[u'method'],
                                   parameters=blob[u'parameters'],
                                   label=blob[u'label'],
                                   source=blob[u'source'],
                                   expect_status=blob.get(u'expect_status'))

class Exchange():
    """An Exchange is an activation of a Request yielding either an error
    or a response (in the 'requests' library sense) and taking up time."""

    def __init__(self, request, time=None, response=None,
                 content_type='application/json',     # type *requested*
                 status_code=200, text=None, json=None):
        self.request = request
        self.time = time
        self.the_json = False
        if response != None:
            self.status_code = response.status_code
            self.text = response.text
            self.the_json = None
            ct = response.headers['content-type'].split(';')[0]
            self.content_type = ct
            if ct == 'application/json':
                self.the_json = response.json()
                if self.status_code == 200 and u'status_code' in self.the_json:
                    self.status_code = self.the_json[u'status_code']

        else:
            self.content_type = content_type
            self.status_code = status_code
            self.text = text
            self.the_json = json

    def json(self):
        return self.the_json

    def to_dict(self):
        if False:
            return {'request': self.request.to_dict(),
                    'time': self.time,
                    'status_code': self.status_code,
                    'content_type': self.content_type,
                    'response': self.json()}
        else:
            return {'request': self.request.label,
                    'time': self.time,
                    'status_code': self.status_code,
                    'content_type': self.content_type,
                    'response': self.json()}

def to_exchange(blob):
    rd = blob.get(u'request')
    if rd == None:
        # backward compatibility.  delete this code in a bit.
        (group, specific_path) = parse_service_url(blob[u'service'])
        service = get_service(group, specific_path)
        request = service.get_request(method=blob[u'method'],
                                      parameters=blob[u'data'],
                                      source=blob.get(u'source'))
    else:
        request = to_request(rd)
        if request == None:
            return None
    return Exchange(request,
                    content_type=blob[u'content_type'],
                    status_code=blob[u'status_code'],
                    json=blob[u'response'])


class WebappTestCase(unittest.TestCase):
    """Subclass of unittest.TestCase with some additional methods that are
    useful for testing web services.

    There should be one subclass of this class for each service."""

    # These methods get overridden in the subclasses!
    @classmethod
    def http_method(cls):
        raise unittest.SkipTest("can't test superclass")
    @classmethod
    def get_service(cls):
        raise unittest.SkipTest("can't test superclass")

    # Shortcut
    def get_request(self, method, parameters):
        return this.__class__.get_service().get_request(method, parameters)

    def assert_success(self, x, message=None):
        """Ensure that the JSON has the form of a successful response.
        x is an Exchange"""

        self.assert_response_status(x, 200, message)
        j = x.json()
        self.assertTrue(u'message' in j)
        self.assertEqual(j[u'message'], u'Success')
        
    
    def assert_response_status(self, x, code, message=None):
        if message == None:
            message = '%s %s' % (x.status_code, x.json().get(u'message'))
        if x.status_code < 300:
            self.assertEqual(x.content_type, u'application/json', message)
        self.assertEqual(x.status_code, code, message)

    
    def start_request_tests(self, request):
        present = request.exchange()
        if len(request.exchanges) > 0:
            self.check_adequacy(present, request.exchanges[0])
        return present

    def check_adequacy(self, now, then):
        """Is the 'now' exchange no worse than the 'then' exchange?"""
        now_cat = now.status_code / 100
        then_cat = then.status_code / 100
        self.assertTrue(now_cat <= then_cat)
        if now_cat == then_cat:
            self.assertTrue(now.status_code <= then.status_code)
            self.check_result(now.json(), then.json())
        else:
            print >>sys.err, ('Better status code now (%s) than before (%s)' %
                              (now.status_code, then.status_code))

    def check_result(self, now, then):
        """Recursion: Is the 'now' result no worse than the 'then' result?"""
        if isinstance(then, dict):
            self.assertTrue(isinstance(now, dict))
            for key in then:
                # Do we still have everything we had before?
                self.assertTrue(key in now)
                if key == u'creation_time': continue
                if key == u'execution_time': continue
                self.check_result(now[key], then[key])
        elif isinstance(then, list):
            self.assertTrue(isinstance(now, list))
            self.assertEqual(len(now), len(then))
            for (n, t) in zip(now, then):
                self.check_result(n, t)
        else:
            self.assertFalse(isinstance(now, dict))
            self.assertFalse(isinstance(now, list))
            self.assertEqual(now, then)

    @classmethod
    def tearDownClass(cls):
        maxtime = 0
        service = cls.get_service()
        if service == None: return
        for r in service.requests.values():
            for x in r.exchanges:
                if x.status_code == 200 and x.time > maxtime:
                    maxtime = x.time
        #if maxtime > 0:
        #   print >>sys.stderr, '\nSlowest exchange for %s: %s' % (service.url, maxtime)
        print >>sys.stderr, '\nFinished testing for %s service.'%service.name
        print >>sys.stderr, '\n==============================================='

    def user_credentials(self):
        expires = config('access_token_expires')
        if expires == None or time.time() < expires:
            return (config('user_id'), config('access_token'))
        else:
            raise unittest.SkipTest("access token expired")


def find_resource(path):
    """Find a resource file on sys.path"""

    for option in sys.path:
        full = os.path.join(option, path)
        if os.path.exists(full):
            return full
    print >>sys.stderr, 'No such resource:', path
    return None

'''
the_configuration = None

def config(param):
    """Get value from configuration file"""

    global the_configuration
    if the_configuration == None:
        path = find_resource('config.json')
        if path == None: return None
        with open(find_resource('config.json')) as infile:
            the_configuration = json.load(infile)
    if not param in the_configuration:
        print >>sys.stderr, 'No such configuration parameter:', param
    return the_configuration.get(param)
'''

def main():
    """Main function for use by test_ files"""

    unittest.main()
    
