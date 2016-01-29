import os
import uuid

import MySQLdb.cursors
import OpenSSL
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra.query import dict_factory

# root = os.path.join(os.path.dirname(__file__), '.')
# sys.path.insert(0, root)

from ca import CA


class CassandraDatabase(object):

    def __init__(self, logger):
        self.logger = logger
        self.cluster = Cluster([os.environ['CASSANDRA']])
        self.session = self.cluster.connect()
        self.session.row_factory = dict_factory

    def keyspace(self, ks):
        self.session.set_keyspace(ks)

    def execute(self, desc, query):
        self.logger.debug('about to try: ' + desc)
        try:
            ## LOCAL_ONE only good for development
            ## TODO: make consistency level higher in production
            q = SimpleStatement(str(query),
                                consistency_level=ConsistencyLevel.LOCAL_ONE)
            rows = self.session.execute(q)
            return rows
        except Exception as e:
            description = str(desc) + ' failed on query:\n' + str(query) + \
                          '  reason:\n' + str(e)
            self.logger.critical('raising exception: ' + description)
            raise Exception(description)


class MariaDBDatabase(object):

    def __init__(self, logger):
        self.logger = logger
        try:
            self.db = MySQLdb.connect(host=os.environ['MDB_SERVER'],
                                      user='root',
                                      passwd=os.environ['MDB_PW'],
                                      db='otohdotio',
                                      cursorclass=MySQLdb.cursors.DictCursor)
        except MySQLdb.Error as e:
            raise Exception('Database.connect failed: ' + str(e))

    def execute(self, desc, sql):
        # TODO: figure out how to stop dropping the connection
        cursor = self.db.cursor()
        try:
            self.logger.debug('about to try: ' + sql)
            cursor.execute(sql)
            self.db.commit()
        except MySQLdb.Error as e:
            raise Exception(desc + 'failed on sql:\n  ' + sql + '  Exception:\n  '+ str(e))

        r = cursor.fetchallDict()
        self.logger.debug('looks good, returning:\n' + str(r))
        cursor.close()
        if isinstance(r, dict):
            return [r]
        else:
            return r


class Certificate(object):

    def __init__(self, logger, cdb, mdb):
        self.ca = CA(config='/ca_config.yaml')
        self.cdb = cdb
        self.mdb = mdb
        self.logger = logger
        self.logger.debug('Certificate object init complete')
        pass

    def get_new_sn(self):
        # Generate a new uuid4
        u = str(uuid.uuid4())

        # Insert it into the db, which auto_increments the primary key
        sql = """
                INSERT INTO certificate
                VALUES(NULL, '{0}')
              """
        sql = sql.format(u)
        try:
            self.mdb.execute('insert new uuid', sql)
        except MySQLdb.Error as e:
            raise e

        # Get the new serial number
        sql = """
                SELECT sn FROM certificate
                WHERE uuid = '{0}'
              """
        sql = sql.format(u)
        r = []
        try:
            r = self.mdb.execute('select new sn', sql)
        except MySQLdb.Error as e:
            raise e
        sn = str(r[0]['sn'])

        # Return the serial number and uuid
        return u, sn

    def set_cert(self, csr, key_use, ca_bool):
        # Load the CSR
        req = OpenSSL.crypto.load_certificate_request(OpenSSL.crypto.FILETYPE_PEM, csr)

        u = ''
        try:
            # Generate a new sequential SN and a random UUID
            u, sn = self.get_new_sn()
            # Now create the new cert
            cert_pem = self.ca.create_cert(csr, key_use, int(sn), ca_bool)
            cert_pem = cert_pem.replace('\n', '\\n')
            # Left off here, next step is to insert the cert into Cassandra
        except Exception as e:
            raise e

        # Generate our CQL queries to store the cert
        cql = """
                insert into cert (uuid, cert_sn, cert, ca_chain)
                values ('{0}', {1}, '{2}', null)
              """
        cql = cql.format(u, sn, cert_pem)
        # TODO: set up persistence container to contain otoh CA certs
        try:
            # Execute our CQL query
            self.cdb.execute('store cert', cql)
        except Exception as e:
            raise e

        return u, sn, cert_pem




