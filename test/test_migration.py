from dbupgrade.common import StepVersion
from dbupgrade.migration.SqlMigration import SqlMigration, BaseMigration
from dbupgrade.repository.file_repository import FileRepository

__author__ = 'Vincent'

import unittest


class BaseMigrationCase(unittest.TestCase):
    def setUp(self):
        self.migration = BaseMigration()

    def test_run_migration_upgrade(self):
        sample_repo = FileRepository('repository', 'app2')
        self.migration.migration = sample_repo.get_migration(version_from=StepVersion('4.0.1'),
                                                     version_to=StepVersion('4.10.0'))

        result = self.migration.run_migration()
        self.assertEqual(
            result,
            ("CREATE TABLE test_first (INTEGER a,VARCHAR b);\n"
             "CREATE TABLE test_second (INTEGER a,VARCHAR b);\n"
             "ALTER TABLE testfirst ADD COLUMN INTEGER C;\n"
            )
        )

    def test_run_migration_downgrade(self):
        repo = FileRepository('repository', 'app2')
        self.migration.migration = repo.get_migration(version_from=StepVersion('4.10.0'),
                                                      version_to=StepVersion('4.0.1'))

        result = self.migration.run_migration()
        self.assertEqual(
            result,
            ("ALTER TABLE testfirst DROP COLUMN C;\n"
             "DROP TABLE test_second;\n"
             "DROP TABLE test_first;\n"
            )
        )


class SqlMigrationCase(unittest.TestCase):
    def setUp(self):
        self.sqlmigration = SqlMigration()

    def test_initialize(self):
        self.assertEqual(
            self.sqlmigration.initialize(),
            '''CREATE TABLE public.dbupgrade_history (
    schema  VARCHAR(90) NOT NULL,
    version VARCHAR(90) NOT NULL,
    timestamp DATE NOT NULL DEFAULT CURRENT_DATE
);
'''
        )


if __name__ == '__main__':
    unittest.main()
