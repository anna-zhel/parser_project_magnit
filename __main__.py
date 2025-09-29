import abc
import contextlib
import argparse
import numpy as np
import heapq
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


@contextlib.contextmanager
def browser_driver_prep():
    browser_prep = webdriver.Chrome()
    browser_prep.implicitly_wait(2)
    browser_prep.get("https://yandex.ru/maps/213/moscow/?ll=37.617700%2C55.755863&z=10")
    browser_prep.fullscreen_window()
    yield browser_prep
    browser_prep.close()


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
            print("shop not found")  # change to logger
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
                print("retry for this shop")  # to do: add for the first shop as well, change to logger
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


class ShopsDict:
    browser: selenium.webdriver.chrome.webdriver.WebDriver

    def __init__(self, addresses: list[str]):
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
        if len(result) == 0:
            print("Sorry, there are no shops with that product near your location. Try larger number of shops.")
        else:
            print(f"Found {len(result)} shop(s) with that product near your location, here are the addresses with prices:")
            for key, value in result.items():
                print(f"{key}: {value} руб")


# def get_all_shops() -> set[str]:
    # with open("shops_moscow.txt", "r", encoding='utf-8') as file:
        # return set([shop.strip() for shop in file.readlines()])

def get_shops(location: str, k: int) -> list[str]:
    area = browser_prep.find_element(By.CLASS_NAME, "input__control._bold")
    area.send_keys(location)
    area.send_keys(Keys.ENTER)
    time.sleep(1)
    x, y = browser_prep.find_element(By.CLASS_NAME, "toponym-card-title-view__coords-badge").text.split(', ')
    coord_loc = np.array([float(x), float(y)])
    with open("shops_moscow_coords.txt", "r", encoding='utf-8') as p_file:
        maxheap = []
        for line in p_file.readlines():
            a, zq = line.strip().split(' -- ')
            z, q = zq.strip('[]').split(', ')
            point = np.array([float(z), float(q)])
            distance = np.linalg.norm(coord_loc - point)
            if len(maxheap) < k:
                heapq.heappush(maxheap, (-distance, a))
            else:
                if -distance > maxheap[0][0]:
                    heapq.heappop(maxheap)
                    heapq.heappush(maxheap, (-distance, a))
    return [element[1] for element in maxheap]


def create_cli():
    parser = argparse.ArgumentParser(description="Getting info on the chosen products.")
    parser.add_argument("location", default="г. Москва, улица Новый Арбат", type=str, help="Your approximate location.")
    parser.add_argument("k", default=50, type=int, help="The number of closest shops to search.")
    parser.add_argument("unit", type=str, help="The product you search for.")
    parser.add_argument("--printer", default="console", type=str, help="The printer.")
    parser.add_argument("--city", default="Moscow", type=str, help="The city of your search.")
    return parser.parse_args()


with browser_driver_prep() as browser_prep:
    start = time.time()  # change to logger
    args = create_cli()
    search_shops_list = get_shops(args.location, args.k)
with browser_driver() as browser:
    found = ShopsDict(search_shops_list).get_shop_dict(args.unit)
    cprinter = ConsolePrinter()
    cprinter.display(found)
    print("Execution time in seconds:", time.time() - start)  # change to logger
