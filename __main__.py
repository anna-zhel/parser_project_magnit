import abc
import contextlib
import argparse

import selenium.webdriver.chrome.webdriver
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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

    def check_sku(self, unit: str) -> float:
        search_cookie = browser.find_elements(By.CLASS_NAME,
                                              'pl-button-base.pl-button-base_size-s.pl-button-base_size-l-m.pl-button.pl-button_invert.popup-unit-cookie-policy__button')
        if len(search_cookie) != 0:
            search_cookie[0].click()
            search_map = browser.find_element(By.CSS_SELECTOR, '[data-test-id="map-button"]')
            search_map.click()
            search_choose = browser.find_elements(By.CSS_SELECTOR, '[data-test-id="v-button-base"]')
            if (len(search_choose) > 1) and (search_choose[1].is_displayed()):
                search_choose[1].click()
            input_shop = browser.find_elements(By.CLASS_NAME, 'pl-input-field')
            input_shop[2].send_keys(self.address)
            # check = browser.find_elements(By.CSS_SELECTOR, '[data-test-id="v-chip-control"]')
            # check[1].click()

        elif len(browser.find_elements(By.CSS_SELECTOR, '[data-test-id="v-top-navigation"]')) == 0:
            search_map = browser.find_element(By.CSS_SELECTOR, '[data-test-id="map-button"]')
            search_map.click()

        if len(search_cookie) == 0:
            input_shop = browser.find_elements(By.CLASS_NAME, 'pl-input-field')
            input_shop[1].send_keys(self.address)
        print(self.address)  # temporary
        time.sleep(1)
        if len(browser.find_elements(By.CLASS_NAME, 'pl-empty-state.pl-shop-select-shop-list-empty')) != 0:
            print("shop not found")
            if len(search_cookie) == 0:
                input_shop[1].send_keys(Keys.CONTROL + "a")
                input_shop[1].send_keys(Keys.DELETE)
            else:
                input_shop[2].send_keys(Keys.CONTROL + "a")
                input_shop[2].send_keys(Keys.DELETE)
            return -1.0
        else:
            search_choose_shop = browser.find_elements(By.CLASS_NAME,
                                                       'pl-button-inline.pl-button-inline_primary.pl-button-inline_size-l')
            if (len(search_choose_shop) > 1) and (search_choose_shop[1].is_displayed()):
                search_choose_shop[1].click()
            else:
                print("retry for this shop")  # to do: add for the first shop as well
                input_shop = browser.find_elements(By.CLASS_NAME, 'pl-input-field')
                if (len(input_shop) > 1) and (input_shop[1].is_displayed()):
                    input_shop[1].send_keys(Keys.CONTROL + "a")
                    input_shop[1].send_keys(Keys.DELETE)
                return -1.0

            if len(search_cookie) != 0:
                input_unit = browser.find_element(By.CSS_SELECTOR, '[data-test-id="v-input-control"]')
                input_unit.send_keys(unit)
                input_unit.send_keys(Keys.ENTER)

            check_unit = browser.find_elements(By.CLASS_NAME, 'unit-catalog-product-preview-image')
            if len(check_unit) != 0:
                print("success")  # temporary
                price = browser.find_element(By.CLASS_NAME, 'pl-text.unit-catalog-product-preview-prices__regular')
                return float(price.text[:-1])
            else:
                print("fail")  # temporary
                return -1.0


class ShopSet:
    browser: selenium.webdriver.chrome.webdriver.WebDriver

    def __init__(self, addresses: set):
        self.addresses = addresses

    def get_shop_dict(self, unit: str) -> dict[str, float]:
        shop_dict = {}
        for address in self.addresses:
            price = Shop(address).check_sku(unit)
            if price >= 0:
                shop_dict[address] = price
        return shop_dict


class Printer(abc.ABC):
    @abc.abstractmethod
    def display(self, result: dict[str, float]) -> None:
        raise NotImplementedError()


class ConsolePrinter(Printer):

    def display(self, result: dict[str, float]) -> None:
        print(f"Found {len(result)} shops with that product, here are the addresses with prices:")
        for key, value in result.items():
            print(f"{key}: {value} руб")


def get_all_shops() -> set[str]:
    with open("shops_moscow.txt", "r", encoding='utf-8') as file:
        return set([shop.strip() for shop in file.readlines()])


def create_cli():
    parser = argparse.ArgumentParser(description="Getting info on the chosen products.")
    parser.add_argument("unit", help="The product you search for.")
    parser.add_argument("--printer", default="console", type=str, help="The printer.")
    parser.add_argument("--city", default="Moscow", type=str, help="The city of your search.")
    return parser.parse_args()


with browser_driver() as browser:
    start = time.time()
    args = create_cli()
    shops_moscow = get_all_shops()
    found = ShopSet(shops_moscow).get_shop_dict(args.unit)
    cprinter = ConsolePrinter()
    cprinter.display(found)
    print("Execution time in seconds:", time.time() - start)
