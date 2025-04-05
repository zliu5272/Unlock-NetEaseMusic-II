# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00861E7214136F7CB484EB6089CB7B5651F7C16923E2F9311583DCBC45C79AC84FD0F302DA0374F9C6D0B885D2639DD84C8EF14FBB08263FD37ACCBC5A4BD67007365E07E3C2FB100958EAC07754EB91AE2C96EECDDBD087CE31AED6BDB856EC9B8346A2CA66870244178234C0734C0DF069BAEDA3E17D3099DBCC5437DA3158E0BD2BFCA0F1738F10588D98D2877684B385395A8BD7FDD7B57103140A5FCA91E19292D9AC958C59756627FD8E59B7006F35A6C624ECA270F494AA70B344E607594B6301C47E187DDD919AC616B9D097FB85E3840934A111237EEFB34101ECC9B06352808A023DC23B8B38CAE184283549764969F3D51350540E5B588626AF5FB0583A8F74CBDB4DC894EC46C573A9A9501E06F425E5E453FE5F70DBA83C5E872EA7FBAAB760AE882412B5264AC54F368D36FEED76C9B523EB7A7A99705AB2DF76C36D2BB0F8D6214BF5E0593090A0B30B005CAE87CC25F4777992C700E2E041D8
"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
