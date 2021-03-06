import os
import re

from dbupgrade.common import StepVersion, Migration


__author__ = 'vincent'


class FileRepository(object):
    """
    Manage the file structure tree and get file contents
    """

    def __init__(self, path, application):
        self.repository_path = path

        self.application = application

        # a list of StepVersion objects
        self.versions = []
        application_path = os.path.join(self.repository_path, self.application)
        for version_string in os.listdir(application_path):
            current_version = StepVersion(version_string)
            self.versions.append(current_version)

        self.versions.sort()

    @staticmethod
    def list_applications(repository_path):
        """
        list of available applications in repository

        :return list:
        """
        applications = os.listdir(repository_path)
        applications.sort()

        return applications

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
        :return hash:
        """

        migration_steps = self.path_to_version(version_from,version_to)

        # TODO: pattern from configuration
        pattern='^migrate_'
        if migration_steps[0] > migration_steps[-1]:
            pattern='^undo_'

        result = Migration(self.application)
        for step in migration_steps:
            step.content = self.read_file(step.version_string, pattern)
            result.append_step(step)

        return result

    def read_file(self, application_version, pattern):
        """
        return the content of the specified file

        :param application_version:
        :param pattern:
        :return string:
        """

        version_path = os.path.join(self.repository_path, self.application, application_version)

        found_files = []
        for step_file in os.listdir(version_path):
            if re.match('%s' % pattern, step_file):
                found_files.append(step_file)

        if len(found_files) != 1:
            raise RepositoryException

        # Slurp
        try:
            repo_file = open(os.path.join(version_path,found_files[0]))
            content = repo_file.read()
            repo_file.close()
        except IOError, e:
            raise RepositoryException('Unable to read file from repository : %s'%e)

        return content


class RepositoryException(Exception):
    pass


