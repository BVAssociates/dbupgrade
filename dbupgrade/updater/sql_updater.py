from dbupgrade.common import StepVersion

__author__ = 'vincent'


class BaseUpdater(object):
    def __init__(self, migration=None):
        self.migration = migration

    def initialize(self):
        """
        This method prepare the updater to receive future migration
        """
        pass

    def is_initialized(self):
        """

        :return: bool
        """
        return False

    def get_current_version(self):
        """
        Return the version of the current component to update
        :return: StepVersion
        """
        return StepVersion(0)

    def run_migration(self):
        """
        This is the main method
        Run all the migrations steps
        :param migration: Migration
        """

        self.begin()

        for step_version in self.migration.steps:
            self.single_migration(step_version)

        self.end()

    def single_migration(self, version):
        """
        Run a single migration step
        :param text: str
        :return:
        """
        pass

    def begin(self):
        """
        This method is executed before running any migration step
        """
        pass

    def end(self):
        """
        This method is executed after all migration steps has been executed
        :return:
        """
        pass


class SqlUpdater(BaseUpdater):
    """
    An universal SQL Updater class. It outputs plain SQL.
    Must be override for each real database provider you will choose.
    """

    def __init__(self, migration=None):
        super(SqlUpdater, self).__init__(migration)

        self.arg_str = '%s'
        self.history_table = 'public.dbupgrade_history'

        self.output_sql = ''

    def initialize(self):
        self.begin()

        initialization_sql = ('CREATE TABLE %s (\n'
                              '    application  VARCHAR(90) NOT NULL,\n'
                              '    version VARCHAR(90) NOT NULL,\n'
                              '    timestamp DATE NOT NULL DEFAULT CURRENT_DATE\n'
                              ');' % (self.history_table,)
        )

        self.run_sql_statement(initialization_sql)

        self.end()

    def is_initialized(self):
        return self.run_sql_statement('SELECT application,version,timestamp FROM %s LIMIT 1;' % self.history_table)

    def get_current_version(self):
        self.begin()
        version_string = self.run_sql_statement(
            'SELECT version FROM %s where application = %s ORDER BY timestamp LIMIT 1;' % (
                self.history_table, self.arg_str),
            (self.migration.application)
        )
        self.end()
        return StepVersion(version_string)


    def begin(self):
        self.output_sql = ''
        self.run_sql_statement('BEGIN;')

    def single_migration(self, version):
        self.run_sql_statement(version.content)
        self.set_version(version)

    def end(self):
        self.run_sql_statement('COMMIT;')

    # SQL Specifics methods

    def set_version(self, version):
        """
        Store the running step into an history table
        :param version:
        :return:
        """
        self.run_sql_statement(
            'INSERT INTO %s (application,version) VALUES (%s,%s);' % (
                self.history_table, self.arg_str, self.arg_str),
            (self.migration.application, version.version_string)
        )

    def run_sql_statement(self, request, params=()):
        """
        Main execution method for each statement. In Output mode, only print the request.
        In DB mode, this method will be override by real execution method
        :param request: str
        :param params: tuple of str
        :return: str
        """

        # simple string formatting RISK OF SQL INJECTION, DO NOT USE IN REAL DATABASE
        output = request % tuple(["'" + p + "'" for p in params])

        self.output_sql += output + "\n"


class UpdaterNotInitialized(Exception):
    pass