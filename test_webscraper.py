
import pytest
from webscraper import MusicCenterScraper
from seleniumbase import BaseCase
from selenium.common.exceptions import TimeoutException, NoSuchElementException


'''
import unittest
# import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from webscraper import MusicCenterScraper
                        # ArtStudioScraper, TechTopScraper, ShalmonScraper)


class TestMusicCenterScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        headless_mode = True
        cls.scraper = MusicCenterScraper(["4260685059885", "AF510M OP"], headless_mode)

    @classmethod
    def tearDownClass(cls):
        pass
        # cls.scraper.close()

    def test_login_success(self):
        try:
            self.scraper.login()
            # WebDriverWait(self.scraper.driver, 3).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "nav-menu-container")))
            self.assertTrue(self.scraper.sb.find_element(By.CLASS_NAME, "nav-menu-container").is_displayed())
            print("TestMusicCenterScraper Login test passed")
        except NoSuchElementException:
            self.fail("TestMusicCenterScraper Login test failed: Incorrect credentials or element not found")
        except TimeoutException:
            self.fail("TestMusicCenterScraper Login test failed: Page load timeout")
        except WebDriverException as e:
            self.fail(f"TestMusicCenterScraper Login test failed: WebDriver exception - {e}")

    def test_search_item(self):
        try:
            # self.scraper.login()
            self.scraper.search_item("4260685059885")
            print("TestMusicCenterScraper Search item test passed")
        except NoSuchElementException:
            self.fail("TestMusicCenterScraper Search item test failed: Element not found")
        except TimeoutException:
            self.fail("TestMusicCenterScraper Search item test failed: Page load timeout")
        except WebDriverException as e:
            self.fail(f"TestMusicCenterScraper Search item test failed: WebDriver exception - {e}")

    def test_scrape_results(self):
        try:
            # self.scraper.login()
            self.scraper.search_item("AF510M OP")
            (stock_status, seller_price, customer_price) = self.scraper.scrape_results()
            self.assertEqual(seller_price, "364")
            print("TestMusicCenterScraper scrape results test passed")
        except NoSuchElementException:
            self.fail("TestMusicCenterScraper Scrape results test failed: Element not found")
        except TimeoutException:
            self.fail("TestMusicCenterScraper Scrape results test failed: Page load timeout")
        except WebDriverException as e:
            self.fail(f"TestMusicCenterScraper Scrape results test failed: WebDriver exception - {e}")
'''
'''
class TestArtStudioScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        headless_mode = False
        cls.scraper = ArtStudioScraper(headless_mode)

    @classmethod
    def tearDownClass(cls):
        cls.scraper.close()

    def test_login_success(self):
        try:
            self.scraper.login()
            self.assertTrue(
                self.scraper.driver.find_element(By.XPATH, "//span[@class='links-text' and text()='החשבון שלי']"))
            print("TestArtStudioScraper Login test passed")
        except NoSuchElementException:
            self.fail("TestArtStudioScraper Login test failed: Incorrect credentials or element not found")
        except TimeoutException:
            self.fail("TestArtStudioScraper Login test failed: Page load timeout")
        except WebDriverException as e:
            self.fail(f"TestArtStudioScraper Login test failed: WebDriver exception - {e}")

    def test_search_item(self):
        try:
            # self.scraper.login()
            self.scraper.search_item("d280")
            self.assertTrue(self.scraper.driver.find_element(By.CLASS_NAME, 'product-stock'))
            print("TestArtStudioScraper Search item test passed")
        except NoSuchElementException:
            self.fail("TestArtStudioScraper Search item test failed: Element not found")
        except TimeoutException:
            self.fail("TestArtStudioScraper Search item test failed: Page load timeout")
        except WebDriverException as e:
            self.fail(f"TestArtStudioScraper Search item test failed: WebDriver exception - {e}")

    def test_scrape_results(self):
        try:
            self.scraper.search_item("sk df180")
            (stock_status, seller_price, customer_price) = self.scraper.scrape_results()
            self.assertEqual(seller_price, "489")
            print("TestArtStudioSCraper Scrape Results test passed")
        except WebDriverException as e:
            self.fail(f"TestArtStudioScraper Search item test failed: WebDriver exception - {e}")


class TestTechTopScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        headless_mode = True
        cls.scraper = TechTopScraper(headless_mode)

    @classmethod
    def tearDownClass(cls):
        cls.scraper.close()

    def test_login_success(self):
        try:
            self.scraper.login()
            self.assertTrue(self.scraper.driver.find_element(By.XPATH, "//*[@id='btnOpenAccount']/div[@class='name']"))
            print("TestTechTopScraper Login test passed")
        except NoSuchElementException:
            self.fail("TestTechTopScraper Login test failed: Incorrect credentials or element not found")
        except TimeoutException:
            self.fail("TestTechTopScraper Login test failed: Page load timeout")
        except WebDriverException as e:
            self.fail(f"TestTechTopScraper Login test failed: WebDriver exception - {e}")

    def test_search_item(self):
        try:
            self.scraper.search_item("11613")
            self.assertTrue(self.scraper.driver.find_element(By.CLASS_NAME, 'productdataplace'))
            print("TestTechTopScraper Search item test passed")
        except NoSuchElementException:
            self.fail("TestTechTopScraper Search item test failed: Element not found")
        except TimeoutException:
            self.fail("TestTechTopScraper Search item test failed: Page load timeout")
        except WebDriverException as e:
            self.fail(f"TestTechTopScraper Search item test failed: WebDriver exception - {e}")

    def test_scrape_results(self):
        try:
            self.scraper.search_item("11618")
            (stock_status, seller_price, customer_price) = self.scraper.scrape_results()
            self.assertEqual(seller_price, "37")
            print("TestTechTopScraper Scrape Results test passed")
        except WebDriverException as e:
            self.fail(f"TestTechTopScraper Search item test failed: WebDriver exception - {e}")


class TestShalmonScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        headless_mode = True
        cls.scraper = ShalmonScraper(headless_mode)

    @classmethod
    def tearDownClass(cls):
        cls.scraper.close()

    def test_login_success(self):
        try:
            self.scraper.login()
            self.scraper.driver.assert_element(".woocommerce-my-account-wrapper")
            print("TestShalmonScraper Login test passed")
        except NoSuchElementException:
            self.fail("TestShalmonScraper Login test failed: Incorrect credentials or element not found")
        except TimeoutException:
            self.fail("TestShalmonScraper Login test failed: Page load timeout")
        except WebDriverException as e:
            self.fail(f"TestShalmonScraper Login test failed: WebDriver exception - {e}")


if __name__ == "__main__":
    unittest.main()
'''
'''

# from seleniumbase import Driver
import pytest
from seleniumbase import BaseCase
from webscraper import MusicCenterScraper, ArtStudioScraper


class TestMusicCenterScraper(BaseCase):
# class TestMusicCenterScraper():

    @pytest.mark.usefixtures("sb")  # This ensures SeleniumBase's setup/teardown
    def test_music_center_login(self):
        self.scraper = MusicCenterScraper(["AF510M OP", "4260685059885"], headless_mode=True, is_test_env=True)
        self.scraper.setUp()
        try:
            self.scraper.login()
            self.scraper.assert_exact_text("דף הבית", "div.title")
        finally:
            self.scraper.tearDown()

    def test_music_center_search(self):
        self.scraper = MusicCenterScraper(["AF510M OP", "4260685059885"], headless_mode=True, is_test_env=True)
        self.scraper.setUp()
        try:
            self.scraper.login()
            self.scraper.search_item("AF 1111111111879645133546767#$%#$(124234^&")
            # self.scraper.assert_element("div.item-container", timeout=2)
            self.scraper.assert_element_not_present("div.item-container")
            self.scraper.wait(2)
            self.scraper.search_item("AF510M OP")
            self.scraper.assert_element("div.item-container", timeout=3)
        finally:
            self.scraper.tearDown()

    def test_music_center_scrape_results(self):
        self.scraper = MusicCenterScraper(["AF510M OP"], headless_mode=True, is_test_env=True)
        self.scraper.setUp()
        try:
            self.scraper.login()
            self.scraper.search_item("AF510M OP")
            # self.scraper.assert_element("div.item-container", timeout=2)
            self.scraper.assertEqual(('קיים במלאי', '364', '655'), self.scraper.scrape_results())
        finally:
            self.scraper.tearDown()
            

'''
'''
class TestArtStudioScraper(BaseCase):
    @pytest.mark.usefixtures("sb")  # This ensures SeleniumBase's setup/teardown
    def test_art_studio_login(self):
        self.scraper = ArtStudioScraper(["d280", "sk df180"], headless_mode=True, is_test_env=True)
        self.scraper.setUp()
        try:
            self.scraper.login()
            self.scraper.assert_text("החשבון שלי")
        finally:
            self.scraper.tearDown()

'''

class TestMusicCenterScraper(BaseCase):

    @pytest.mark.usefixtures("sb")  # Ensures SeleniumBase setup/teardown
    def test_login(self):
        """Test the login functionality with real data."""
        scraper = MusicCenterScraper(
            items=["AF510M OP", "4260685059885"],
            headless_mode=True,
            is_test_env=True
        )
        scraper.login(self)  # Pass 'self' as the driver argument

    @pytest.mark.usefixtures("sb")
    def test_search_item(self):
        """Test item search functionality with real items."""
        scraper = MusicCenterScraper(
            items=["AF510M OP", "4260685059885"],
            headless_mode=True,
            is_test_env=True
        )
        scraper.login(self)  # Pass 'self' as the driver
        scraper.search_item(self, "AF510M OP")  # Pass 'self' as the driver

    @pytest.mark.usefixtures("sb")
    def test_scrape_results(self):
        """Test scraping product data after searching."""
        scraper = MusicCenterScraper(
            items=["AF510M OP", "4260685059885"],
            headless_mode=True,
            is_test_env=True
        )
        scraper.login(self)  # Pass 'self' as the driver
        scraper.search_item(self, "AF510M OP")  # Pass 'self' as the driver
        results = scraper.scrape_results(self)  # Pass 'self' as the driver

        for result in results:
            assert result != "N/A"


    @pytest.mark.usefixtures("sb")
    def test_nonexistent_item(self):
        """Test search functionality with a non-existent item code."""
        scraper = MusicCenterScraper(
            items=["NONEXISTENT_ITEM"],  # Pass a non-existent item code
            headless_mode=True,
            is_test_env=True
        )
        scraper.login(self)  # Ensure logged in before searching
        try:
            scraper.search_item(self, "NONEXISTENT_ITEM")  # Search for non-existent item
            self.sleep(2)
            results = scraper.scrape_results(self)  # Attempt to scrape results

            for result in results:
                assert result == "N/A"

        except Exception as e:
            pytest.fail(f"Scraping failed for non-existent item: {e}")



