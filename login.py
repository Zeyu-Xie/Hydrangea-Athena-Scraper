import sys
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from load_config import *
from print_log import print_log

INF = 2**31 - 1


def _is_logged_in(driver):
    url = driver.current_url
    if "athena.itslearning.com/main.aspx?TextURL=CourseCards" in url:
        return True
    elif "athena.itslearning.com/CourseCards" in url:
        return True
    else:
        return False


def login(driver):
    if not AutoLogin:
        print_log("Auto Login Disabled by Config")
        while not _is_logged_in(driver):
            pass
        print_log("Login Successful")
    else:
        print_log("Auto Login Enabled by Config, Logging in")
        try:
            # Wait for and Click Login Button
            element = WebDriverWait(driver, INF).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "itsl-native-login-button")
                )
            )
            _to_login = driver.find_element(By.CLASS_NAME, "itsl-native-login-button")
            _to_login.click()

            # Wait for and Fill in Username and Password
            element = WebDriverWait(driver, INF).until(
                EC.all_of(
                    EC.presence_of_element_located((By.ID, "username")),
                    EC.presence_of_element_located((By.ID, "password")),
                    EC.presence_of_element_located((By.NAME, "_eventId_proceed")),
                )
            )
            _Username = driver.find_element(By.ID, "username")
            _Username.send_keys(Username)
            _Password = driver.find_element(By.ID, "password")
            _Password.send_keys(Password)
            _login = driver.find_element(By.NAME, "_eventId_proceed")
            _login.click()

            # Wait for Login
            while not _is_logged_in(driver):
                if "Incorrect username or password." in driver.page_source:
                    raise Exception("Incorrect username or password.")
        except Exception as e:
            print_log(f"Login Failed: {e}")
            driver.quit()
            sys.exit(1)

        # Finished Login
        print_log("Login Successful")
