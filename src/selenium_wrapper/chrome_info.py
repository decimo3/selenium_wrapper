''' Module to find Google Chrome executable path '''
import os
import platform

def chrome_fullpath_finder() -> str | None:
    ''' Function to find Google Chrome executable path '''
    system = platform.system()

    if system == 'Windows':
        candidates = [
            os.path.expandvars(
                r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'
            ),
            os.path.expandvars(
                r'%PROGRAMFILES%\Google\Chrome\Application\chrome.exe'
            ),
            os.path.expandvars(
                r'%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe'
            ),
        ]

    elif system == 'Darwin':
        candidates = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            os.path.expanduser(
                '~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            ),
        ]

    elif system == 'Linux':
        candidates = [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/opt/google/chrome/google-chrome',
        ]

    else:
        return None

    for path in candidates:
        if os.path.isfile(path):
            return path

    return None
