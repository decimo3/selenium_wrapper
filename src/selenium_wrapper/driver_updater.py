''' Module that check updates and apply then '''
import os
import re
from pathlib import Path
import shutil
import zipfile
import logging
import requests
from .chrome_info import chrome_fullpath_finder
from .executioner import execute
from .exceptions import VersionNotFound, PathNotFoundError, CannotDownloadUpdate
from .version import Version
from .multilang import LANG

# pylint: disable=line-too-long,invalid-name
DRIVER_MILESTONE = 'https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone.json'
DRIVER_DOWNLOAD = 'https://storage.googleapis.com/chrome-for-testing-public/{driver_version}/win64/chromedriver-win64.zip'
# pylint: enable=line-too-long

def get_version_from_string_output(result: str) -> Version | None:
    ''' Function to get version number from version string '''
    match = re.search(r'\d+(?:\.\d+)+', result)
    if not match:
        return None
    return Version(match.group())

def googlechrome_get_local_version(chrome_path: str | None = None) -> Version:
    ''' Function to get installed Google Chrome version '''
    if not chrome_path:
        chrome_path = chrome_fullpath_finder()
    if not chrome_path:
        raise PathNotFoundError(LANG.UPDATER_CHROME_LOCAL_NOT_FOUND)
    if not os.path.exists(chrome_path):
        raise FileNotFoundError(LANG.UPDATER_CHROME_LOCAL_PATH_ERROR)
    version = get_version_from_string_output(execute(
        'powershell',
        f'-c "(Get-Item \'{chrome_path}\').VersionInfo.ProductVersion.ToString()"'
    ))
    if not version:
        raise VersionNotFound(LANG.UPDATER_CHROME_LOCAL_VERSION_ERROR)
    return version

def chromedriver_get_local_version() -> Version:
    ''' Function to get installed Chrome Driver version '''
    driver_path = Path.cwd() / 'chromedriver-win64' / 'chromedriver.exe'
    if not os.path.exists(driver_path):
        return Version(0, 0, 0)
    version = get_version_from_string_output(
        execute(str(driver_path), '--version'))
    if not version:
        raise VersionNotFound(LANG.UPDATER_DRIVER_LOCAL_VERSION_ERROR)
    return version

def chromedriver_get_remote_version(major: int) -> Version:
    ''' Function to get info about Chrome Driver versions '''
    response = requests.get(DRIVER_MILESTONE, timeout=60)
    data = response.json()
    data_version = data['milestones'][str(major)]['version']
    version = get_version_from_string_output(data_version)
    if not version:
        raise VersionNotFound(LANG.UPDATER_DRIVER_REMOTE_VERSION_ERROR)
    return version

def chromedriver_download_newer_version(driver_version: Version) -> None:
    ''' Function to download newer version of Chrome Driver '''
    update_path = Path.cwd() /  'chromedriver-win64.zip'
    driver_download = DRIVER_DOWNLOAD.format(driver_version=str(driver_version))
    response = requests.get(driver_download, timeout=60)
    if not response.ok:
        raise CannotDownloadUpdate(LANG.UPDATER_DRIVER_REMOTE_DOWNLOAD_ERROR)
    with open(update_path, 'wb') as file:
        file.write(response.content)

def chromedriver_remove_older_version() -> None:
    ''' Function to uninstall previous version '''
    driver_path = Path.cwd() / 'chromedriver-win64'
    if os.path.exists(driver_path):
        shutil.rmtree(driver_path)

def chromedriver_install_newer_version() -> None:
    ''' Function to install newer version '''
    update_path = Path.cwd() / 'chromedriver-win64.zip'
    if not os.path.exists(update_path):
        raise CannotDownloadUpdate(LANG.UPDATER_DRIVER_NEW_REMOTE_ERROR)
    with zipfile.ZipFile(update_path, 'r') as zip_ref:
        zip_ref.extractall()

def driver_updater(chrome_path: str | None = None) -> None:
    ''' Main function to check programs versions and update then '''
    logger = logging.getLogger(__name__)
    # Checking browser and driver versions
    logger.info(LANG.UPDATER_CHECKING_LOCAL_VERSIONS)
    chrome_version = googlechrome_get_local_version(chrome_path)
    logger.info(LANG.UPDATER_CHROME_LOCAL_MAJOR_VERSION, chrome_version)
    driver_version = chromedriver_get_local_version()
    logger.info(LANG.UPDATER_DRIVER_LOCAL_MAJOR_VERSION, driver_version)
    if driver_version == chrome_version:
        logger.info(LANG.UPDATER_EQUALS_LOCAL_VERSIONS)
        return
    # Looking for a ChromeDriver update
    logger.info(LANG.UPDATER_DRIVER_REMOTE_VERSION_CHECK)
    newer_version = chromedriver_get_remote_version(chrome_version.major)
    logger.info(LANG.UPDATER_DRIVER_REMOTE_VERSION_FOUND, newer_version)
    # Updating ChromeDriver to the new version
    logger.info(LANG.UPDATER_DRIVER_REMOTE_DOWNLOADING)
    chromedriver_download_newer_version(newer_version)
    logger.info(LANG.UPDATER_DRIVER_OLD_LOCAL_UNINSTALL)
    chromedriver_remove_older_version()
    logger.info(LANG.UPDATER_DRIVER_NEW_REMOTE_INSTALL)
    chromedriver_install_newer_version()
    logger.info(LANG.UPDATER_DRIVER_SUCCESSFUL_UPDATE)
    return
