from dbupgrade.common import Migration

__author__ = 'vincent'


class BaseMigration(object):
    def initialize(self):
        """
        This method setup
        :return: string
        """
        return ''

    def is_initialized(self):
        """

        :return: string
        """
        return ''

    def run_migration(self, migration):
        """
        This is the main method
        Run all the migrations steps
        :param migration: Migration
        :return: str
        """
        assert isinstance(migration, Migration)

        result_string = ''

        result_string += self.begin()

        for step_version in migration:
            result_string += self.single_migration(migration[step_version])

        result_string += self.end()

        return result_string

    def single_migration(self, text):
        """
        Run a single migration step
        :param text: str
        :return:
        """
        return text + "\n"

    def begin(self):
        """
        This method is executed before running any migration step
        :return:
        """
        return ''

    def end(self):
        """
        This method is executed after all migration steps has been executed
        :return:
        """
        return ''


class SqlMigration(BaseMigration):
    """

    """

    def __init__(self):
        pass

    def initialize(self):
        initialization_sql = ('CREATE TABLE public.dbupgrade_history (\n'
                              '    schema  VARCHAR(90) NOT NULL,\n'
                              '    version VARCHAR(90) NOT NULL,\n'
                              '    timestamp DATE NOT NULL DEFAULT CURRENT_DATE\n'
                              ');\n'
        )
        return initialization_sql

    def is_initialized(self):
        check_init = "SELECT schema,version,timestamp FROM public.dbupgrade_history LIMIT 1;\n"
        return check_init

    def begin(self):
        return 'BEGIN;' + "\n"

    def single_migration(self, text):
        return text + "\n" + self.set_version() + "\n"

    def end(self):
        return 'COMMIT;' + "\n"

    def set_version(self, version):
        return 'INSERT INTO public.dbupgrade_history SET (schema,version) VALUES (\'%s\',\'%s\');' % ('tata', 'titi')


class MigrationNotInitialized(Exception):
    pass