from dbupgrade.repository.version import FileRepository, StepVersion

__author__ = 'vincent'

import unittest


class FileRepositoryCase(unittest.TestCase):
    def setUp(self):
        self.repo = FileRepository('test/repository')

    def test_list_applications(self):
        apps = self.repo.list_modules()
        self.assertEqual(['app1', 'app2'], apps)

    def test_list_versions(self):
        tested_app = 'app2'
        assert_versions = [
            StepVersion('4.0.1', tested_app),
            StepVersion('4.0.1.2', tested_app),
            StepVersion('4.5.0', tested_app),
            StepVersion('4.10.0', tested_app),
        ]
        versions = self.repo.list_versions(tested_app)

        self.assertEqual(assert_versions, versions)


if __name__ == '__main__':
    unittest.main()
