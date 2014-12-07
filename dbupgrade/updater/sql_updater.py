from dbupgrade.common import StepVersion

__author__ = 'vincent'


class BaseUpdater(object):
    def __init__(self, migration=None):
        self.migration = migration

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
        :return: str
        """

        result_string = ''

        result_string += self.begin()

        for step_version in self.migration.steps:
            result_string += self.single_migration(step_version)

        result_string += self.end()

        return result_string

    def single_migration(self, version):
        """
        Run a single migration step
        :param text: str
        :return:
        """
        return version.content + "\n"

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


class SqlUpdater(BaseUpdater):
    """

    """

    def initialize(self):
        initialization_sql = ('CREATE TABLE public.dbupgrade_history (\n'
                              '    application  VARCHAR(90) NOT NULL,\n'
                              '    version VARCHAR(90) NOT NULL,\n'
                              '    timestamp DATE NOT NULL DEFAULT CURRENT_DATE\n'
                              ');\n'
        )
        return initialization_sql

    def is_initialized(self):
        check_init = "SELECT application,version,timestamp FROM public.dbupgrade_history LIMIT 1;\n"
        return check_init

    def get_current_version(self):
        version_string = "SELECT version FROM public.dbupgrade_history where application = '%s' ORDER BY timestamp LIMIT 1;\n" % (
            self.migration.application
        )
        return StepVersion(version_string)


    def begin(self):
        return 'BEGIN;' + "\n"

    def single_migration(self, version):
        return version.content + "\n" + self.set_version(version) + "\n"

    def end(self):
        return 'COMMIT;' + "\n"

    def set_version(self, version):
        return 'INSERT INTO public.dbupgrade_history SET (application,version) VALUES (\'%s\',\'%s\');\n' % (
            self.migration.application, version.version_string
        )


class UpdaterNotInitialized(Exception):
    pass