import json
import logging
import logging.handlers
import collections
import sys

import cherrypy

# root = os.path.join(os.path.dirname(__file__), '..')
# sys.path.insert(0, root)

from model import CassandraDatabase, MariaDBDatabase, Certificate
from include import handle_json

__version__ = '0.1'

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -' +
                              '%(message)s')
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.debug('logger initialized')

cdb = CassandraDatabase(logger)
cdb.keyspace('otohdotio')
mdb = MariaDBDatabase(logger)

class Test(object):
    exposed = True

    def __init__(self, logger):
        self.logger = logger
        self.logger.debug('Test object init complete ')

    def GET(self):
        cherrypy.response.status = 200
        return 'test successful\n'


class CA(object):
    exposed = True

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.logger.debug('CA object init complete')

    def GET(self):
        # data = handle_json(cherrypy.request.headers['Content-Length'])
        raise cherrypy.HTTPError(status=500,
                                 message='Not implemented yet')

    def POST(self):
        raise cherrypy.HTTPError(status=405,
                                 message='POST method not exposed for /ca, ' +
                                         'use GET or DELETE')

    def PUT(self):
        raise cherrypy.HTTPError(status=405,
                                 message='PUT method not exposed for /ca, ' +
                                         'use GET or DELETE')

    def DELETE(self):
        # data = handle_json(cherrypy.request.headers['Content-Length'])
        raise cherrypy.HTTPError(status=500,
                                 message='Not implemented yet')


class Cert(object):
    exposed = True

    def __init__(self, cdb, mdb, logger):
        self.cdb = cdb
        self.mdb = mdb
        self.logger = logger
        self.certificate = Certificate(logger, cdb, mdb)
        self.logger.debug('Cert object init complete')

    def GET(self, **kwargs):
        if not kwargs.get('uuid') and not kwargs.get('cn'):
            raise cherrypy.HTTPError(status=400,
                                     message='ERROR: Must provide UUID or CN')
        if kwargs.get('uuid'):
            return json.dumps(self.certificate.get_cert(uuid=kwargs['uuid']))
        if kwargs.get('cn'):
            return json.dumps(self.certificate.get_cert(cn=kwargs['cn']))

    def POST(self):
        raise cherrypy.HTTPError(status=405,
                                 message='POST method not exposed for /cert, ' +
                                         'use GET or DELETE')

    def PUT(self):
        raise cherrypy.HTTPError(status=405,
                                 message='PUT method not exposed for /cert, ' +
                                         'use GET or DELETE')

    def DELETE(self):
        # I'm on the fence about this method. One one hand, it would be nice
        # to fully delete a certificate if it was created in error. On the
        # other hand, it would be better just to issue a revocation cert and
        # update the OCSP responder. For now we'll leave it in.
        od = collections.OrderedDict(sorted(cherrypy.request.wsgi_environ.items()))
        self.logger.debug('\n'.join("%s=%s" % (k, v) for (k, v) in od.iteritems()))
        cn = cherrypy.request.wsgi_environ['SSL_CLIENT_S_DN_CN']
        data = handle_json(cherrypy.request.headers['Content-Length'])
        if not data.get('uuid'):
            raise cherrypy.HTTPError(status=400,
                                     message='ERROR: Must provide UUID')
        if self.certificate.get_uuid_by_cn(cn) != data['uuid']:
            raise cherrypy.HTTPError(status=400,
                                     message='ERROR: You can only delete the' +
                                             'cert if you have it and ' +
                                             'provide it as a client cert. ' +
                                             'Otherwise, revoke the cert ' +
                                             'with the /ocsp endpoint.')
        try:
            self.certificate.delete_cert(cn, data['uuid'])
        except Exception as e:
            raise cherrypy.HTTPError(status=500,
                                     message='ERROR: failed to delete: ' +
                                     str(e))
        return json.dumps({'result': 'success'})


class CSR(object):
    exposed = True

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.logger.debug('CSR object init complete')
        self.certificate = Certificate(logger, cdb, mdb)
        self.logger.debug('Cert object init complete')

    def GET(self):
        raise cherrypy.HTTPError(status=405,
                                 message='GET method not exposed for ' +
                                         '/csr, use POST')

    def POST(self):
        data = handle_json(cherrypy.request.headers['Content-Length'])
        if not data.get('csr') or not data.get('key_use'):
            raise cherrypy.HTTPError(status=400,
                                     message='ERROR: Must provide CSR ' +
                                             'and key_use')
        if not data.get('is_ca'):
            is_ca = False
        else:
            is_ca = data['is_ca']
        uuid, sn, cert_pem = self.certificate.set_cert(data['csr'],
                                                       data['key_use'],
                                                       is_ca)
        return json.dumps({'uuid': uuid, 'sn': sn, 'cert': cert_pem})

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
        data = handle_json(cherrypy.request.headers['Content-Length'])

    def POST(self):
        data = handle_json(cherrypy.request.headers['Content-Length'])

    def PUT(self):
        data = handle_json(cherrypy.request.headers['Content-Length'])

    def DELETE(self):
        data = handle_json(cherrypy.request.headers['Content-Length'])


class OCSP(object):
    exposed = True

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        self.logger.debug('OCSP object init complete')

    def GET(self):
        data = handle_json(cherrypy.request.headers['Content-Length'])

    def POST(self):
        data = handle_json(cherrypy.request.headers['Content-Length'])

    def PUT(self):
        data = handle_json(cherrypy.request.headers['Content-Length'])

    def DELETE(self):
        data = handle_json(cherrypy.request.headers['Content-Length'])


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
        # data = handle_json(cherrypy.request.headers['Content-Length'])
        raise cherrypy.HTTPError(status=500,
                                 message='Method not yet implemented')

    def PUT(self):
        raise cherrypy.HTTPError(status=405,
                                 message='PUT method not exposed for '
                                         '/search, use POST')

    def DELETE(self):
        raise cherrypy.HTTPError(status=405,
                                 message='DELETE method not exposed for' +
                                         '/search, use POST')

cherrypy.tree.mount(
    Test(logger), '/test',
    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
)
cherrypy.tree.mount(
    CA(cdb, logger), '/ca',
    {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
)
cherrypy.tree.mount(
    Cert(cdb, mdb, logger), '/cert',
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
