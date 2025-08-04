import abc
import contextlib
import argparse

import selenium.webdriver.chrome.webdriver
from selenium import webdriver
import chromedriver_binary
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from shops_processing import shops_moscow


@contextlib.contextmanager
def browser_driver():
    browser = webdriver.Chrome()
    browser.implicitly_wait(2)
    browser.get("https://magnit.ru/shops?utm_source=magnit.ru&utm_campaign=navbar&utm_medium=shops")
    browser.fullscreen_window()
    yield browser
    browser.close()


class Shop:
    address: str
    browser: selenium.webdriver.chrome.webdriver.WebDriver
    def __init__(self, address: str):
        self.address = address

    def check_sku(self, unit: str) -> bool:
        search_cookie = browser.find_elements(By.CLASS_NAME,
                                              'pl-button-base.pl-button-base_size-s.pl-button-base_size-l-m.pl-button.pl-button_invert.popup-unit-cookie-policy__button')
        if len(search_cookie) != 0:
            search_cookie[0].click()
            search_map = browser.find_element(By.CSS_SELECTOR, '[data-test-id="map-button"]')
            search_map.click()
            search_choose = browser.find_elements(By.CSS_SELECTOR, '[data-test-id="v-button-base"]')
            # if (len(search_choose) > 1) and (search_choose[1].is_displayed()):
            #     search_choose[1].click()

        elif len(browser.find_elements(By.CSS_SELECTOR, '[data-test-id="v-top-navigation"]')) == 0:
            search_map = browser.find_element(By.CSS_SELECTOR, '[data-test-id="map-button"]')
            search_map.click()

        input_shop = browser.find_elements(By.CLASS_NAME, 'pl-input-field')
        input_shop[1].send_keys(self.address)
        print(self.address)  # temporary
        time.sleep(1)
        if len(browser.find_elements(By.CLASS_NAME, 'pl-empty-state.pl-shop-select-shop-list-empty')) != 0:
            print("shop not found")
            input_shop[1].send_keys(Keys.CONTROL + "a")
            input_shop[1].send_keys(Keys.DELETE)
            return False
        else:
            search_choose_shop = browser.find_elements(By.CLASS_NAME,
                                                       'pl-button-inline.pl-button-inline_primary.pl-button-inline_size-l')
            if (len(search_choose_shop) > 1) and (search_choose_shop[1].is_displayed()):
                search_choose_shop[1].click()
            else:
                print("retry for this shop")
                input_shop = browser.find_elements(By.CLASS_NAME, 'pl-input-field')
                if (len(input_shop) > 1) and (input_shop[1].is_displayed()):
                    input_shop[1].send_keys(Keys.CONTROL + "a")
                    input_shop[1].send_keys(Keys.DELETE)
                return False

            if len(search_cookie) != 0:
                input_unit = browser.find_element(By.CSS_SELECTOR, '[data-test-id="v-input-control"]')
                input_unit.send_keys(unit)
                input_unit.send_keys(Keys.ENTER)

            check_unit = browser.find_elements(By.CLASS_NAME, 'unit-catalog-product-preview-image')
            if len(check_unit) != 0:
                print("success")  # temporary
                return True
            else:
                print("fail")  # temporary
                return False


class ShopSet:
    browser: selenium.webdriver.chrome.webdriver.WebDriver

    def __init__(self, addresses: set):
        self.addresses = addresses

    def get_shop_list(self, unit: str) -> list[str]:
        shop_list = []
        for address in self.addresses:
            if Shop(address).check_sku(unit):
                shop_list.append(address)
        return shop_list

# class Printer(abc.ABC):
    # @abc.abstractmethod
    # def print(self) -> None:
        #raise NotImplementedError()


# class ConsolePrinter(Printer):

    #def print(self) -> None:
        #pass


def create_cli():
    parser = argparse.ArgumentParser(description="Getting info on the chosen products.")
    parser.add_argument("unit", help="The product you search for.")
    parser.add_argument("--printer", default="console", type=str, help="The printer.")
    parser.add_argument("--city", default="Moscow", type=str, help="The city of your search.")
    return parser.parse_args()


if __name__ == "main":
    with browser_driver() as browser:
        args = create_cli()
        found = ShopSet(shops_moscow).get_shop_list(args.unit)
        print("Found", len(found), "shops with that product")
        print("The addresses of the shops are:", *found, sep="\n")

