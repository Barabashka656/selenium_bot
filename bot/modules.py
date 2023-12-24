import os
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def scroll_to_kunka(driver: webdriver.Chrome) -> None:
    scroll_down = driver.find_element(
        by=By.XPATH,
        value='//*[@id="battle"]/div/div[5]/div/ul/li[1]/p'
    )
    actions = ActionChains(driver)
    actions.move_to_element(scroll_down)
    actions.perform()

def get_ticket(driver: webdriver.Chrome, is_map_taken: bool) -> None:
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


def take_prize(driver: webdriver.Chrome, attempts_logger: logging.Logger) -> None:
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
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(prize_info_tuple)
        )
        prize = driver.find_element(
            *prize_info_tuple
        )
        
        logging.info(f'prize: {prize.text}')
        attempts_logger.info(f'prize: {prize.text}')

        prize_path = os.path.join('bot', 'data', 'prizes.txt') 
        with open(prize_path, 'a', encoding='utf-8') as f:
            f.write(prize.text + '\n')
    except Exception:
        logging.info('last cell was mined')
        attempts_logger.info('last cell was mined')
        
def walk_until_death(driver: webdriver.Chrome, attempts_logger: logging.Logger) -> None:
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
            except Exception:
                logging.info(f'hp are over')
                attempts_logger.info(f'hp are over')
                win_flag = False    
                break 

        if win_flag:
            take_prize(driver, attempts_logger)
            break

def click_play_btn(driver: webdriver.Chrome) -> None:
    play_btn = WebDriverWait(driver, 7).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "game-actions__btn"))
    )
    play_btn = driver.find_element(
        by=By.CLASS_NAME,
        value='game-actions__btn'
    )
    play_btn.click()