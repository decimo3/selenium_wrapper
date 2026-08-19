# selenium_wrapper

A lightweight Selenium helper for browser automation with Chrome/Chromedriver, built around a `path.ini` configuration file and a small wrapper API for locating page elements reliably.

The project is designed to simplify common web-automation tasks such as:

- opening a predefined website
- finding page elements by an easy path convention
- waiting for elements to become available
- filling inputs and selecting options
- selecting radio buttons
- automatically checking for the right ChromeDriver version

## Features

- Simple wrapper around Selenium WebDriver
- Easy element access using path aliases from `path.ini`
- Built-in waits via `WaitSec`
- Automatic ChromeDriver update check
- Browser and residual process cleanup helpers
- Support for custom exceptions and clear error handling

## Requirements

- Python 3.10+
- Google Chrome installed
- Windows support is the main target for the included driver management logic
- Selenium, python-dotenv and requests are installed via the package dependencies

## Installation

Download and install from the *.whl file:

```bash
pip install selenium_wrapper-*.whl
```

Or install directly from GIT:

```bash
pip install git+https://github.com/decimo3/selenium_wrapper.git
```

## Project layout

```text
src/
  selenium_wrapper/
    __init__.py
    wrapper.py
    executioner.py
    driver_updater.py
    terminator.py
    multilang.py
    exceptions.py
    chrome_info.py
    version.py
    resources/
      pt-BR.lang
```

## Configuration

Create a `path.ini` file in your project root or pass a custom path to `Wrapper(paths_file=...)`.

Example:

```ini
[DEFAULT]
GOOGLE_CHROME=C:\Program Files\Google\Chrome\Application\chrome.exe

[APP]
HOME=https://example.com
LOGIN_FORM=#login-form
USERNAME=#username
PASSWORD=#password
SUBMIT_BUTTON=.submit-btn
```

The wrapper interprets selectors as follows:

- `#value` → `By.ID`
- `/value` → `By.XPATH`
- `.value` → `By.CLASS_NAME`

This means a config entry like:

```ini
LOGIN_BUTTON=.login-button
```

will resolve to a class-name lookup for `login-button`.

## Basic usage

```python
from selenium_wrapper import Wrapper, WaitSec

with Wrapper('HOME') as browser:
    browser.get_element('USERNAME', WaitSec.MED, 'myuser@example.com')
    browser.get_element('PASSWORD', WaitSec.MED, 'secretpass')
    browser.get_element('SUBMIT_BUTTON', WaitSec.MED).click()
```

## Available API

### `Wrapper`

```python
Wrapper(website_path: str, paths_file: str | Path | None = None)
```

Initializes the browser and loads the website configured under the given section key.

Example:

```python
browser = Wrapper('HOME')
```

### `WaitSec`

```python
from selenium_wrapper import WaitSec
```

Available wait values:

- `WaitSec.NOW` = 0s
- `WaitSec.SHORT` = 3s
- `WaitSec.MED` = 7s
- `WaitSec.LONG` = 15s
- `WaitSec.MAX` = 30s

### Element lookup

```python
browser.get_element(pathname: str, timeout: WaitSec, value: str | list[str] | None = None, replace_text: int | list[int] | None = None)
```

Gets the first matching element and optionally fills it.

```python
# fill input
browser.get_element('USERNAME', WaitSec.MED, 'myuser')

# fill a field from a list of values
browser.get_element('NOTES', WaitSec.MED, ['first line', 'second line'])
```

### List of elements

```python
browser.get_elements(pathname: str, timeout: WaitSec = WaitSec.NOW, replace_text: int | list[int] | None = None)
```

Returns all matched elements when available.

### Select dropdown

```python
browser.select_option(
    'COUNTRY',
    WaitSec.MED,
    'Brazil',
    use_value=False,
)
```

Or by option value:

```python
browser.select_option('COUNTRY', WaitSec.MED, 'BR', use_value=True)
```

### Radio buttons

```python
browser.select_radio('GENDER', WaitSec.MED, 'Male')
```

This matches by the radio label text. Numeric values are also supported, based on the order returned by the selector.

## Example: full flow

```python
from selenium_wrapper import Wrapper, WaitSec

with Wrapper('HOME', paths_file='path.ini') as browser:
    browser.get_element('USERNAME', WaitSec.MED, 'demo_user')
    browser.get_element('PASSWORD', WaitSec.MED, 'demo_pass')
    browser.get_element('LOGIN_BUTTON', WaitSec.MED).click()

    # optional select
    browser.select_option('COUNTRY', WaitSec.MED, 'Brazil')

    # optional radio selection
    browser.select_radio('GENDER', WaitSec.MED, 'Female')
```

## Execution helper

The package also includes a small command execution utility:

```python
from selenium_wrapper.executioner import execute

output = execute('echo', 'hello')
print(output)
```

This helper runs a process and returns the command output as a string. It raises `FileNotFoundError` for missing programs and `SubprocessError` for invalid execution failures.

## Error handling

Custom exceptions include:

- `ElementNotFoundError`
- `PathNotFoundError`
- `InvalidPathTypeError`
- `CouldNotDetermineInstances`
- `MultiplesInstancesException`
- `VersionNotFound`
- `CannotDownloadUpdate`

## Notes

- The wrapper expects Chrome to be present and compatible with the installed ChromeDriver.
- The project includes an automatic ChromeDriver version check/update flow when the wrapper starts.
- Browser state is initialized with a temporary directory and app-mode launch using `--app=<site>`.

## Running tests

```bash
pytest
```

The repository includes a small test suite covering the execution helper and expected error behavior.

## License

This project is distributed under the MIT license.
