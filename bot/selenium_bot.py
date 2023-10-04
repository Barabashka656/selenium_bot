import os
import time
import pickle
import logging

logger = logging.getLogger(__name__)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_driver() -> webdriver.Chrome:
    chrome_driver_path = os.path.join("bot", "data", "chromedriver", "chromedriver.exe")
    print(chrome_driver_path)
    service = Service(executable_path=chrome_driver_path)
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +\
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0'
    
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent}")
    return webdriver.Chrome(options=options, service=service)

def config_browser(driver: webdriver.Chrome):
    url = "https://epicloot.in/event#battle"
    cookies_path = os.path.join('bot', 'data', 'cookies')
    # driver.maximize_window()
    driver.get(url=url)
    for cookie in pickle.load(open(cookies_path, 'rb')):
        driver.add_cookie(cookie)
    driver.refresh()

def start_play(driver: webdriver.Chrome):
    prize_path = os.path.join('bot', 'data', 'prizes.txt') 
    while True:
        is_map_taken = True
        driver.refresh()
        while is_map_taken:
            time.sleep(10)
            try:
                take_map = driver.find_element(
                    by=By.CLASS_NAME,
                    value='game-gift__take'
                )
                take_map.click()
                is_map_taken = False
            except Exception: 
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
                        win_flag = False  
                        break
                except Exception as ex:
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
                    with open(prize_path, 'a', encoding='utf-8') as f:
                        f.write(prize.text + '\n')
                except Exception as ex:
                    print("last cell is mined")
                finally:
                    break
        time.sleep(1)
        driver.refresh()
        time.sleep(3602)