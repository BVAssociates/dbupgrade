__author__ = 'vincent'


class StepVersion(object):
    """
    Manage version numbering.
    """

    def __init__(self, version_string):
        self.version_string = version_string

        if self.version_string == 'Infinite':
            self.version_string = '999999'

        try:
            self.version_internal = map(int, (self.version_string.split('.')))
        except ValueError:
            raise VersionException("Invalid version format %s" % self.version_string)

        # only accept 6 digit version number
        if len(self.version_internal) > 6:
            raise VersionException("Invalid version format %s" % self.version_string)

        # left fill with 0
        self.version_internal = tuple(self.version_internal + [0] * (6 - len(self.version_internal)))

    def __repr__(self):
        return self.version_string

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


class VersionException(Exception):
    pass