import os
import sys
import uuid

import MySQLdb

from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from cassandra.query import dict_factory

root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root)


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
        self.cdb = cdb
        self.mdb = mdb
        self.logger = logger
        self.logger.debug('Certificate object init complete')
        pass
