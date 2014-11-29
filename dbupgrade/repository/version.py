import os

__author__ = 'vincent'


class VersionException(Exception):
    pass


class Version(object):
    """
    Manage version numbering
    """

    def __init__(self, version_string, module_name):
        self.version_string = version_string
        self.module_name = module_name

    def __cmp__(self, other):
        if self.module_name != other.module_name:
            raise VersionException
        return cmp(self.version_string, other.version_string)

    def __repr__(self):
        return "%s.%s" % (self.module_name, self.version_string)


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
            self.versions.append(Version(version_string, module_name))
        self.versions.sort()


