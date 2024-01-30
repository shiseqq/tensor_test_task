import os.path
from Helper import Helper
from Helper import Locators
from Helper import Urls
import requests


def test_first_bench(browser):
    main_page = Helper(browser)
    main_page.open_site(Urls.URL_SBIS_BASE)
    main_page.click_on(Locators.LOCATOR_SBIS_CONTACTS_TEXT)
    main_page.find_element(Locators.LOCATOR_SBIS_TENSOR_BANNER)
    main_page.click_on(Locators.LOCATOR_SBIS_TENSOR_BANNER)
    main_page.open_site(Urls.URL_TENSOR_BASE)
    main_page.check_text_block()
    main_page.open_site(main_page.check_and_get_about_href())
    main_page.check_images()


def test_second_bench(browser):
    main_page = Helper(browser)
    main_page.open_site(Urls.URL_SBIS_BASE)
    main_page.open_site(main_page.get_href_by_locator(Locators.LOCATOR_SBIS_CONTACTS_TEXT))
    main_page.check_region()
    main_page.check_existing_list_of_partners()
    main_page.set_region()
    main_page.check_new_region()
    main_page.check_new_list_of_partners()
    main_page.check_url_and_title()


def test_third_bench(browser):
    filename = 'app.exe'
    p = requests.get(Urls.URL_SBIS_DOWNLOAD_PLUGIN)
    out = open(filename, "wb")
    out.write(p.content)
    out.close()
    filesize = os.path.getsize(filename)
    assert filesize == 7361144

