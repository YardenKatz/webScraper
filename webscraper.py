# import math

# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
# import undetected_chromedriver as UC
import time, pickle, requests
from seleniumbase import Driver as SBDriver
from services.config_service import ConfigService


class WebScraperException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class WebScraper:
    def __init__(self, target_index, headless_mode = True):
        self.config_service = ConfigService('config.ini')
        self.config_service.readConfig()
        targets = self.config_service.getTargets()

        self.base_url = self.config_service.getData(targets[target_index], 'url')
        self.username = self.config_service.getData(targets[target_index], 'username')
        self.pwd = self.config_service.getData(targets[target_index], 'pwd')

        self.headless_mode = headless_mode
        # self.profile_path = "/chrome_profile"
        # self.profile_directory = "Profile 1"
        self.driver = self.init_driver()
        # self.session = requests.session()

    def init_driver(self):
        # service = Service('C:/Apps/chromedriver-win64/chromedriver.exe')
        # options = Options()
        # options.add_argument(f"--user-data-dir={self.profile_path}")
        # options.add_argument(f'--profile-directory={self.profile_directory}')
        # if self.headless_mode:
        #     options.add_argument("--headless=new")
        # return webdriver.Chrome(service=service, options=options)
        return SBDriver(uc=True, headless=self.headless_mode)

    def login(self):
        raise NotImplementedError("Subclasses should implement this method")

    def search_item(self, item_code):
        raise NotImplementedError("Subclasses should implement this method")

    def scrape_results(self) -> (str, str, str):
        raise NotImplementedError("Subclasses should implement this method")

    def close(self):
        self.driver.quit()


class MusicCenterScraper(WebScraper):

    def __init__(self, headless_mode = True):
        super().__init__(0 ,headless_mode)
        self.is_first_search = True

    def login(self):
        try:
            login_endpoint = '/system/login'
            self.driver.get(self.base_url + login_endpoint)
            self.driver.implicitly_wait(2)

            username_field, pwd_field = self.driver.find_elements(By.CSS_SELECTOR, "input[role='textbox']")
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "dx-button[aria-label='כניסה למערכת']")

            print("Entering login credentials")
            username_field.send_keys(self.username)
            pwd_field.send_keys(self.pwd)
            submit_btn.send_keys(Keys.RETURN)

            self.driver.implicitly_wait(2)

            # Check if login was successful by looking for a known element on the home page
            WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "dx-button[aria-label='התחל הזמנה']"))
            )
            print("Login successful")
        except (NoSuchElementException, TimeoutException):
            self.close()
            raise WebScraperException("Login failed: Incorrect credentials or element not found\n")

    def search_item(self, item_code):
        try:
            if self.is_first_search:
                self.driver.find_element(By.CSS_SELECTOR, "dx-button[aria-label='התחל הזמנה']").send_keys(Keys.RETURN)
                self.is_first_search = False
            search_field = self.driver.find_element(By.CSS_SELECTOR, "input.dx-texteditor-input")
            search_field.clear()
            search_field.send_keys(item_code)
            search_field.send_keys(Keys.RETURN)
            # print("Search initiated for item:", item_code)
            time.sleep(5)  # Adjust the sleep time as needed
        except NoSuchElementException:
            # self.close()
            raise WebScraperException("Search failed. Search field not found")

    def scrape_results(self) -> (str, str, str):
        try:
            # WebDriverWait(self.driver, 4).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='stock-custom-text']"))
            # )
            self.driver.implicitly_wait(4)
            stock_status = self.driver.find_element(By.CSS_SELECTOR, "div[class*='stock-custom-text']").text
            trader_price = self.driver.find_element(By.CLASS_NAME, "price").text
            price_switch = self.driver.find_element(By.CLASS_NAME, "alternative-price")
            price_switch.click()
            consumer_price = self.driver.find_element(By.CLASS_NAME, "price").text


            return (stock_status, trader_price, consumer_price)
        except NoSuchElementException:
            raise


class ArtStudioScraper(WebScraper):
    def __init__(self, headless_mode = True):
        super().__init__(1, headless_mode)

    def init_driver(self):
        return SBDriver(uc=True, headless=self.headless_mode)

    def login(self):
        try:
            self.driver.get(self.base_url + '?route=account/login')
            # self.driver.implicitly_wait(5)

            # login_field = self.driver.find_element(By.CSS_SELECTOR, "#input-email")
            # pwd_field = self.driver.find_element(By.CSS_SELECTOR, '#input-pwd')
            # submit_btn = self.driver.find_element(By.CSS_SELECTOR, '#content > div > div:nth-child(2) > div > form > div.buttons > div > button')
            #
            # login_field.send_keys(self.username)
            # pwd_field.send_keys(self.pwd)
            # submit_btn.send_keys(Keys.RETURN)

            self.driver.type("#input-email", self.username)
            self.driver.type("#input-password", self.pwd)
            self.driver.click('#content > div > div:nth-child(2) > div > form > div.buttons > div > button')

            # Check if login was successful by looking for a known element on the home page
            # WebDriverWait(self.driver, 4).until(
            #     EC.presence_of_element_located((By.XPATH, "//span[@class='links-text' and text()='החשבון שלי']"))
            # )
            # self.driver.assert_element("//span[@class='links-text' and text()='החשבון שלי']")
            self.driver.assert_text("החשבון שלי")
            print("Login successful")


        except Exception as error:
            raise


    def search_item(self, item_code):
        search_field = self.driver.find_element(By.XPATH,'// *[ @ id = "search"] / div / div / span / input[2]')
        search_field.clear()
        search_field.send_keys(item_code)
        try:
            wait = WebDriverWait(self.driver, 3)  # wait for up to 3 seconds
            element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-result.tt-suggestion.tt-selectable"))
            )

            # Find the link within the element
            link = element.find_element(By.TAG_NAME, "a")
            link.click()
        except Exception as e:
            raise


    def scrape_results(self) -> (str, str, str):
        try:
            stock_status = self.driver.find_element(By.CSS_SELECTOR, 'li.product-stock > span').text

            trader_price = self.driver.find_element(By.CSS_SELECTOR, 'div.price-group > div.product-price').text
            trader_price_number = ''.join(filter(str.isdigit, trader_price))

            consumer_price = self.driver.find_element(By.CSS_SELECTOR,'div.text-left').text
            consumer_price_number = ''.join(filter(str.isdigit, consumer_price))

            return (stock_status, trader_price_number, consumer_price_number)
        except Exception as e:
            raise


#search

class TechTopScraper(WebScraper):
    def __init__(self, headless_mode = True):
        super().__init__(2, headless_mode)

    def login(self):
        try:
            self.driver.get(self.base_url + '/Login')
            # self.driver.implicitly_wait(2)

            login_field = self.driver.find_element(By.CSS_SELECTOR, "#ContentPlaceHolder1_Login1_LoginName")
            pwd_field = self.driver.find_element(By.CSS_SELECTOR, '#ContentPlaceHolder1_Login1_LoginPWD')
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, '#ContentPlaceHolder1_Login1_submitLogIn')

            login_field.send_keys(self.username)
            pwd_field.send_keys(self.pwd)
            submit_btn.send_keys(Keys.RETURN)

            # Check if login was successful by looking for a known element on the home page
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='btnOpenAccount']/div[@class='name']"))
            )
            print("Login successful")


        except Exception as error:
            raise

    def search_item(self, item_code):
        search_field = self.driver.find_element(By.XPATH,"//input[@id='search']")
        search_field.clear()
        search_field.send_keys(item_code)
        search_btn = self.driver.find_element(By.ID, "SearchButton")
        self.driver.execute_script("arguments[0].click();", search_btn)

        try:
            results_container = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.searchresults a'))
            )

            # Wait for the first search result to be clickable
            # first_result = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.searchresults a'))
            # )

            # Click on the first search result
            self.driver.execute_script("arguments[0].click();", results_container)
        except Exception as e:
            raise

    def scrape_results(self) -> (str, str, str):
        try:
            WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.CLASS_NAME, "productdataplace"))
            )
            # self.driver.implicitly_wait(4)
            stock_status = self.driver.find_element(By.CSS_SELECTOR, "div.stockplace span").text

            prices = self.driver.find_elements(By.CSS_SELECTOR, "div.price span.pr")
            consumer_price = prices[0].text.split(' ')[0].split('.')[0]
            trader_price = prices[1].text.split(' ')[0].split('.')[0]

            return (stock_status, trader_price, consumer_price)
        except NoSuchElementException:
            raise


class ShalmonScraper(WebScraper): 
    def __init__(self, headless_mode = True):
        # shalmon_url = 'https://shalmonmusic.co.il'
        super().__init__(3, headless_mode)
    
    def login(self):
        self.driver.get(self.base_url + '/my-account')

        try:
            # login_field = self.driver.find_element(By.CSS_SELECTOR, "#username")
            # pwd_field = self.driver.find_element(By.CSS_SELECTOR, '#password')
            # submit_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[name="login"]')

            # login_field.send_keys(self.username)
            # pwd_field.send_keys(self.pwd)
            # submit_btn.send_keys(Keys.RETURN)

            self.driver.type("#username", self.username)
            self.driver.type("#password", self.pwd)
            self.driver.click('button[name="login"]')
            self.driver.assert_element(".woocommerce-my-account-wrapper")

            # # Check if login was successful by looking for a known element on the home page
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "woocommerce-my-account-wrapper"))
            # )
            print("Login successful")


        except Exception as error:
            raise

    def search_item(self, item_code):
        search_field = self.driver.find_element(By.XPATH,"//input[@aria-label='Search']")
        search_field.clear()
        search_field.send_keys(item_code)
        search_btn = self.driver.find_element(By.CLASS_NAME, "searchsubmit")
        # self.driver.execute_script("arguments[0].click();", search_btn)
        search_btn.click()

        try:
            results_container = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'wd-product'))
            )

            # Wait for the first search result to be clickable
            # first_result = WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.searchresults a'))
            # )

            # Click on the first search result
            link =  self.driver.find_element(By.CSS_SELECTOR, "div.wd-product a")
            # self.driver.execute_script("arguments[0].click();", results_container)
            link.click()
        except Exception as e:
            raise

# Usage example
def main():
    # Music Center
    headless_mode = True
    products = ["4260685059885", "AF510M OP"]
    music_center_scraper = MusicCenterScraper(headless_mode)

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
    finally:
        music_center_scraper.close()

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
    finally:
        art_studio_scraper.close()

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
    finally:
        tech_top_scraper.close()

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
    finally:
        shalmon_scraper.close()

if __name__ == "__main__":
    main()
