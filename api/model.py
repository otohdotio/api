

class CassandraDatabase(object):

    def __init__(self, logger):
        pass


class MariaDBDatabase(object):

    def __init__(self, logger):
        pass


class Certificate(object):

    def __init__(self, cdb, logger):
        self.cdb = cdb
        self.logger = logger
        self.logger.debug('Certificate object init complete')
        pass
