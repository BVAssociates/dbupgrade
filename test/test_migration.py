import sqlite3

from dbupgrade.common import StepVersion, Migration
from dbupgrade.updater.db_updater import SqliteDBUpdater
from dbupgrade.updater.sql_updater import SqlUpdater
from dbupgrade.repository.file_repository import FileRepository


__author__ = 'Vincent'

import unittest


class SqlUpdaterCase(unittest.TestCase):
    def setUp(self):
        self.sqlupdater = SqlUpdater()

    def test_initialize(self):
        self.sqlupdater.initialize()

        self.assertEqual(
            self.sqlupdater.output_sql,
            ('BEGIN;\n'
             'CREATE TABLE public.dbupgrade_history (\n'
             '    application  VARCHAR(90) NOT NULL,\n'
             '    version VARCHAR(90) NOT NULL,\n'
             '    timestamp DATE NOT NULL DEFAULT CURRENT_DATE\n'
             ');\n'
             'COMMIT;\n'
            )
        )

    def test_set_version(self):
        self.sqlupdater.migration = Migration('app2')

        self.sqlupdater.set_version(StepVersion('4.0.1'))

        self.assertEqual(
            self.sqlupdater.output_sql,
            "INSERT INTO public.dbupgrade_history (application,version) VALUES ('app2','4.0.1');\n"
        )

    def test_run_migration_upgrade(self):
        repo = FileRepository('repository', 'app2')
        self.sqlupdater.migration = repo.get_migration(version_from=StepVersion('4.0.1'),
                                                       version_to=StepVersion('4.10.0'))

        self.sqlupdater.run_migration()

        self.assertEqual(
            self.sqlupdater.output_sql,
            "BEGIN;\n"

            "CREATE TABLE test_first (a INTEGER, b VARCHAR);\n"
            "INSERT INTO public.dbupgrade_history (application,version) VALUES ('app2','4.0.1.2');\n"

            "CREATE TABLE test_second (a INTEGER, b VARCHAR);\n"
            "INSERT INTO public.dbupgrade_history (application,version) VALUES ('app2','4.5.0');\n"

            "CREATE INDEX test_first_idx ON test_first (b);\n"
            "INSERT INTO public.dbupgrade_history (application,version) VALUES ('app2','4.10.0');\n"

            "COMMIT;\n"
        )

    def test_run_migration_downgrade(self):
        repo = FileRepository('repository', 'app2')
        self.sqlupdater.migration = repo.get_migration(version_from=StepVersion('4.10.0'),
                                                       version_to=StepVersion('4.0.1'))

        self.sqlupdater.run_migration()

        self.assertEqual(
            self.sqlupdater.output_sql,
            (
                "BEGIN;\n"

                "DROP INDEX test_first_idx;\n"
                "INSERT INTO public.dbupgrade_history (application,version) VALUES ('app2','4.10.0');\n"

                "DROP TABLE test_second;\n"
                "INSERT INTO public.dbupgrade_history (application,version) VALUES ('app2','4.5.0');\n"

                "DROP TABLE test_first;\n"
                "INSERT INTO public.dbupgrade_history (application,version) VALUES ('app2','4.0.1.2');\n"

                "COMMIT;\n"
            )
        )


class SqliteDBUpdaterCase(unittest.TestCase):
    def setUp(self):
        conn = sqlite3.connect(':memory:')
        self.sqlupdater = SqliteDBUpdater(conn)

        self.sqlupdater.initialize()
        self.maxDiff = None

    def test_initialize(self):

        self.assertTrue(self.sqlupdater.is_initialized())

    def test_run_migration_upgrade(self):
        repo = FileRepository('repository', 'app2')
        self.sqlupdater.migration = repo.get_migration(version_from=StepVersion('4.0.1'),
                                                       version_to=StepVersion('4.10.0'))

        self.sqlupdater.run_migration()

        self.sqlupdater.migration = repo.get_migration(version_from=StepVersion('4.10.0'),
                                                       version_to=StepVersion('4.0.1'))

        self.sqlupdater.run_migration()

        self.assertEqual(
            self.sqlupdater.schema_dump(),
            (
                'BEGIN TRANSACTION;\n'
                'CREATE TABLE dbupgrade_history (\n'
                '    application  VARCHAR(90) NOT NULL,\n'
                '    version VARCHAR(90) NOT NULL,\n'
                '    timestamp DATE NOT NULL DEFAULT CURRENT_DATE\n'
                ');\n'
                'COMMIT;\n'
            )
        )


if __name__ == '__main__':
    unittest.main()
