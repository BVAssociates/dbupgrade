import os

__author__ = 'vincent'


class VersionException(Exception):
    pass


class StepVersion(object):
    """
    Manage version numbering
    """

    def __init__(self, version_string, module_name):
        self.version_string = version_string
        self.module_name = module_name

        try:
            self.version_internal = map(int, (self.version_string.split('.')))
        except ValueError:
            raise VersionException("Invalid version format %s" % self.version_string)

        if len(self.version_internal) > 6:
            raise VersionException("Invalid version format %s" % self.version_string)

        self.version_internal = tuple(self.version_internal + [0] * (6 - len(self.version_internal)))

    def __eq__(self, other):
        return self.version_internal == other.version_internal

    def __repr__(self):
        return "%s.%s" % (self.module_name, '.'.join(map(str, self.version_internal)))


class FileRepository(object):
    """
    Manage the file structure tree and get file contents
    """

    def __init__(self, path):
        self.versions = []
        self.repository_path = path

        self.modules = os.listdir(path)
        self.modules.sort()

    def list_modules(self):
        """
        list of available modules in repository

        :return list:
        """
        return self.modules

    def list_versions(self, module_name):
        """
        list of available versions in repository

        :param module_name:
        :return list:
        """
        if not self.versions:
            self.read_versions(module_name)

        return self.versions

    def read_versions(self, module_name):
        for version_string in os.listdir(os.path.join(self.repository_path, module_name)):
            self.versions.append(StepVersion(version_string, module_name))
        self.versions.sort(key=lambda ver: ver.version_internal)



