from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import random
import time

chrome_version = random.randint(110, 140)
windows_version = random.randint(10, 11)
opts = Options()
opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT {windows_version}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=opts)

def ignore_casp():
    ignore_link = driver.find_element(By.CLASS_NAME, value="ignorelink")
    ignore_link.click()

def User_test(user):
    name = driver.find_element(By.ID, value="username")
    name.click()
    name.send_keys(user)
    if driver.find_element(By.CLASS_NAME, value="error-message").text == "Такой пользователь уже существует":
        print("Такой пользователь существует")

def Pass_test(password):
    input_pass = driver.find_element(By.ID , value="password")
    input_pass.click()
    input_pass.send_keys(password)
    if driver.find_element(By.CLASS_NAME, value="error-message").text == "Неверный логин или пароль":
        print("Йоу")

def Confirm_pass_test(password):
    input_pass = driver.find_element(By.ID , value="confirm_password")
    input_pass.click()
    input_pass.send_keys(password)
    if driver.find_element(By.CLASS_NAME, value="error-message").text == "Пароли не совпадают":
        print("Пароли не совпадают")

def change_page():
    page = driver.find_element(By.ID, value="change_page")
    page.click()


driver.get("https://127.0.0.1:443")
ignore_casp()

usernames = ["admin", "bimbimbambam", "someone"]
passwords = [1234, 12345, "chotohz"]

for user in usernames:
    User_test(user)
    for pasik in passwords:
        Pass_test(pasik)

time.sleep(10)


