from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from conftest import BasePage
import requests
import time


class Locators:
    LOCATOR_SBIS_CONTACTS_TEXT = (By.LINK_TEXT, 'Контакты')
    LOCATOR_SBIS_TENSOR_BANNER = (By.XPATH, '//*[@id="contacts_clients"]/div[1]/div/div/div[2]/div/a/img')
    LOCATOR_TENSOR_TEXT_BANNER = (By.CLASS_NAME, 'tensor_ru-Index__block4-bg')
    LOCATOR_TENSOR_ABOUT_TEXT = (By.XPATH, '//*[@id="container"]/div[1]/div/div[5]/div/div/div[1]/div/p[4]/a')
    LOCATOR_TENSOR_WORKING_TEXT = (By.XPATH, '//*[@id="container"]/div[1]/div/div[4]')
    LOCATOR_TENSOR_IMAGES = (By.XPATH, ".//img[not(@style='hidden')]")
    LOCATOR_TENSOR_LIST_OF_PARTNERS = (By.XPATH, '//*[@id="contacts_list"]/div/div[2]/div[2]/div/div[2]/div[1]/div['
                                                 '3]/div[2]')
    LOCATOR_TENSOR_MY_REGION = (By.XPATH, '//*[@id="container"]/div[1]/div/div[3]/div[2]/div[1]/div/div[2]')
    LOCATOR_TENSOR_KAMCHATKA_KRAI = (By.XPATH, '//*[@id="popup"]/div[2]/div/div/div/div/div[2]/div/ul/li[43]')
    LOCATOR_SBIS_DOWNLOAD_SBIS = (By.LINK_TEXT, 'Скачать СБИС')
    LOCATOR_SBIS_PLUGIN = (By.XPATH, '//*[@id="ws-nm7llgajiia1706611204837"]/div[2]')


class Urls:
    URL_SBIS_BASE = 'https://sbis.ru/'
    URL_TENSOR_BASE = 'https://tensor.ru/'
    URL_SBIS_DOWNLOAD_PLUGIN = 'https://update.sbis.ru/Sbis3Plugin/master/win32/sbisplugin-setup-web.exe'


class Helper(BasePage):
    list_of_partners = 0

    def check_text_block(self):
        text_block = self.find_element(Locators.LOCATOR_TENSOR_TEXT_BANNER)
        text_to_check = 'Сила в людях'
        assert text_block.text[0:len(text_to_check)] == text_to_check

    def check_and_get_about_href(self):
        elem = self.find_element(Locators.LOCATOR_TENSOR_ABOUT_TEXT)
        assert elem.get_attribute('href') == 'https://tensor.ru/about'
        return elem.get_attribute('href')

    def check_images(self):
        working = self.find_element(Locators.LOCATOR_TENSOR_WORKING_TEXT)
        images = working.find_elements(By.XPATH, ".//img[not(@style='hidden')]")
        for i in range(len(images)):
            for j in range(i + 1, len(images)):
                assert (images[i].get_attribute('height') == images[j].get_attribute('height') or
                        images[i].get_attribute('width') == images[j].get_attribute('width'))

    def check_exists_by_locator(self, locator):
        try:
            self.find_element(locator)
        except NoSuchElementException:
            return False
        return True

    def get_href_by_locator(self, locator):
        contacts = self.find_element(locator)
        return contacts.get_attribute('href')

    def check_region(self):
        response = requests.get(self.get_href_by_locator(Locators.LOCATOR_SBIS_CONTACTS_TEXT))
        cookie_value = dict(self.get_cookie('s3reg'))
        time.sleep(2)
        cur_url = self.current_url()
        assert cookie_value['value'] in cur_url

    def check_existing_list_of_partners(self):
        self.list_of_partners = self.find_element(Locators.LOCATOR_TENSOR_LIST_OF_PARTNERS)
        assert self.check_exists_by_locator(Locators.LOCATOR_TENSOR_LIST_OF_PARTNERS)

    def set_region(self):
        region = self.find_element(Locators.LOCATOR_TENSOR_MY_REGION)
        region.click()
        region = self.find_element(Locators.LOCATOR_TENSOR_KAMCHATKA_KRAI)
        region.click()
        time.sleep(2)

    def check_new_region(self):
        region = self.find_element(Locators.LOCATOR_TENSOR_MY_REGION).text
        assert region == 'Камчатский край'

    def check_new_list_of_partners(self):
        assert self.list_of_partners != self.find_element(Locators.LOCATOR_TENSOR_LIST_OF_PARTNERS)

    def check_url_and_title(self):
        assert "41-kamchatskij-kraj" in self.driver.current_url
        assert "Камчатский край" in self.driver.title
