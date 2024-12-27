from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pytest


# Функция ожидания элементов
def wait_of_element_located(xpath, driver):
   element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located(
         (By.XPATH, xpath)
      )
   )
   return element


# Вынесем инициализцию драйвера в отдельную фикстуру pytest
@pytest.fixture
def driver():
   options = webdriver.ChromeOptions()
   options.add_experimental_option("excludeSwitches", ["enable-logging"])
   driver = webdriver.Chrome(options=options)
   driver.get("https://www.saucedemo.com/")
   yield driver
2

# Вынесем аутентификацию юзера в отдельную функцию
def auth_user(user_name, password, driver):
   # Поиск и ожидание элементов и присваивание к переменным.
   input_username = wait_of_element_located(xpath='//*[@id=\"user-name\"]', driver=driver)
   input_password = wait_of_element_located(xpath='//*[@id=\"password\"]', driver=driver)
   login_button = wait_of_element_located(xpath='//*[@id=\"login-button\"]', driver=driver)

   # Действия с формами
   input_username.send_keys("standard_user")
   input_password.send_keys("secret_sauce")
   login_button.send_keys(Keys.RETURN)



def add_to_cart(xpath_item, driver):
   # Поиск и ождиание прогрузки ссылки элемента товара магазина и клик по ссылке
   item_name = wait_of_element_located(xpath='//*[@id=\"item_5_title_link\"]/div', driver=driver)
   item_name.click()

   # Поиск и ожидание кнопки добавления товара и клик по этой кнопке
   item_add_button = wait_of_element_located(xpath='//*[@id="add-to-cart"]', driver=driver)
   item_add_button.click()

   # Ждем пока товар добавится в корзину, появится span(кол-во позиций в корзине) и кликаем по корзине чтобы перейти
   shopcar_with_item = wait_of_element_located(xpath='//*[@id=\"shopping_cart_container\"]/a/span', driver=driver)
   return shopcar_with_item


def test_add_jacket_to_the_shopcart(driver):
   # Аутентификация пользователя
   auth_user("standard_user", "secret_sauce", driver=driver)

   # Добавление товара в корзину и если товар добавлен переход в корзину
   add_to_cart(xpath_item='//*[@id="item_5_title_link"]/div', driver=driver).click()

   # Поиск корзины и клик
   wait_of_element_located(xpath='//*[@id="shopping_cart_container"]/a', driver=driver).click()

   # Еще один поиск ссылки элемента позиции магазина
   item_name = wait_of_element_located(xpath='//*[@id="item_5_title_link"]/div', driver=driver)

   item_description = wait_of_element_located(
      xpath='//*[@id="cart_contents_container"]/div/div[1]/div[3]/div[2]/div[1]', driver=driver)

   assert item_description.text == "It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office."
   assert item_name.text == "Sauce Labs Fleece Jacket"

   driver.close()

if(__name__ == "__main__"):
   test_add_jacket_to_the_shopcart()