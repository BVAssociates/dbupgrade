__author__ = 'vincent'


class StepVersion(object):
    """
    Manage version numbering.
    """

    def __init__(self, version_string, content=None):
        self._version_string = version_string
        self._content = content

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


class Migration(object):
    """
    Manage a set of migration
    """

    def __init__(self, application, version_list=None):
        self._application = str(application)
        self._steps = []

        if version_list:
            for version in version_list:
                self.append_step(version)

    def append_step(self, version):
        # error on duplicate
        if version in self.steps:
            raise MigrationException

        if not isinstance(version, StepVersion):
            raise MigrationException
        self.steps.append(version)

    @property
    def steps(self):
        return self._steps

    def content_steps(self):
        return tuple(step.content for step in self.steps)

    @property
    def application(self):
        return self._application

class MigrationException(Exception):
    pass

class VersionException(Exception):
    pass