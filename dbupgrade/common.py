__author__ = 'vincent'

from collections import OrderedDict

class StepVersion(object):
    """
    Manage version numbering.
    """

    def __init__(self, version_string, module=None, content=None):
        self._version_string = version_string
        self._content = content
        self._module = module

        if self._version_string == 'Infinite':
            self._version_string = '999.999.999'

        try:
            self.version_internal = map(int, (self.version_string.split('.')))
        except ValueError:
            raise VersionException("Invalid version format %s" % self.version_string)

        # only accept 6 digit version number
        if len(self.version_internal) > 6:
            raise VersionException("Invalid version format %s" % self.version_string)

        for num in self.version_internal:
            if num > 999:
                raise VersionException("Unsupported version format %s" % self.version_string)

        # left fill with 0
        self.version_internal = tuple(
            tuple(self.version_internal) + tuple([0] * (6 - len(self.version_internal)))
        )

    # Properties
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def version_string(self):
        return self._version_string

    @property
    def module(self):
        return self._module

    # For debugging purpose
    def __repr__(self):
        return self.version_string

    # allow use it as key in dicts
    def __hash__(self):
        return hash(self.version_string)

    # rich comparisons
    def __eq__(self, other):
        assert isinstance(other, StepVersion)
        return self.version_internal == other.version_internal

    def __ne__(self, other):
        assert isinstance(other, StepVersion)
        return self.version_internal != other.version_internal

    def __gt__(self, other):
        assert isinstance(other, StepVersion)
        return self.version_internal > other.version_internal

    def __ge__(self, other):
        assert isinstance(other, StepVersion)
        return self.version_internal >= other.version_internal

    def __lt__(self, other):
        assert isinstance(other, StepVersion)
        return self.version_internal < other.version_internal

    def __le__(self, other):
        assert isinstance(other, StepVersion)
        return self.version_internal <= other.version_internal


class Migration(OrderedDict):
    """
    Manage a set of migration
    """

    def __setitem__(self, version, content):

        # hardened type
        if not isinstance(version, StepVersion):
            raise MigrationException
        if not isinstance(content, str):
            raise MigrationException

        # error on duplicate
        for k in self.keys():
            if k == version:
                raise MigrationException

        super(Migration, self).__setitem__(version, content)


class MigrationException(Exception):
    pass

class VersionException(Exception):
    pass