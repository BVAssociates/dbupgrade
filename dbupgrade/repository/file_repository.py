import os
import re

from dbupgrade.version import StepVersion


__author__ = 'vincent'


class FileRepository(object):
    """
    Manage the file structure tree and get file contents
    """

    def __init__(self, path, module):
        self.repository_path = path

        self.module = module

        # a list of StepVersion objects
        self.versions = []
        module_path = os.path.join(self.repository_path, self.module)
        for version_string in os.listdir(module_path):
            current_version = StepVersion(version_string)
            self.versions.append(current_version)

        self.versions.sort()

    @staticmethod
    def list_modules(repository_path):
        """
        list of available modules in repository

        :return list:
        """
        modules = os.listdir(repository_path)
        modules.sort()

        return modules

    def list_versions(self):
        """
        List of available versions in repository

         :return list:
        """

        return self.versions

    def path_to_version(self, version_from=None, version_to=None):

        # check if version_from exists
        if version_from:
            found = [item for item in self.versions if version_from == item]
            if len(found) == 0:
                raise RepositoryException('Version %s does not exists in repository' % str(version_from))
        else:
            version_from = StepVersion('0')

        # check if version_to exists
        if version_to:
            found = [item for item in self.versions if version_to == item]
            if len(found) == 0:
                raise RepositoryException('Version %s does not exists in repository' % str(version_from))
        else:
            version_to = StepVersion('Infinite')

        # it is a downgrade!
        downgrade = False
        if version_from > version_to:
            tmp = version_from
            version_from = version_to
            version_to = tmp

            downgrade = True

        versions_path = []

        for step in self.versions:

            if version_from < step <= version_to:
                versions_path.append(step)

        if downgrade:
            versions_path.reverse()

        return versions_path

    def get_migration(self, version_from=None, version_to=None):
        """
        Read filesystem and return

        :type version_from: object
        :return:
        """

        migration_steps = []
        for step in self.list_versions():
            pass

    def _fs_readfile(self, module_version, pattern):
        """
        return the content of the specified file

        :param module_version:
        :param pattern:
        :return string:
        """

        version_path = os.path.join(self.repository_path, self.module, module_version)

        found_files = []
        for step_file in os.listdir(version_path):
            if re.match('^%s' % pattern, step_file):
                found_files.append(step_file)

        if len(found_files) != 1:
            raise RepositoryException

        repo_file = open(found_files[0])
        content = repo_file.readall()
        repo_file.close()

        return content


class RepositoryException(Exception):
    pass


