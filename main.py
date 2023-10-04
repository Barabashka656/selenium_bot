import logging

from bot.utils.my_logger import configure_logger
from bot.selenium_bot import (
    get_driver,
    config_browser,
    start_play
)

logger = logging.getLogger(__name__)

def main():
    configure_logger()
    driver = get_driver()
    config_browser(driver)
    start_play(driver)

if __name__ == '__main__':
    main()