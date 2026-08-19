''' Module to hold all custom exceptions classes '''

class ElementNotFoundError(Exception):
    ''' Custom exception to indicate when element is not found '''

class PathNotFoundError(Exception):
    ''' Custom exception to indicate when path is not found '''

class InvalidPathTypeError(Exception):
    ''' Custom exception to indicate when path type is not recognize '''

class CouldNotDetermineInstances(Exception):
    ''' Custom exception to indicate that number of instances cold not be defined '''

class MultiplesInstancesException(Exception):
    ''' Custom exception to indicate that multiples instances is running '''

class VersionNotFound(Exception):
    ''' Custom exception to indicate that version could not be defined '''

class CannotDownloadUpdate(Exception):
    ''' Custom exception to indicate that update couldn't be download '''
