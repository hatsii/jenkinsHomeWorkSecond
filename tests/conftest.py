# tests/conftest.py
import os
import pytest
import allure
from allure_commons.types import AttachmentType

from selene import Browser, Config
from selenium.webdriver import Remote
from selenium.webdriver.remote.client_config import ClientConfig
from selenium.webdriver.chrome.options import Options
from utils import attach
from dotenv import load_dotenv

DEFAULT_BROWSER_VERSION = "100.0"


def pytest_addoption(parser):
    parser.addoption("--browser_version", default="128.0", help="Chrome version for Selenoid")
    parser.addoption(
        "--browser",
        help="Браузер, в котором будут тесты",
        choices=["chrome", "firefox"],
        default="chrome",
    )


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function")
def setup_browser(request):
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION

    options = Options()
    # capabilities for selenoid
    options.set_capability("browserName", "chrome")
    options.set_capability("browserVersion", browser_version)
    options.set_capability(
        "selenoid:options",
        {
            "enableVNC": True,
            "enableVideo": True,
        },
    )

    host = os.getenv("SELENOID_HOST", "selenoid.autotests.cloud")
    remote_url = f"https://{host}/wd/hub"

    cfg = ClientConfig(
        remote_server_addr=remote_url,
        username=os.getenv("LOGIN"),
        password=os.getenv("PASSWORD"),
    )

    driver = Remote(command_executor=remote_url, options=options, client_config=cfg)

    # debug info в Allure и консоль
    info = [
        f"executor: {remote_url}",
        f"session_id: {driver.session_id}",
        f"browserName: {driver.capabilities.get('browserName')}",
        f"browserVersion: {driver.capabilities.get('browserVersion')}",
        f"selenoid:options: {driver.capabilities.get('selenoid:options')}",
    ]
    allure.attach("\n".join(info), "driver_info", AttachmentType.TEXT, ".txt")
    print("\n".join(info))

    app = Browser(
        Config(
            driver=driver,
            base_url="https://demoqa.com",
            window_width=1080,
            window_height=1200,
            timeout=10,
        )
    )

    yield app

    # вложения в Allure (если падение — пригодится)
    attach.add_html(app)
    attach.add_screenshot(app)
    attach.add_logs(app)
    attach.add_video(app)
    app.quit()
