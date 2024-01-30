from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pytest


@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(ec.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(ec.presence_of_all_elements_located(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def click_on(self, locator):
        contacts = self.find_element(locator)
        return contacts.click()

    def close_window(self):
        return self.driver.close()

    def get_cookie(self, name):
        return self.driver.get_cookie(name)

    def current_url(self):
        return self.driver.current_url

    def open_site(self, url):
        return self.driver.get(url)
