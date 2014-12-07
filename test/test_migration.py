from dbupgrade.common import StepVersion, Migration
from dbupgrade.migration.SqlMigration import SqlUpdater, BaseUpdater
from dbupgrade.repository.file_repository import FileRepository

__author__ = 'Vincent'

import unittest


class BaseUpdaterCase(unittest.TestCase):
    def setUp(self):
        self.updater = BaseUpdater()

    def test_run_migration_upgrade(self):
        sample_repo = FileRepository('repository', 'app2')
        self.updater.migration = sample_repo.get_migration(version_from=StepVersion('4.0.1'),
                                                           version_to=StepVersion('4.10.0'))

        result = self.updater.run_migration()
        self.assertEqual(
            result,
            ("CREATE TABLE test_first (INTEGER a,VARCHAR b);\n"
             "CREATE TABLE test_second (INTEGER a,VARCHAR b);\n"
             "ALTER TABLE testfirst ADD COLUMN INTEGER C;\n"
            )
        )

    def test_run_migration_downgrade(self):
        repo = FileRepository('repository', 'app2')
        self.updater.migration = repo.get_migration(version_from=StepVersion('4.10.0'),
                                                    version_to=StepVersion('4.0.1'))

        result = self.updater.run_migration()
        self.assertEqual(
            result,
            ("ALTER TABLE testfirst DROP COLUMN C;\n"
             "DROP TABLE test_second;\n"
             "DROP TABLE test_first;\n"
            )
        )


class SqlUpdaterCase(unittest.TestCase):
    def setUp(self):
        self.sqlupdater = SqlUpdater()

    def test_initialize(self):
        self.assertEqual(
            self.sqlupdater.initialize(),
            '''CREATE TABLE public.dbupgrade_history (
    application  VARCHAR(90) NOT NULL,
    version VARCHAR(90) NOT NULL,
    timestamp DATE NOT NULL DEFAULT CURRENT_DATE
);
'''
        )

    def test_set_version(self):
        self.sqlupdater.migration = Migration('app2')

        self.assertEqual(
            self.sqlupdater.set_version(StepVersion('4.0.1')),
            "INSERT INTO public.dbupgrade_history SET (application,version) VALUES ('app2','4.0.1');\n"
        )

    def test_run_migration_upgrade(self):
        repo = FileRepository('repository', 'app2')
        self.sqlupdater.migration = repo.get_migration(version_from=StepVersion('4.0.1'),
                                                       version_to=StepVersion('4.10.0'))

        self.assertEqual(
            self.sqlupdater.run_migration(),
            "BEGIN;\n"

            "CREATE TABLE test_first (INTEGER a,VARCHAR b);\n"
            "INSERT INTO public.dbupgrade_history SET (application,version) VALUES ('app2','4.0.1.2');\n\n"

            "CREATE TABLE test_second (INTEGER a,VARCHAR b);\n"
            "INSERT INTO public.dbupgrade_history SET (application,version) VALUES ('app2','4.5.0');\n\n"

            "ALTER TABLE testfirst ADD COLUMN INTEGER C;\n"
            "INSERT INTO public.dbupgrade_history SET (application,version) VALUES ('app2','4.10.0');\n\n"

            "COMMIT;\n"
        )

    def test_run_migration_downgrade(self):
        repo = FileRepository('repository', 'app2')
        self.sqlupdater.migration = repo.get_migration(version_from=StepVersion('4.10.0'),
                                                       version_to=StepVersion('4.0.1'))

        self.assertEqual(
            self.sqlupdater.run_migration(),
            (
                "BEGIN;\n"

                "ALTER TABLE testfirst DROP COLUMN C;\n"
                "INSERT INTO public.dbupgrade_history SET (application,version) VALUES ('app2','4.10.0');\n\n"

                "DROP TABLE test_second;\n"
                "INSERT INTO public.dbupgrade_history SET (application,version) VALUES ('app2','4.5.0');\n\n"

                "DROP TABLE test_first;\n"
                "INSERT INTO public.dbupgrade_history SET (application,version) VALUES ('app2','4.0.1.2');\n\n"

                "COMMIT;\n"
            )
        )


if __name__ == '__main__':
    unittest.main()
