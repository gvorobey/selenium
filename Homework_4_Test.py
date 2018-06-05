import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

browsers = ["Chrome", "Firefox"]

def open_browser(browser):
    function = getattr(webdriver, browser)
    driver = function()
    driver.get("http://localhost/litecart")
    return driver

def close_browser(driver):
    driver.quit()

def find_price(product, price_type):
    selected_type = product.find_element_by_class_name("%s" % price_type)
    price = selected_type.get_attribute("innerText")
    color = selected_type.value_of_css_property("color")
    style = selected_type.tag_name
    return (price, color, style)

@pytest.mark.parametrize("browser", browsers)
def test_compare_name_and_price(browser):

    driver = open_browser(browser)

    regular_price = "regular-price"
    campaign_price = "campaign-price"

    campaigns = driver.find_element_by_id("box-campaigns")
    campaigns_product = campaigns.find_element_by_tag_name("li")
    campaings_product_name = campaigns_product.find_element_by_class_name("name").get_attribute("innerText")

    campaigns_regular_price = find_price(campaigns_product, regular_price)
    campaigns_discount_price = find_price(campaigns_product, campaign_price)

    campaigns_product.click()

    main_product = driver.find_element_by_id("box-product")
    main_product_name = main_product.find_element_by_class_name("title").get_attribute("innerText")

    main_regular_price = find_price(main_product, regular_price)
    main_discount_price = find_price(main_product, campaign_price)

    assert campaings_product_name == main_product_name
    assert campaigns_discount_price == main_discount_price
    assert campaigns_regular_price == main_regular_price

    close_browser(driver)