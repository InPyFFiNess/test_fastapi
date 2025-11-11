import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestSite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists("log.csv"):
            os.remove("log.csv")

        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--test-type")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--headless")

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.set_page_load_timeout(10)
        cls.wait = WebDriverWait(cls.driver, 5)

        cls.base_url = "https://127.0.0.1:443"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_01_open_register_page(self):
        self.driver.get(f"{self.base_url}/register")
        self.assertIn("Регистрация", self.driver.page_source)

    def test_02_register_user(self):
        self.driver.get(f"{self.base_url}/register")
        self.driver.find_element(By.ID, "username").send_keys("testuser")
        self.driver.find_element(By.ID, "password").send_keys("testpass")
        self.driver.find_element(By.ID, "confirm_password").send_keys("testpass")
        self.driver.find_element(By.ID, "confirm_password").send_keys(Keys.RETURN)

        time.sleep(1)
        self.assertIn("Регистрация успешна", self.driver.page_source)
        self.assertIn("login", self.driver.current_url)

    def test_03_login_user(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("testuser")
        self.driver.find_element(By.ID, "password").send_keys("testpass")
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

        self.wait.until(EC.url_contains("/home"))
        self.assertIn("home", self.driver.current_url)
        self.assertIn("Hello world!", self.driver.page_source)

    def test_04_login_wrong_password(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("testuser")
        self.driver.find_element(By.ID, "password").send_keys("wrongpass")
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Неверный логин или пароль"))
        self.assertIn("Неверный логин или пароль", self.driver.page_source)

    def test_05_login_wrong_username(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("nouser")
        self.driver.find_element(By.ID, "password").send_keys("testpass")
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Неверный логин или пароль"))
        self.assertIn("Неверный логин или пароль", self.driver.page_source)

    def test_06_admin_page_access_denied_for_user(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("testuser")
        self.driver.find_element(By.ID, "password").send_keys("testpass")
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        self.wait.until(EC.url_contains("/home"))

        self.driver.get(f"{self.base_url}/admins")

        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "403"))
        self.assertIn("Forbidden", self.driver.page_source)

    def test_07_login_admin_and_access_admin_page(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

        self.wait.until(EC.url_contains("/home"))
        self.assertIn("home", self.driver.current_url)

        self.driver.get(f"{self.base_url}/admins")
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Hello admin!"))
        self.assertIn("Hello admin!", self.driver.page_source)

    def test_08_logout(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("testuser")
        self.driver.find_element(By.ID, "password").send_keys("testpass")
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        self.wait.until(EC.url_contains("/home"))

        self.driver.get(f"{self.base_url}/logout")
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Сессия завершена"))
        self.assertIn("Сессия завершена", self.driver.page_source)

    def test_09_navigation_between_pages(self):
        self.driver.get(f"{self.base_url}/register")

        self.driver.find_element(By.ID, "login").click()
        self.wait.until(EC.url_contains("/login"))
        self.assertIn("Авторизация", self.driver.page_source)

        self.driver.find_element(By.CLASS_NAME, "register-link").click()
        self.wait.until(EC.url_contains("/register"))
        self.assertIn("Регистрация", self.driver.page_source)

    def test_10_404_page(self):
        self.driver.get(f"{self.base_url}/nonexistent-page")
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "404"))
        self.assertIn("Страница не найдена", self.driver.page_source)

    def test_11_password_mismatch(self):
        self.driver.get(f"{self.base_url}/register")
        
        self.driver.find_element(By.ID, "username").send_keys("newuser")
        self.driver.find_element(By.ID, "password").send_keys("pass1")
        self.driver.find_element(By.ID, "confirm_password").send_keys("pass2")
        self.driver.find_element(By.ID, "confirm_password").send_keys(Keys.RETURN)

        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Пароли не совпадают"))
        self.assertIn("Пароли не совпадают", self.driver.page_source)

    def test_12_duplicate_user_registration(self):
        self.driver.get(f"{self.base_url}/register")
        
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "confirm_password").send_keys("1234")
        self.driver.find_element(By.ID, "confirm_password").send_keys(Keys.RETURN)

        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Такой пользователь уже существует"))
        self.assertIn("Такой пользователь уже существует", self.driver.page_source)


if __name__ == "__main__":
    if not os.path.exists("users.csv"):
        with open("users.csv", "w", encoding="utf-8-sig") as f:
            f.write("user,password,role\n")
    
    unittest.main(verbosity=2)