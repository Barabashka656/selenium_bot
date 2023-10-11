import os
import time
import pickle
import logging

from bot.utils.my_logger import setup_attempts_logger

logger = logging.getLogger(__name__)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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

def config_browser(driver: webdriver.Chrome):
    logging.info('the browser is being configured...')
    cookies_path = os.path.join('bot', 'data', 'cookies')
    try:
        for cookie in pickle.load(open(cookies_path, 'rb')):
            driver.add_cookie(cookie)
    except Exception as e:
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
    

def start_play(driver: webdriver.Chrome):
    attempts_logger = setup_attempts_logger()
    logging.info('running driver')
    prize_path = os.path.join('bot', 'data', 'prizes.txt') 
    logging.info('start abuse')
    while True:
        attempts_value = driver.find_element(
            by=By.XPATH,
            value='//*[@id="battle"]/div/div[5]/div/div[1]/div[2]/div[1]/div[2]/span'
        )
        if int(attempts_value.text):
            is_map_taken = False
            driver.refresh()
            time.sleep(4)
        else:
            is_map_taken = True
            driver.refresh()
        scroll_down = driver.find_element(
            by=By.XPATH,
            value='//*[@id="battle"]/div/div[5]/div/ul/li[1]/p'
        )
        actions = ActionChains(driver)
        actions.move_to_element(scroll_down)
        actions.perform()

        while is_map_taken:
            logging.info('trying to get a ticket')
            time.sleep(10)
            try:
                take_map = driver.find_element(
                    by=By.CLASS_NAME,
                    value='game-gift__take'
                )
               
                take_map.click()
                logging.info('ticket taken successfully')
                is_map_taken = False
            except Exception:
                logging.info('ticket taking failed')
                pass
        play_btn = WebDriverWait(driver, 7).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "game-actions__btn"))
        )
        play_btn = driver.find_element(
            by=By.CLASS_NAME,
            value='game-actions__btn'
        )
        play_btn.click()
        hp_value = 4
        for _ in range(4):
            win_flag = True
            for i in range(2, 6):
                try:
                    time.sleep(2)
                    cell_btn = driver.find_element(
                        by=By.XPATH,
                        value='//*[@id="battle"]/div/div[5]/div/div[1]/div[1]' +\
                             f'/div[2]/div[3]/div[{i}]/div[1]'
                    )
                    cell_btn.click()
                    time.sleep(2)
                    parent_div_hp = driver.find_element(
                        By.XPATH,
                        value='//*[@id="battle"]/div/div[5]/div/div[1]/div[4]/div[1]/div'
                    )
                    divs = parent_div_hp.find_elements(
                        by=By.TAG_NAME,
                        value="div"
                    )
                    current_hp = 4
                    for div in divs:
                        if div.get_attribute('class') == 'game-lives__item disabled':
                            current_hp-=1
                    if current_hp < hp_value:
                        hp_value-=1
                        logging.info(f'hp value changed to {hp_value}')
                        win_flag = False  
                        break
                except Exception as ex:
                    logging.info(f'hp are over')
                    attempts_logger.info(f'hp are over')
                    win_flag = False    
                    break 

            if win_flag:
                try:
                    time.sleep(2)
                    win_btn = driver.find_element(
                        by=By.XPATH,
                        value='//*[@id="battle"]/div/div[5]/div/div[1]' +\
                              '/div[1]/div[2]/div[3]/div[6]/div'
                    )
                    win_btn.click()
                    prize_info_tuple = (
                        By.XPATH,
                        '//*[@id="battle"]/div/div[4]/div[2]/div/div[2]'
                    )
                    play_btn = WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located(prize_info_tuple)
                    )
                    prize = driver.find_element(
                        *prize_info_tuple
                    )
                    
                    logging.info(f'prize: {prize.text}')
                    attempts_logger.info(f'prize: {prize.text}')
                    with open(prize_path, 'a', encoding='utf-8') as f:
                        f.write(prize.text + '\n')
                except Exception as ex:
                    logging.info('last cell was mined')
                    attempts_logger.info('last cell was mined')
                finally:
                    break
        logging.info('start waiting 1 hour')
        time.sleep(1)
        driver.refresh()
        time.sleep(3602)

def update_cookies(driver: webdriver.Chrome):
    cookies_path = os.path.join('bot', 'data', 'cookies')
    steam_auth_url_path = os.path.join('bot', 'data', 'steam_auth_url.txt')
    with open(steam_auth_url_path, 'r') as f:
        steam_auth_url = f.read()
    driver.get(url=steam_auth_url)
    time.sleep(50)
    pickle.dump(driver.get_cookies(), open(cookies_path, 'wb'))
