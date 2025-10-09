# tests/conftest.py
import os
import pytest
import allure
from allure_commons.types import AttachmentType

from selene import Browser, Config
from selenium.webdriver import Remote, ChromeOptions, FirefoxOptions
from selenium.webdriver.remote.client_config import ClientConfig
from utils import attach


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        help="Браузер, в котором будут тесты",
        choices=["chrome", "firefox"],
        default="chrome",
    )


@pytest.fixture(scope='function')
def app(request):
    browser_name = request.config.getoption("--browser")

    # --- опции под выбранный браузер ---
    if browser_name == "chrome":
        opts = ChromeOptions()
        # консольные логи есть только у Chrome через goog:loggingPrefs
        opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    else:
        opts = FirefoxOptions()
        # для Firefox не трогаем goog:loggingPrefs

    opts.set_capability('browserName', browser_name)

    # версию лучше не пинить. Если нужно — задавай через ENV:
    version_env = os.getenv('BROWSER_VERSION')
    if version_env:
        opts.set_capability('browserVersion', version_env)

    opts.set_capability('acceptInsecureCerts', True)
    opts.set_capability('selenoid:options', {
        'enableVNC': True,
        'enableVideo': True,
        'name': f'test_session_{browser_name}',
    })

    host = os.getenv('SELENOID_HOST', 'selenoid.autotests.cloud')
    remote_url = f'https://{host}/wd/hub'

    cfg = ClientConfig(
        remote_server_addr=remote_url,
        username=os.getenv('SELENOID_USER', 'user1'),
        password=os.getenv('SELENOID_PASS', '1234'),
    )

    driver = Remote(command_executor=remote_url, options=opts, client_config=cfg)

    # Маячок
    info = [
        f"executor: {remote_url}",
        f"session_id: {driver.session_id}",
        f"browserName: {driver.capabilities.get('browserName')}",
        f"browserVersion: {driver.capabilities.get('browserVersion')}",
        f"selenoid:options: {driver.capabilities.get('selenoid:options')}",
    ]
    allure.attach("\n".join(info), "driver_info", AttachmentType.TEXT, ".txt")
    print("\n".join(info))

    app = Browser(Config(
        driver=driver,
        base_url='https://demoqa.com',
        window_width=1080,
        window_height=1200,
        timeout=10,
    ))

    yield app

    attach.add_html(app)
    attach.add_screenshot(app)
    attach.add_logs(app)
    attach.add_video(app)
    app.quit()
