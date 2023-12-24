import logging
import os
import pickle
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


logger = logging.getLogger(__name__)

def get_driver() -> webdriver.Chrome:
    logging.info("the driver starts...")
    chrome_driver_path = os.path.join("bot", "data", "chromedriver", "chromedriver.exe")
    service = Service(executable_path=chrome_driver_path)
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +\
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0'
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent}")
    #options.add_argument("--headless")
    options.add_argument("--window-size=1050,750")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options, service=service)
    #driver.maximize_window()
    url = "https://epicloot.in/event#battle"
    driver.get(url=url)
    logging.info('driver is created')
    return driver

def config_browser(driver: webdriver.Chrome) -> None:
    logging.info('the browser is being configured...')
    cookies_path = os.path.join('bot', 'data', 'cookies')
    try:
        for cookie in pickle.load(open(cookies_path, 'rb')):
            driver.add_cookie(cookie)
    except Exception:
        pass
    logging.info('cookies downloaded successfully')
    driver.refresh()
    logging.info('cheking cookies...')
    try:
        driver.find_element(
            by=By.CLASS_NAME,
            value='js-user-balance-coins'
        )
    except Exception:
        logging.info('cookies are out of date')
        update_cookies(driver)
    logging.info('cookies are ok')

def update_cookies(driver: webdriver.Chrome) -> None:
    cookies_path = os.path.join('bot', 'data', 'cookies')
    steam_auth_url_path = os.path.join('bot', 'data', 'steam_auth_url.txt')
    with open(steam_auth_url_path, 'r') as f:
        steam_auth_url = f.read()
    driver.get(url=steam_auth_url)
    time.sleep(50)
    pickle.dump(driver.get_cookies(), open(cookies_path, 'wb'))
