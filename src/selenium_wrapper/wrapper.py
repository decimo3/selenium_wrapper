''' Module that allows to handle WebDriver easily. '''
import logging
from enum import Enum
from pathlib import Path
from time import sleep
from datetime import datetime, timedelta
from dotenv import dotenv_values
from selenium.webdriver.chrome import webdriver, options, service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from .exceptions import ElementNotFoundError, PathNotFoundError, InvalidPathTypeError
from .chrome_info import chrome_fullpath_finder
from .driver_updater import driver_updater
from .terminator import instance_killer
from .multilang import LANG

class WaitSec(Enum):
    ''' Explicit wait times, in seconds, for an element to become visible. '''
    NOW = 0
    SHORT = 3
    MED = 7
    LONG = 15
    MAX = 30

BY = {
    '#': By.ID,
    '/': By.XPATH,
    '.': By.CLASS_NAME
}

class Wrapper:
    ''' A wrapper around WebDriver. '''
    def __init__(
        self,
        website_path: str,
        paths_file: str | Path | None = None,
        ) -> None:
        self.logger = logging.getLogger(__name__)
        self.paths = dotenv_values(
            Path.cwd() / 'path.ini'
            if not paths_file else
            Path(paths_file)
        )
        instance_killer()
        driver_updater()
        self.initialize(website_path)
    def initialize(
            self,
            website_path: str,
        ) -> None:
        ''' Startup Selenium WebDriver Wrapper '''
        site_url = self.paths.get(website_path)
        if not site_url:
            raise PathNotFoundError(LANG.WRAPPER_URL_NOT_DEFINED)
        temp_path = Path.cwd() / 'tmp'
        driver_path = Path.cwd() / 'chromedriver-win64' / 'chromedriver.exe'
        if not driver_path.exists():
            raise FileNotFoundError(LANG.WRAPPER_DRIVER_NOT_FOUND)
        _service = service.Service(executable_path=str(driver_path))
        _options = options.Options()
        chrome_path = chrome_fullpath_finder()
        if not chrome_path:
            chrome_path = self.paths.get('GOOGLE_CHROME')
            if not chrome_path:
                raise FileNotFoundError(LANG.WRAPPER_CHROME_NOT_FOUND)
        _options.binary_location = chrome_path
        _options.add_argument(f'--app={site_url}')
        _options.add_argument(f'--user-data-dir={temp_path}')
        self.driver = webdriver.WebDriver(service=_service, options=_options)
        self.driver.maximize_window()
    def get_elements(
            self,
            pathname: str,
            timeout: WaitSec = WaitSec.NOW,
            replace_text: int | list[int] | None = None,
        ) -> list[WebElement] | None:
        ''' Function to get a list of WebElements '''
        # Example 1: /html/body/main/form
        # Will be By.XPATH and '/html/body/main/form'
        # Example 2: #form-item
        # Will be By.CLASS_NAME and 'form-item'
        # Example 3: .form-id
        # Will be By.ID and 'form-id'
        self.logger.debug(LANG.WRAPPER_PATH_TO_FIND, pathname, timeout.name)
        path_value = self.paths.get(pathname)
        if not path_value:
            raise PathNotFoundError(
                LANG.WRAPPER_PATH_NOT_FOUND.format(pathname=pathname))
        if isinstance(replace_text, int):
            path_value = path_value.replace('?', str(replace_text))
        if isinstance(replace_text, list):
            for x in replace_text:
                path_value = path_value.replace('?', str(x), 1)
        by_type = BY.get(path_value[:1], '')
        if not by_type:
            raise InvalidPathTypeError(
                LANG.WRAPPER_PATH_TYPE_MISTYPE.format(pathname=pathname))
        by_value = path_value[1:] if by_type != By.XPATH else path_value
        self.logger.debug(LANG.WRAPPER_ELEMENT_TO_FIND, by_type, by_value)
        expiration_time = datetime.now() + timedelta(seconds=timeout.value)
        while True:
            elements = self.driver.find_elements(by_type, by_value)
            if elements and elements[0].is_displayed() and elements[0].is_enabled():
                self.logger.debug(LANG.WRAPPER_ELEMENT_FOUND_COUNT, len(elements))
                return elements
            if datetime.now() > expiration_time:
                return None
            sleep(0.2)
    def get_element(
            self,
            pathname: str,
            timeout: WaitSec,
            value: str | list[str] | None = None,
            replace_text: int | list[int] | None = None,
        ) -> WebElement:
        ''' Function to get a single WebElement '''
        elements = self.get_elements(pathname, timeout, replace_text)
        if not elements:
            raise ElementNotFoundError(
                LANG.WRAPPER_ELEMENT_NOT_FOUND.format(pathname=pathname))
        element = elements[0]
        if value:
            if isinstance(value, list):
                element.send_keys('\n'.join(value))
            if isinstance(value, (str, int)):
                element.click() # Set focus on input
                element.clear() # Clear value if already filled
                element.send_keys(str(value)) # Set new input value
            if isinstance(value, datetime):
                element.send_keys(value.strftime('%d/%m/%Y'))
        return element
    def select_option(
            self,
            pathname: str,
            timeout: WaitSec,
            value: str | int,
            use_value: bool = False,
            replace_text: int | list[int] | None = None,
        ) -> None:
        ''' Function to wrap change select element value '''
        # Try to interact to select element, if fail, try twice
        try:
            self.get_element(pathname, timeout, None, replace_text).click()
        except StaleElementReferenceException:
            self.get_element(pathname, timeout, None, replace_text).click()
        #
        element = self.get_element(pathname, timeout, None, replace_text)
        if use_value:
            Select(element).select_by_value(str(value))
        else:
            Select(element).select_by_visible_text(str(value))
    def select_radio(
            self,
            pathname: str,
            timeout: WaitSec,
            value: str | int | bool,
            replace_text: int | list[int] | None = None,
        ) -> None:
        ''' Function to wrap change radio element value

        value is not 0 base number, the first is 1
        '''
        radios = self.get_elements(pathname, timeout, replace_text)
        if radios is None:
            raise ElementNotFoundError(
                LANG.WRAPPER_ELEMENT_NOT_FOUND.format(pathname=pathname))
        if isinstance(value, str):
            for radio in radios:
                if radio.text == value:
                    radio.click()
        if isinstance(value, (int, bool)):
            radios[int(value) - 1].click()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
