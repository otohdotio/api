import json
import logging
import logging.handlers
import os
import sys

import cherrypy

# from api import include, model
root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root)

from api import include, model

# from api import model, include

__version__ = '0.1'
__author__ = 'jason'

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -' +
                              '%(message)s')
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.debug('logger initialized')


cdb = model.CassandraDatabase(logger)
mdb = model.MariaDBDatabase(logger)


class Test(object):
    exposed = True

    def __init__(self):
        self.logger.debug('Test object init complete ')

    def GET(self):
        cherrypy.response.status = 200
        return 'test successful'


class CA(object):
    exposed = True

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.logger.debug('CA object init complete')

    def GET(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])

    def POST(self):
        raise cherrypy.HTTPError(status=405,
                                 message='POST method not exposed for /ca, ' +
                                         'use GET or DELETE')

    def PUT(self):
        raise cherrypy.HTTPError(status=405,
                                 message='PUT method not exposed for /ca, ' +
                                         'use GET or DELETE')

    def DELETE(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])


class Cert(object):
    exposed = True

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.logger.debug('Cert object init complete')

    def GET(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])

    def POST(self):
        raise cherrypy.HTTPError(status=405,
                                 message='POST method not exposed for ' +
                                         '/cert, use GET or DELETE')

    def PUT(self):
        raise cherrypy.HTTPError(status=405,
                                 message='PUT method not exposed for /cert, ' +
                                         'use GET or DELETE')

    def DELETE(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])


class CSR(object):
    exposed = True

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.logger.debug('CSR object init complete')

    def GET(self):
        raise cherrypy.HTTPError(status=405,
                                 message='GET method not exposed for ' +
                                         '/csr, use POST')

    def POST(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])

    def PUT(self):
        raise cherrypy.HTTPError(status=405,
                                 message='PUT method not exposed for /csr, ' +
                                         'use POST')

    def DELETE(self):
        raise cherrypy.HTTPError(status=405,
                                 message='DELETE method not exposed for' +
                                         '/csr, use POST')


class Escrow(object):
    exposed = True

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.logger.debug('Escrow object init complete')

    def GET(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])

    def POST(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])

    def PUT(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])

    def DELETE(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])


class OCSP(object):
    exposed = True

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.logger.debug('OCSP object init complete')

    def GET(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])

    def POST(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])

    def PUT(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])

    def DELETE(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])


class Search(object):
    exposed = True

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.logger.debug('Search object init complete')

    def GET(self):
        raise cherrypy.HTTPError(status=405,
                                 message='GET method not exposed for ' +
                                         '/search, use POST')

    def POST(self):
        data = include.handle_json(cherrypy.request.headers['Content-Length'])

    def PUT(self):
        raise cherrypy.HTTPError(status=405,
                                 message='PUT method not exposed for '
                                         '/search, use POST')

    def DELETE(self):
        raise cherrypy.HTTPError(status=405,
                                 message='DELETE method not exposed for' +
                                         '/search, use POST')

cherrypy.tree.mount(
    Test(), '/test',
    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
)
cherrypy.tree.mount(
    CA(cdb, logger), '/ca',
    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
)
cherrypy.tree.mount(
    Cert(cdb, logger), '/cert',
    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
)
cherrypy.tree.mount(
    CSR(cdb, logger), '/csr',
    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
)
cherrypy.tree.mount(
    Escrow(cdb, logger), '/escrow',
    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
)
cherrypy.tree.mount(
    OCSP(cdb, logger), '/ocsp',
    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
)
cherrypy.tree.mount(
    Search(cdb, logger), '/search',
    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
)

application = cherrypy.tree
