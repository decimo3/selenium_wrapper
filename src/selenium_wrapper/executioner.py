''' Module to wrap calls to external programs '''
import subprocess
from subprocess import SubprocessError
import logging
from .multilang import LANG

def execute(*args: str) -> str:
    ''' Function to execute and return code and stdout '''
    logger = logging.getLogger(__name__)
    if not args:
        raise ValueError(LANG.EXECUTIONER_ARGS_MISS)
    command = ' '.join(args)
    logger.debug(LANG.EXECUTIONER_COMMAND_TO_RUN, command)
    try:
        result = subprocess.run(
            args=command,
            capture_output=True,
            text=True,
            shell=False,
            check=True
            )
        logger.debug(LANG.EXECUTIONER_COMMAND_RESULT, result)
        return result.stdout
    except SubprocessError as e:
        raise SubprocessError(
            e.args or LANG.EXECUTIONER_EXEC_ERROR.format(program=args[0])) from e
    except FileNotFoundError as e:
        raise FileNotFoundError(
            e.args or LANG.EXECUTIONER_PROG_MISS.format(program=args[0])) from e
