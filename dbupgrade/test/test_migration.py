from dbupgrade.repository.file_repository import FileRepository, RepositoryException
from dbupgrade.version import StepVersion
import os

__author__ = 'vincent'

import unittest


class FileRepositoryCase(unittest.TestCase):
    def setUp(self):
        self.repo = FileRepository('repository', 'app2')

    def test_list_applications(self):
        apps = FileRepository.list_modules('repository')
        self.assertEqual(['app1', 'app2'], apps)

    def test_list_versions(self):
        assert_versions = [
            StepVersion('4.0.1'),
            StepVersion('4.0.1.2'),
            StepVersion('4.5.0'),
            StepVersion('4.10.0'),
        ]
        versions = self.repo.list_versions()

        self.assertEqual(versions, assert_versions)

    def test_path_to_version(self):
        with self.assertRaises(RepositoryException):
            self.repo.path_to_version(version_from=StepVersion('7.0.0'))

        with self.assertRaises(RepositoryException):
            self.repo.path_to_version(version_to=StepVersion('7.0.0'))

        self.assertEqual(
            self.repo.path_to_version(version_from=StepVersion('4.5.0'), version_to=StepVersion('4.5.0')),
            []
        )

        self.assertEqual(
            self.repo.path_to_version(),
            [
                StepVersion('4.0.1'),
                StepVersion('4.0.1.2'),
                StepVersion('4.5.0'),
                StepVersion('4.10.0'),
            ]
        )

        # Upgrade
        self.assertEqual(
            self.repo.path_to_version(version_to=StepVersion('4.5.0')),
            [
                StepVersion('4.0.1'),
                StepVersion('4.0.1.2'),
                StepVersion('4.5.0'),
            ]
        )

        self.assertEqual(
            self.repo.path_to_version(version_from=StepVersion('4.0.1.2')),
            [
                StepVersion('4.5.0'),
                StepVersion('4.10.0'),
            ]
        )

        self.assertEqual(
            self.repo.path_to_version(version_from=StepVersion('4.0.1.2'), version_to=StepVersion('4.5.0')),
            [
                StepVersion('4.5.0'),
            ]
        )

        # Downgrade
        self.assertEqual(
            self.repo.path_to_version(version_from=StepVersion('4.5.0'), version_to=StepVersion('4.0.1.2')),
            [
                StepVersion('4.5.0'),
            ]
        )

        self.assertEqual(
            self.repo.path_to_version(version_from=StepVersion('4.10.0'), version_to=StepVersion('4.0.1')),
            [
                StepVersion('4.10.0'),
                StepVersion('4.5.0'),
                StepVersion('4.0.1.2'),

            ]
        )


if __name__ == '__main__':
    unittest.main()
