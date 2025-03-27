from bs4 import BeautifulSoup

from datetime import datetime
import humanize
import os
from pathlib import Path
import sys
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def is_download_page(driver):
    driver.switch_to.default_content()
    frame_id = "ctl00_ContentPlaceHolder_ExtensionIframe"
    button_id_list = [
        "ctl00_ctl00_MainFormContent_DownloadLinkForViewType",
        "ctl00_ctl00_MainFormContent_ResourceContent_DownloadButton_DownloadLink",
    ]
    try:
        driver.switch_to.frame(frame_id)
        for button_id in button_id_list:
            try:
                if driver.find_element(By.ID, button_id):
                    return True
            except:
                pass
        return False
    except:
        return False


def is_link_page(driver):
    driver.switch_to.default_content()
    frame_id = "ctl00_ContentPlaceHolder_ExtensionIframe"
    div_id = "embedPreview"
    try:
        driver.switch_to.frame(frame_id)
        sub_frame = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(sub_frame)
        if driver.find_element(By.ID, div_id):
            if driver.find_element(By.TAG_NAME, "a"):
                return True
        return False
    except:
        return False


def is_discussion_page(driver):
    driver.switch_to.default_content()
    span_xpath = "//span[text()='Discussion']"
    try:
        if driver.find_element(By.XPATH, span_xpath):
            return True
        return False
    except:
        return False


def is_custom_page(driver):
    driver.switch_to.default_content()
    h1_xpath = "//h1[@class='prom-page-header-editable__title']"
    try:
        if driver.find_element(By.XPATH, h1_xpath):
            return True
        return False
    except:
        return False


def page_type(driver):

    if is_download_page(driver):
        return "Download Page"
    elif is_link_page(driver):
        return "Link Page"
    elif is_discussion_page(driver):
        return "Discussion Page"
    elif is_custom_page(driver):
        return "Custom Page"
    else:
        return "Unrecognized Page"
