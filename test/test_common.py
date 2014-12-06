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

    def test_module(self):
        sample_module = "module1"
        version = StepVersion('0.0.1', module=sample_module)
        self.assertEqual(version.module, sample_module)

        # read-only property
        with self.assertRaises(AttributeError):
            version.module = 'fail'


class MigrationCase(unittest.TestCase):
    def test_exception(self):
        migration = Migration()

        with self.assertRaises(MigrationException):
            migration['toto'] = 'something'
        with self.assertRaises(MigrationException):
            migration[StepVersion('4.0.1')] = 999
        with self.assertRaises(MigrationException):
            migration[StepVersion('4.0.1')] = 'one'
            migration[StepVersion('4.0.1')] = 'one'

    def test_order(self):
        assert_migration = {
            StepVersion('4.0.1'): 'one',
            StepVersion('4.0.1.2'): 'two',
            StepVersion('4.5.0'): 'three',
        }

        migration = Migration()
        migration[StepVersion('4.0.1')] = 'one'
        migration[StepVersion('4.0.1.2')] = 'two'
        migration[StepVersion('4.5.0')] = 'three'

        # assert keys are still sorted
        self.assertEqual(sorted(assert_migration.keys()), migration.keys())


if __name__ == '__main__':
    unittest.main()
