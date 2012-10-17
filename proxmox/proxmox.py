##################################
#
# Python API to Proxmox REST API
# See http://pve.proxmox.com/wiki/Proxmox_VE_API for details.
#
# Requires: json, urllib, urlib2, logging, threading on the system
#
##################################

import json
import urllib
import urllib2
import logging

from .exceptions import ProxmoxAuthError, ProxmoxConnectionError, ProxmoxTypeError, ProxmoxError
from .exceptions import logcall

__author__ = "Andrew Bunday"
__copyright__ = "Baseblack Ltd 2012"
__license__ = ""
__version__ = "1.0.0"

LOGGING_LEVEL = logging.INFO
logging.basicConfig(format='%(levelname)s:%(funcName)s: %(message)s', level=LOGGING_LEVEL)


class ProxmoxAuthToken(object):
    """
    Authentication storage class. When called returns the ticket attribute by
    default. Any number of these _can_ be created during a session, but only 1
    is required. The ticket and CSRF tokens expire 2 hours after creation.
    """
    def __init__(self, user, ticket, CSRFPreventionToken):
        self.username = user
        self.ticket = ticket
        self.CSRFPreventionToken = CSRFPreventionToken

    def __repr__(self):
        return self.ticket


class ConnectorAPI(object):
    """
    Base transport class. Provides GET/POST/PUT functions for use by child classes.
    """

    def __init__(self, hostname, port=8006):
        """
        Sets the Proxmox api URL which is going to be used for all further interaction.
        Objects of this type should not be created directly. A subclass should be
        created.
        """
        object.__init__(self)

        self.host = hostname
        self.port = port
        self.baseurl = "https://{0}:{1}/api2/json".format(self.host, self.port)

        logging.debug('API endpoint base url is {baseurl}'.format(**self.__dict__))

    def fetch(self, filter, arguments=None):
        """
        Full GET request. Accepts both the filter arg of the simple_fetch but
        also a dict of arguments to be appended to the url.

        Example:    klass.fetch('version')
                        ==> "{urlbase}/version"

        Example:    klass.fetch('rrd', {'ds': 'cpu', 'timeframe': 'hour'})
                        ==> "{urlbase}/rrd/?ds=cpu&timeframe=hour"
        """
        url = "{0}/{1}".format(self.baseurl, filter)

        if arguments:
            try:
                urlencoded_arguments = urllib.urlencode(arguments)
                url = "{0}?{1}".format(url, urlencoded_arguments)
            except TypeError:
                raise ProxmoxTypeError("urllib.urlencode requires 'arguments' to be of type dict()")

        return self.__query('get', url)

    def post(self, filter, params={}):
        """
        Performs a POST request. Assumes that if params is a string it has already
        been urlencoded and is passed straight through. If it is not a string it will
        attempt to encode the dict.

        Raises an exception if it is unable to encode params.
        """
        url = "{0}/{1}".format(self.baseurl, filter)

        try:
            urlencoded_params = params if isinstance(params, str) else urllib.urlencode(params)
            return self.__query('post', url, urlencoded_params)
        except TypeError:
            raise ProxmoxConnectionError("'params' argument is if incorrect type. Should be a dict.")

    def put(self, filter, params={}):
        """
        Performs a PUT request. Assumes that if params is a string it has already
        been urlencoded and is passed straight through. If it is not a string it will
        attempt to encode the dict.

        Raises an exception if it is unable to encode params.
        """
        url = "{0}/{1}".format(self.baseurl, filter)

        try:
            urlencoded_params = params if isinstance(params, str) else urllib.urlencode(params)
            return self.__query('put', url, urlencoded_params)
        except TypeError:
            raise ProxmoxConnectionError("'params' argument is if incorrect type. Should be a dict.")

    def delete(self, filter, params={}):
        """
        Performs a PUT request. Assumes that if params is a string it has already
        been urlencoded and is passed straight through. If it is not a string it will
        attempt to encode the dict.

        Raises an exception if it is unable to encode params.
        """
        url = "{0}/{1}".format(self.baseurl, filter)

        try:
            urlencoded_params = params if isinstance(params, str) else urllib.urlencode(params)
            return self.__query('delete', url, urlencoded_params)
        except TypeError:
            raise ProxmoxConnectionError("'params' argument is if incorrect type. Should be a dict.")


    def __query(self, verb, url, post_params=None):
        """
        Performs a HTTP request for blah
        """
        logging.debug(url)
        if verb == 'get':
            request = urllib2.Request(url)
        if verb == 'post':
            request = urllib2.Request(url, post_params)
        if verb == 'put':
            request = urllib2.Request(url, post_params)
            request.get_method = lambda: 'PUT'
        if verb == 'delete':
            request = urllib2.Request(url, post_params)
            request.get_method = lambda: 'DELETE'

        headers = {"Accept": "application/json",
                   "CSRFPreventionToken": "%s" % self._auth.CSRFPreventionToken,
                   "Cookie": "PVEAuthCookie=%s" % self._auth.ticket}

        for k,v in headers.items():
            request.add_header(k, v)

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:  # username or password is incorrect.
            raise ProxmoxError(e)
        except urllib2.URLError as e:   # server or port are incorrect. or the server is down.
            raise ProxmoxConnectionError(e)

        try:
            fields = json.loads(response.read())
        except ValueError as e:  # malformed json
            logging.error(e)
            return

        return fields['data']



# Primary connection object
class Connector(ConnectorAPI):
    """
    Connector Class. This should be the first object which an application creates.
    This is used to fetch an authentication token and to access general information
    about the Proxmox cluster.

    This Class does not use AttrMethods to ensure that it does not accidentally get
    used in general execution.
    """
    def __init__(self, hostname, port=8006):
        ConnectorAPI.__init__(self, hostname, port)

    def fetch_auth_token(self, username, password):
        """
        Called with a valid username/password combination. Assumes @pam is provided
        in the username, if required.
        Returns a ProxmoxAuthToken object which contains a valid ticket and CSRFPreventionToken.
        If an invalid
        """
        url = "{baseurl}/access/ticket".format(**self.__dict__)
        post = urllib.urlencode({"username": str(username), "password": str(password)})
        headers = {"Accept": "application/json"}

        logging.debug("GET {0}".format(url))
        request = urllib2.Request(url, post, headers)

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:  # username or password is incorrect.
            raise ProxmoxAuthError(e)
        except urllib2.URLError as e:   # server or port are incorrect. or the server is down.
            raise ProxmoxConnectionError(e)

        try:
            fields = json.loads(response.read())
        except ValueError as e:
            logging.error(e)
            return

        if not fields['data']:  # returned None
            raise ProxmoxAuthError("Failed to obtain access token")

        ticket = fields['data']['ticket']
        CSRFPreventionToken = fields['data']['CSRFPreventionToken']

        self._auth = ProxmoxAuthToken(username, ticket, CSRFPreventionToken)
        return self._auth

    def access(self):
        return self.parameterized_fetch('access', {})

    def cluster(self):
        return self.parameterized_fetch('cluster', {})

    def nodes(self):
        return self.parameterized_fetch('nodes', {})

    def pools(self):
        return self.parameterized_fetch('pools', {})

    def storage(self, **kwargs):
        return self.fetch('storage', kwargs)

################################################################################
#
# Base Class for primary interface classes.
#
################################################################################
class Proxmox(ConnectorAPI):
    """
    Base Class inherited by all other interaction objects such as nodes/cluster etc.
    """
    def __init__(self, conn):
        """
        Consumes the Connector object provided into self
        """
        ConnectorAPI.__init__(self, conn.host, conn.port)
        self._auth = conn._auth

    def __getattr__(self, key):
        """
        A dynamic GET request is called when no other definition for the requested
        method can be found.
        """
        return AttrMethod(self, key)


class AttrMethod(object):
    """
    Dynamic method provider. For any method not already defined on a Proxmox
    based class an instance of this Class will be created and returned.

    When called the class provides a generic GET method.

    Any arguments passed to the __call__ in the form of keyword arguments

    ie, foo(a=1,b=2)

    are passed onto the GET method as a key/value pair dictionary.
    """
    def __init__(self, parent, method_name):
        self.parent = parent
        self.method_name = method_name

    def __getattr__(self, key):
        """
        Formats the any child attributes as a filter key.
        Example:   myobj.status.current() ==> "status/current"
        """
        return AttrMethod(self.parent, '/'.join((self.method_name, key)))

    def __call__(self, **kwargs):
        """
        Passes on the arguments to the call as a dict of key/values.
        """
        logging.debug("Generated call for %s/%s" % (self.parent.baseurl, self.method_name))
        return self.parent.fetch(self.method_name, kwargs)
