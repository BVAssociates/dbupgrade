__author__ = 'vincent'


class SqlMigration(object):
    """

    """

    def __init__(self):
        pass

    def migration_join(self, migration_list):
        """
        return a string with the whole migration
        :param migration_list:
        :return string:
        """

        result_string = ''

        result_string += self.migration_begin()

        for migration in migration_list:
            result_string += self.migration_string(migration)
            result_string += self.set_version()

        result_string += self.migration_end()

    def migration_begin(self):
        return 'BEGIN;' + "\n"

    def migration_string(self, migration):
        return migration + "\n"

    def migration_end(self):
        return 'COMMIT;' + "\n"

    def set_version(self):
        return ''