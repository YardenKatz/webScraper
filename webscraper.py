'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidElementStateException, NoSuchElementException, TimeoutException
from seleniumbase import BaseCase, SB
from services.config_service import ConfigService
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class WebScraperException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class WebScraper(BaseCase):
    """
       Scrapes Websites.

       :param int target_index: refers to index of target in config.ini. Update config.ini with target data
       [string] items: list of item codes to search
    """

    def __init__(self, target_index, items, headless_mode=True, is_test_env=False):
        super().__init__()  # Call SeleniumBase init for tests

        self.config_service = ConfigService('config.ini')
        self.config_service.read_config()
        targets = self.config_service.get_targets()

        self.base_url = self.config_service.get_data(targets[target_index], 'url')
        self.username = self.config_service.get_data(targets[target_index], 'username')
        self.pwd = self.config_service.get_data(targets[target_index], 'pwd')

        self.items = items
        self.headless_mode = headless_mode
        self.is_test_env = is_test_env
        if not self.is_test_env:
            # Initialize ChromeDriver with WebDriverManager
            options = webdriver.ChromeOptions()
            if self.headless_mode:
                options.add_argument("--headless")
            self.driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                                           options=options)
        else:
            self.driver = None  # Handled by SeleniumBase in test mode



    def setUp(self):
        """Initialize SeleniumBase's driver."""
        if self.is_test_env:
            super().setUp()  # Let pytest handle initialization in test mode

    def tearDown(self):
        """Clean up the driver."""
        if self.is_test_env:
            super().tearDown()  # Let pytest handle teardown in test mode
        else:
            self.driver.quit()  # Manually quit in standalone mode

    # Helper methods to use SeleniumBase methods in standalone mode
    def open(self, url):
        if self.is_test_env:
            super().open(url)
        else:
            self.driver.get(url)

    def type(self, selector, text, clear_before=True, wait_time=15):
        """
        Types text into an input field.

        Args:
            selector (str): The CSS selector of the input field.
            text (str): The text to type into the field.
            clear_before (bool): Whether to clear the field before typing. Default is True.
            wait_time (int): How long to wait for the element to become interactable. Default is 15 seconds.
        """
        if self.is_test_env:
            super().type(selector, text)
        else:
            try:
                # Wait for the element to be visible and enabled
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                # Clear the field if required
                if clear_before:
                    try:
                        element.clear()
                    except InvalidElementStateException:
                        print(f"Cannot clear element {selector}. Proceeding to type.")
                element.send_keys(text)
            except (TimeoutException, NoSuchElementException):
                print(f"Element not found or not interactable: {selector}")
                raise WebScraperException(f"Element not found or not interactable: {selector}")

    def click(self, selector, wait_time=15):
        """
        Clicks an element.

        Args:
            selector (str): The CSS selector of the element to click.
            wait_time (int): How long to wait for the element to become clickable. Default is 15 seconds.
        """
        if self.is_test_env:
            super().click(selector)
        else:
            try:
                # Wait for the element to be clickable
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                element.click()
            except (TimeoutException, NoSuchElementException):
                print(f"Element not found or not clickable: {selector}")
                raise WebScraperException(f"Element not found or not clickable: {selector}")

    def get_text(self, selector, wait_time=60):
        """
        Retrieves the text of an element.

        Args:
            selector (str): The CSS selector of the element to get text from.
            wait_time (int): How long to wait for the element to become visible. Default is 60 seconds.

        Returns:
            str: The text of the element.
        """
        if self.is_test_env:
            return super().get_text(selector)
        else:
            try:
                # Wait for the element to be visible
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                )
                return element.text
            except (TimeoutException, NoSuchElementException):
                print(f"Element not found or not visible: {selector}")
                raise WebScraperException(f"Element not found or not visible: {selector}")

    def login(self):
        raise NotImplementedError("Subclasses should implement this method")

    def search_item(self, item_code):
        raise NotImplementedError("Subclasses should implement this method")

    def scrape_results(self) -> (str, str, str):
        raise NotImplementedError("Subclasses should implement this method")

    def handle_results(self, results):
        print(results)

    def start(self):
        self.setUp()
        try:
            self.login()
            for item in self.items:
                self.search_item(item)
                results = self.scrape_results()
                self.handle_results(results)
        finally:
            self.tearDown()

'''

from seleniumbase import SB  # Import SB context manager from SeleniumBase
from services.config_service import ConfigService
# from selenium.common.exceptions import NoSuchElementException, TimeoutException


class WebScraperException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class WebScraper:
    """
    Scrapes Websites.

    :param int target_index: refers to index of target in config.ini. Update config.ini with target data
    :param list items: list of item codes to search
    """

    def __init__(self, target_index, items, headless_mode=True, is_test_env=False):
        self.config_service = ConfigService('config.ini')
        self.config_service.read_config()
        targets = self.config_service.get_targets()

        self.base_url = self.config_service.get_data(targets[target_index], 'url')
        self.username = self.config_service.get_data(targets[target_index], 'username')
        self.pwd = self.config_service.get_data(targets[target_index], 'pwd')

        self.items = items
        self.headless_mode = headless_mode
        self.is_test_env = is_test_env

        if not self.is_test_env:
            # Initialize SB context manager for standalone mode
            self.sb = SB(headless=headless_mode)
        else:
            self.sb = None  # SB instance handled by SeleniumBase in test mode

    def start(self):
        if not self.is_test_env:
            with self.sb as sb:
                self._execute_standalone_mode(sb)
        else:
            self._execute_test_mode()

    def _execute_standalone_mode(self, sb):
        """Executes the scraping steps in standalone mode."""
        try:
            self.login(sb)
            for item in self.items:
                self.search_item(sb, item)
                results = self.scrape_results(sb)
                self.handle_results(results)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.sb.quit()

    def _execute_test_mode(self):
        """Executes the scraping steps in test mode, assuming sb is passed in tests."""
        self.login(self.sb)
        for item in self.items:
            self.search_item(self.sb, item)
            results = self.scrape_results(self.sb)
            self.handle_results(results)

    def login(self, sb):
        raise NotImplementedError("Subclasses should implement this method")

    def search_item(self, sb, item_code):
        raise NotImplementedError("Subclasses should implement this method")

    def scrape_results(self, sb):
        raise NotImplementedError("Subclasses should implement this method")

    def handle_results(self, results):
        print(results)


class MusicCenterScraper(WebScraper):

    def __init__(self, items, headless_mode=True, is_test_env=False):
        super().__init__(0, items, headless_mode, is_test_env)
        self.is_first_search = True

    def start(self):
        """Unified start method for both test mode and standalone mode."""
        if self.is_test_env:
            driver = self  # In test mode, 'self' is the SeleniumBase instance
            self.setUp()
            try:
                self.run_scraper(driver)
            finally:
                self.tearDown()  # Clean up for test mode
        else:
            with SB(headless=self.headless_mode) as driver:  # In standalone mode, use the SB instance
                self.run_scraper(driver)

    def run_scraper(self, driver):
        """Main scraping logic that handles login, search, and results scraping."""
        try:
            self.login(driver)
            for item in self.items:
                self.search_item(driver, item)
                driver.sleep(2)
                results = self.scrape_results(driver)
                self.handle_results(results)
        except Exception as e:
            print(f"An error occurred: {e}")

    def login(self, driver):
        """Login method (handles both modes with a unified driver)."""
        login_endpoint = '/system/login'
        driver.open(self.base_url + login_endpoint)
        driver.type("input[type='text'][role='textbox']", self.username)
        driver.type("input[type='password']", self.pwd)
        driver.click("dx-button[aria-label='כניסה למערכת']")

    def search_item(self, driver, item_code):
        """Search item method (handles both modes with a unified driver)."""
        if self.is_first_search:
            driver.click("dx-button[aria-label='התחל הזמנה']")
            self.is_first_search = False
        driver.type("input.dx-texteditor-input", item_code)

    def scrape_results(self, driver):
        """Scrape results method (handles both modes with a unified driver)."""
        try:
            stock_status = driver.get_text("div[class*='stock-custom-text']")
            trader_price = driver.get_text(".price")
            driver.click(".alternative-price")
            consumer_price = driver.get_text(".price")
            return stock_status, trader_price, consumer_price
        except Exception:
            # Return placeholder values if item is not found
            print("Item not found: stock status could not be retrieved.")
            return "N/A", "N/A", "N/A"


# Usage example

'''
class MusicCenterScraper(WebScraper):

    def __init__(self, items, headless_mode=True, is_test_env=False):
        super().__init__(0, items, headless_mode, is_test_env)
        self.is_first_search = True

    def login(self):
        try:
            login_endpoint = '/system/login'
            self.open(self.base_url + login_endpoint)
            self.type("input[type='text'][role='textbox']", self.username)
            self.type("input[type='password']", self.pwd)
            self.click("dx-button[aria-label='כניסה למערכת']")
        except (NoSuchElementException, TimeoutException):
            raise WebScraperException("Login failed: Incorrect credentials or element not found\n")

    def search_item(self, item_code):
        try:
            if self.is_first_search:
                self.click("dx-button[aria-label='התחל הזמנה']")
                self.is_first_search = False

            self.type("input.dx-texteditor-input", item_code)
        except NoSuchElementException:
            raise WebScraperException("Search failed. Search field not found")

    def scrape_results(self) -> (str, str, str):
        self.wait(2)
        try:
            stock_status = self.get_text("div[class*='stock-custom-text']")
            trader_price = self.get_text(".price")
            self.click(".alternative-price")
            consumer_price = self.get_text(".price")

            return stock_status, trader_price, consumer_price
        except NoSuchElementException:
            raise WebScraperException("Scraping results failed: Element not found")


class ArtStudioScraper(WebScraper):
    def __init__(self, items, headless_mode=True, is_test_env=False):
        super().__init__(1, items, headless_mode, is_test_env)

    # def init_driver(self):
    #     return SBDriver(uc=True, headless=self.headless_mode)

    def login(self):
        try:
            # self.driver.get(self.base_url + '?route=account/login')
            # self.driver.implicitly_wait(5)

            self.open(self.base_url + '?route=account/login')

            # login_field = self.driver.find_element(By.CSS_SELECTOR, "#input-email") pwd_field =
            # self.driver.find_element(By.CSS_SELECTOR, '#input-pwd') submit_btn = self.driver.find_element(
            # By.CSS_SELECTOR, '#content > div > div:nth-child(2) > div > form > div.buttons > div > button')
            #
            # login_field.send_keys(self.username)
            # pwd_field.send_keys(self.pwd)
            # submit_btn.send_keys(Keys.RETURN)

            # self.driver.type("#input-email", self.username)
            # self.driver.type("#input-password", self.pwd)
            # self.driver.click('#content > div > div:nth-child(2) > div > form > div.buttons > div > button')
            self.type("#input-email", self.username)
            self.type("#input-password", self.pwd)
            self.click('#content > div > div:nth-child(2) > div > form > div.buttons > div > button')

            # Check if login was successful by looking for a known element on the home page
            # WebDriverWait(self.driver, 4).until(
            #     EC.presence_of_element_located((By.XPATH, "//span[@class='links-text' and text()='החשבון שלי']"))
            # )
            # self.driver.assert_element("//span[@class='links-text' and text()='החשבון שלי']")
            # self.driver.assert_text("החשבון שלי")
            # self.assert_text("החשבון שלי")



        except Exception:
            raise

    def search_item(self, item_code):
        # search_field = self.driver.find_element(By.XPATH, '// *[ @ id = "search"] / div / div / span / input[2]')
        # search_field.clear()
        # search_field.send_keys(item_code)


        self.type('input[name="search"]', item_code)
        try:
            # wait = WebDriverWait(self.driver, 3)  # wait for up to 3 seconds
            # element = wait.until(
            #     ec.presence_of_element_located((By.CSS_SELECTOR, "div.search-result.tt-suggestion.tt-selectable"))
            # )
            # self.assert_element_present("div.search-result.tt-suggestion.tt-selectable")
            # Find the link within the element
            # link = element.find_element(By.TAG_NAME, "a")
            # link.click()
            element = "div.search-result.tt-suggestion.tt-selectable > a"
            sb.wait_for_element("div.search-result.tt-suggestion.tt-selectable > a", timeout=2)
            sb.click(element)
        except Exception:
            raise

    def scrape_results(self) -> (str, str, str):
        try:
            # stock_status = self.driver.find_element(By.CSS_SELECTOR, 'li.product-stock > span').text
            #
            # trader_price = self.driver.find_element(By.CSS_SELECTOR, 'div.price-group > div.product-price').text
            # trader_price_number = ''.join(filter(str.isdigit, trader_price))
            #
            # consumer_price = self.driver.find_element(By.CSS_SELECTOR, 'div.text-left').text
            # consumer_price_number = ''.join(filter(str.isdigit, consumer_price))
            #
            stock_status = self.get_text('li.product-stock > span')

            trader_price = self.get_text('div.price-group > div.product-price')
            trader_price_number = ''.join(filter(str.isdigit, trader_price))

            consumer_price = self.get_text('div.text-left')
            consumer_price_number = ''.join(filter(str.isdigit, consumer_price))

            return stock_status, trader_price_number, consumer_price_number
        except Exception:
            raise


# search

class TechTopScraper(WebScraper):
    def __init__(self, headless_mode=True):
        super().__init__(2, headless_mode)

    def login(self):
        try:
            # self.driver.get(self.base_url + '/Login')
            # self.driver.implicitly_wait(2)
            self.open(self.base_url + '/Login')

            # login_field = self.driver.find_element(By.CSS_SELECTOR, "#ContentPlaceHolder1_Login1_LoginName")
            # pwd_field = self.driver.find_element(By.CSS_SELECTOR, '#ContentPlaceHolder1_Login1_LoginPWD')
            # submit_btn = self.driver.find_element(By.CSS_SELECTOR, '#ContentPlaceHolder1_Login1_submitLogIn')
            #
            # login_field.send_keys(self.username)
            # pwd_field.send_keys(self.pwd)
            # submit_btn.send_keys(Keys.RETURN)

            self.type('#ContentPlaceHolder1_Login1_LoginName', self.username)
            self.type('#ContentPlaceHolder1_Login1_LoginPWD', self.pwd)
            self.click('#ContentPlaceHolder1_Login1_submitLogIn')

            # # Check if login was successful by looking for a known element on the home page
            # WebDriverWait(self.driver, 2).until(
            #     ec.presence_of_element_located((By.XPATH, "//*[@id='btnOpenAccount']/div[@class='name']"))
            # )
            self.assert_element_present("//*[@id='btnOpenAccount']/div[@class='name']")
            print("Login successful")


        except Exception:
            raise

    def search_item(self, item_code):
        # search_field = self.driver.find_element(By.XPATH, "//input[@id='search']")
        # search_field.clear()
        # search_field.send_keys(item_code)
        # search_btn = self.driver.find_element(By.ID, "SearchButton")
        # self.driver.execute_script("arguments[0].click();", search_btn)

        self.type("//input[@id='search']", item_code)
        self.click("#SearchButton")

        try:
            # results_container = WebDriverWait(self.driver, 2).until(
            #     ec.presence_of_element_located((By.CSS_SELECTOR, 'div.searchresults a'))
            # )

            # Wait for the first search result to be clickable
            # first_result = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.searchresults a'))
            # )

            # Click on the first search result
            results_container = self.get_element('div.searchresults a')
            self.driver.execute_script("arguments[0].click();", results_container)
        except Exception:
            raise

    def scrape_results(self) -> (str, str, str):
        try:
            # WebDriverWait(self.driver, 4).until(
            #     ec.presence_of_element_located((By.CLASS_NAME, "productdataplace"))
            # )
            # self.driver.implicitly_wait(4)
            # stock_status = self.driver.find_element(By.CSS_SELECTOR, "div.stockplace span").text
            #
            # prices = self.driver.find_elements(By.CSS_SELECTOR, "div.price span.pr")
            # consumer_price = prices[0].text.split(' ')[0].split('.')[0]
            # trader_price = prices[1].text.split(' ')[0].split('.')[0]

            stock_status = self.get_text("div.stockplace span")
            prices = self.find_elements("div.price span.pr")
            consumer_price = prices[0].text.split(' ')[0].split('.')[0]
            trader_price = prices[1].text.split(' ')[0].split('.')[0]

            return stock_status, trader_price, consumer_price
        except NoSuchElementException:
            raise


class ShalmonScraper(WebScraper):
    def __init__(self, headless_mode=True):
        super().__init__(3, headless_mode)

    def login(self):
        # self.driver.get(self.base_url + '/my-account')
        self.open(self.base_url + '/my-account')

        try:
            # login_field = self.driver.find_element(By.CSS_SELECTOR, "#username")
            # pwd_field = self.driver.find_element(By.CSS_SELECTOR, '#password')
            # submit_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[name="login"]')

            # login_field.send_keys(self.username)
            # pwd_field.send_keys(self.pwd)
            # submit_btn.send_keys(Keys.RETURN)

            # self.driver.type("#username", self.username)
            # self.driver.type("#password", self.pwd)
            # self.driver.click('button[name="login"]')
            # self.driver.assert_element(".woocommerce-my-account-wrapper")

            self.type("#username", self.username)
            self.type("#password", self.pwd)
            self.click('button[name="login"]')
            self.assert_element(".woocommerce-my-account-wrapper")

            # # Check if login was successful by looking for a known element on the home page
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "woocommerce-my-account-wrapper"))
            # )
            print("Login successful")


        except Exception:
            raise

    def search_item(self, item_code):
        # search_field = self.driver.find_element(By.XPATH, "//input[@aria-label='Search']")
        # search_field.clear()
        # search_field.send_keys(item_code)
        # search_btn = self.driver.find_element(By.CLASS_NAME, "searchsubmit")
        # # self.driver.execute_script("arguments[0].click();", search_btn)
        # search_btn.click()

        self.type("//input[@aria-label='Search']")
        self.click('searchsubmit')
        try:
            results_container = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'wd-product'))
            )

            # Wait for the first search result to be clickable
            # first_result = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.searchresults a'))
            # )

            # Click on the first search result
            link = self.driver.find_element(By.CSS_SELECTOR, "div.wd-product a")
            # self.driver.execute_script("arguments[0].click();", results_container)
            link.click()
        except Exception:
            raise

'''

'''
# Usage example
def main():
    pass
    
    # Music Center
    headless_mode = True
    products = ["4260685059885", "AF510M OP"]
    music_center_scraper = MusicCenterScraper(products, headless_mode)

    try:
        print("Music Center")
        music_center_scraper.login()
        for product in products:
            music_center_scraper.search_item(product)
            (stock_status, seller_price, customer_price) = music_center_scraper.scrape_results()

            print(f'Product: {product}')
            print('Availability: ' + stock_status)
            print('Seller price: ' + seller_price)
            print('Customer price: ' + customer_price)

    except Exception as e:
        print(f"An error occurred: {e}")
    # finally:
    # music_center_scraper.close()
    
    # Art Studio
    headless_mode = False
    products = ["D280", "sk df180"]
    art_studio_scraper = ArtStudioScraper(headless_mode)

    try:
        print("Art Studio")
        art_studio_scraper.login()

        for product in products:
            art_studio_scraper.search_item(product)
            (stock_status, seller_price, customer_price) = art_studio_scraper.scrape_results()

            print(f'Product: {product}')
            print('Availability: ' + stock_status)
            print('Seller price: ' + seller_price)
            print('Customer price: ' + customer_price)

    except Exception as e:
        print(f"An error occurred: {e}")
    # finally:
    #     art_studio_scraper.close()

    # Tech Top
    headless_mode = True
    products = ['11613', '11618']
    tech_top_scraper = TechTopScraper(headless_mode)

    try:
        print("Tech Top")
        tech_top_scraper.login()

        for product in products:
            tech_top_scraper.search_item(product)
            (stock_status, seller_price, customer_price) = tech_top_scraper.scrape_results()

            print(f'Product: {product}')
            print('Availability: ' + stock_status)
            print('Seller price: ' + seller_price)
            print('Customer price: ' + customer_price)

    except Exception as e:
        print(f"An error occurred: {e}")
    # finally:
    #     tech_top_scraper.close()

    # Shalmon
    headless_mode = False
    # products = ['11613', '11618']
    shalmon_scraper = ShalmonScraper(headless_mode)

    try:
        print("Shalmon")
        shalmon_scraper.login()

        # for product in products:
        #     tech_top_scraper.search_item(product)
        #     (stock_status, seller_price, customer_price) = tech_top_scraper.scrape_results()
        #
        #     print(f'Product: {product}')
        #     print('Availability: ' + stock_status)
        #     print('Seller price: ' + seller_price)
        #     print('Customer price: ' + customer_price)

    except Exception as e:
        print(f"An error occurred: {e}")
    # finally:
    #     shalmon_scraper.close()

    '''

def main():
    items = ["n460", "sk df180"]
    scraper = MusicCenterScraper(items, headless_mode=True, is_test_env=False)
    try:
        scraper.start()
    except WebScraperException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()