# utils/attach.py
import os
import allure
from allure_commons.types import AttachmentType

# Скриншоты
def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')

# логи
def add_logs(browser):
    # работает только если драйвер поддерживает логи и включены prefs
    try:
        if hasattr(browser.driver, 'get_log'):
            logs = browser.driver.get_log('browser')  # может кинуть ошибку — ловим ниже
            text = '\n'.join(f"[{e.get('level')}] {e.get('message')}" for e in logs) if logs else ''
            if text.strip():
                allure.attach(text, 'browser_logs', AttachmentType.TEXT, '.log')
    except Exception:
        # просто молча пропускаем, чтобы teardown не падал
        pass

# html-код страницы
def add_html(browser):
    html = browser.driver.page_source
    allure.attach(html, 'page_source', AttachmentType.HTML, '.html')

def add_video(browser):
    # берём урл из env и добавляем basic-auth, если есть
    host = os.getenv('SELENOID_HOST', 'selenoid.autotests.cloud')
    user = os.getenv('SELENOID_USER', '')
    pwd  = os.getenv('SELENOID_PASS', '')
    auth = f'{user}:{pwd}@' if user and pwd else ''
    video_url = f'https://{auth}{host}/video/{browser.driver.session_id}.mp4'

    html = (
        "<html><body><video width='100%' height='100%' controls autoplay>"
        f"<source src='{video_url}' type='video/mp4'>"
        "</video></body></html>"
    )
    allure.attach(html, f'video_{browser.driver.session_id}', AttachmentType.HTML, '.html')