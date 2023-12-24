import logging

from bot.setup_bot import config_browser, get_driver
from bot.utils.my_logger import configure_root_logger
from bot.selenium_bot import (
    afk_play,
    farm_maps,
    start_play
)

logger = logging.getLogger(__name__)

def main():
    configure_root_logger()
    driver = get_driver()
    config_browser(driver)
    a = 1
    if a == 1:
        farm_maps(driver)
    elif a == 2:
        afk_play(driver)
        pass 
    elif a == 3:
        start_play(driver)


if __name__ == '__main__':
    main()
