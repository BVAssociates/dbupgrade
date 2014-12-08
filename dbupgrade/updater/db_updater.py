from sqlite3 import OperationalError

from dbupgrade.updater.sql_updater import SqlUpdater


__author__ = 'Vincent'


class SqliteDBUpdater(SqlUpdater):
    def __init__(self, conn, migration=None):
        super(SqliteDBUpdater, self).__init__(migration)

        self.conn = conn
        self.cursor = None

        # configuration
        self.arg_str = '?'
        self.history_table = 'dbupgrade_history'

    def begin(self):
        self.cursor = self.conn.cursor()

    def end(self):
        #print "commiting..."
        self.conn.commit()

    def run_sql_statement(self, request, params=()):
        try:
            #print '==== BEGIN DUMP ===='
            #for line in self.conn.iterdump():
            #    print line
            #print '==== END DUMP ===='
            #print request

            self.cursor.execute(request, params)
        except OperationalError as o:
            raise OperationalError(o.message + " : " + request)

        return self.cursor.rowcount




