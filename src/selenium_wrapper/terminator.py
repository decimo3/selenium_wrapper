''' Module to check multiples instances and kill residual processes '''
import platform
import logging
from .multilang import LANG
from .executioner import execute

def instance_killer() -> None:
    ''' Function to kill residual programs '''
    logger = logging.getLogger(__name__)
    system = platform.system()
    processes = {
        'Windows': ('chrome.exe', 'chromedriver.exe'),
        'Darwin': ('Google Chrome', 'chromedriver'),
        'Linux': ('chrome', 'chromedriver'),
    }
    if system not in processes:
        raise OSError(LANG.TERMINATOR_OS_ERROR.format(system=system))
    logger.info(LANG.TERMINATOR_KILLING_RESIDUAL_PROCESSES)
    for process in processes[system]:
        if system == 'Windows':
            execute('taskkill', '/F', '/IM', process)
        elif system in ('Darwin', 'Linux'):
            execute('pkill', '-f', process)
        else:
            raise OSError(LANG.TERMINATOR_OS_ERROR.format(system=system))
