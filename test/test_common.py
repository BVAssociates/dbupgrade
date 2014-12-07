from dbupgrade.common import Migration, StepVersion, MigrationException

__author__ = 'Vincent'

import unittest


class StepVersionCase(unittest.TestCase):
    def test_equal(self):
        version = StepVersion('4.0.1')
        same_version = StepVersion('4.0.1')

        self.assertEqual(version, same_version)

    def test_greater(self):
        version = StepVersion('0.0.1')
        upper_version = StepVersion('0.1.0')

        self.assertLess(version, upper_version)

    def test_content(self):
        sample_string = "it is a migration step!"
        version = StepVersion('0.0.1', content=sample_string)
        self.assertEqual(version.content, sample_string)

        another_sample_string = "it is another migration step!"
        version.content = another_sample_string
        self.assertEqual(version.content, another_sample_string)

class MigrationCase(unittest.TestCase):
    def test_exception(self):
        migration = Migration('myApp')
        version_one = StepVersion('4.0.1', 'one')

        with self.assertRaises(MigrationException):
            migration.append_step('toto')
        with self.assertRaises(MigrationException):
            migration.append_step(version_one)
            migration.append_step(version_one)

    def test_order(self):
        version_one = StepVersion('4.0.1', 'one')
        version_two = StepVersion('4.0.1.2', 'two')
        version_three = StepVersion('4.5.0', 'three')

        assert_migration = [
            StepVersion('4.0.1'),
            StepVersion('4.0.1.2'),
            StepVersion('4.5.0'),
        ]

        migration = Migration('myApp')
        migration.append_step(version_one)
        migration.append_step(version_two)
        migration.append_step(version_three)

        # assert keys are still sorted
        self.assertEqual(migration.steps, sorted(assert_migration))


if __name__ == '__main__':
    unittest.main()
