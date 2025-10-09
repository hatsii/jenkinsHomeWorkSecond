# tests/conftest.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene.support.shared import browser
from utils import attach

@pytest.fixture(scope='function', autouse=True)
def set_browser():
    opts = Options()
    opts.set_capability('browserName', 'chrome')
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    opts.set_capability('browserVersion', '128.0')
    opts.set_capability('selenoid:options', {
        'enableVNC': True,
        'enableVideo': True,
    })

    hub = f"https://{os.getenv('SELENOID_USER','user1')}:{os.getenv('SELENOID_PASS','1234')}@selenoid.autotests.cloud/wd/hub"
    driver = webdriver.Remote(command_executor=hub, options=opts)
    browser.config.driver = driver

    browser.config.base_url = 'https://demoqa.com'
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.timeout = 10

    yield
    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_video(browser)
    browser.quit()
