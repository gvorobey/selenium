import pytest
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener

menu_xpass = "//ul[@id='box-apps-menu']/li"

class Logger(AbstractEventListener):
    def before_find(self, by, value, driver):
        print("Trying to find element %s" % value)
    def after_find(self, by, value, driver):
        print("Found element %s" % value)
    def on_exception(self, exception, driver):
        screenshot_name = str(datetime.datetime.now()).replace(":", "-") + ".png"
        driver.get_screenshot_as_file(screenshot_name)
        print("Screenshot saved as '%s'" % screenshot_name)

@pytest.yield_fixture(scope="session", autouse=True)
def driver():

    help_driver = webdriver.Chrome()
    driver = EventFiringWebDriver(help_driver, Logger())
    driver.get("http://localhost/litecart/admin/")
    el_username = driver.find_element_by_name("username")
    el_username.send_keys("admin")
    el_password = driver.find_element_by_name("password")
    el_password.send_keys("admin")

    el_login = driver.find_element_by_name("login")
    el_login.click()

    yield driver
    driver.quit()


def test_check_menu(driver):
    el_count = len(driver.find_elements(By.XPATH, menu_xpass))

    for counter in range(1, el_count):
        el = driver.find_element_by_xpath("%s[%s]" % (menu_xpass, counter))
        el.click()
        assert driver.find_element_by_tag_name("h1")

        el = driver.find_element_by_xpath("%s[%s]" % (menu_xpass, counter))
        submenu = el.find_elements(By.XPATH, "./ul/li")
        target_id = list(menu.get_attribute("id") for menu in submenu)

        for id in target_id:
            el = driver.find_element_by_id(id)
            el.click()
            assert driver.find_element_by_tag_name("h1")




