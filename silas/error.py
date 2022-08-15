class SilasError(Exception):
    """ Basic error
    """

    def __init__(self, msg):
        self.msg = msg


class FileNotFundError(SilasError):
    """ File not found
    """


class UnsetEnvError(SilasError):
    """ No environment variables are configured
    """


class UnrealizedError(SilasError):
    """ The specified method is not implemented
    """


class TypeTransError(SilasError):
    """ Type conversion failed
    """