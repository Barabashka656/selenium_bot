import time
import logging

from bot.modules import (
    click_play_btn,
    get_ticket,
    walk_until_death,
    scroll_to_kunka
)
from bot.utils.my_logger import setup_attempts_logger

from selenium import webdriver
from selenium.webdriver.common.by import By


def farm_maps(driver: webdriver.Chrome) -> None:
    logging.info('start farm')
    while True:
        driver.refresh()
        scroll_to_kunka(driver)
        get_ticket(driver, True)

        logging.info('start waiting 1 hour')
        time.sleep(1)
        driver.refresh()
        time.sleep(3602)

def afk_play(driver: webdriver.Chrome) -> None:
    attempts_logger = setup_attempts_logger()
    logging.info('start afk play')
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
            print("DONE")
            time.sleep(3000)
            return 
        
        scroll_to_kunka(driver)
        get_ticket(driver, is_map_taken)
        click_play_btn(driver)
        walk_until_death(driver, attempts_logger)
        time.sleep(1)
        driver.refresh()
        time.sleep(3)

def start_play(driver: webdriver.Chrome) -> None:
    attempts_logger = setup_attempts_logger()
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
        
        scroll_to_kunka(driver)
        get_ticket(driver, is_map_taken)
        click_play_btn(driver)
        walk_until_death(driver, attempts_logger)
        logging.info('start waiting 1 hour')
        time.sleep(1)
        driver.refresh()
        time.sleep(3602)
