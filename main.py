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

from src.page import page_type

from list_files import list_files, list_paths, list_downloads
from load_config import *
from login import login
from print_log import print_log

INF = 2**31 - 1


def set_download_path(driver, path):
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": path}
    )


def download_button(driver):
    print(page_type(driver))
    if page_type(driver) != "Download Page":
        return None
    driver.switch_to.default_content()
    frame_id = "ctl00_ContentPlaceHolder_ExtensionIframe"
    button_id_list = [
        "ctl00_ctl00_MainFormContent_DownloadLinkForViewType",
        "ctl00_ctl00_MainFormContent_ResourceContent_DownloadButton_DownloadLink",
    ]
    driver.switch_to.frame(frame_id)
    for button_id in button_id_list:
        try:
            return driver.find_element(By.ID, button_id)
        except:
            pass
    return None


def download(driver, path, url):
    driver.get(url)
    print_log(f"Opened {url}")

    set_download_path(driver, os.path.dirname(os.path.join(DownloadPath, path)))
    print_log(
        f"Set download directory to {os.path.dirname(os.path.join(DownloadPath, path))}"
    )

    db = download_button(driver)
    if db:
        db.click()
        print_log(f"Downloaded {path}")
    else:
        print_log(f"No download button found for {path}")


if __name__ == "__main__":

    # Print Header
    print("Hydrangea Athena Downloader © 2025 by Zeyu Xie. All rights reserved.")
    
    # Create Download Path
    if not os.path.exists(DownloadPath):
        os.makedirs(DownloadPath, exist_ok=True)
        print_log(f"Download Path: {DownloadPath}")

    # Set Chrome Options
    prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    print_log("Chrome Options Set")
    options = Options()
    options.add_experimental_option("prefs", prefs)
    
    # Start Driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.set_page_load_timeout(INF)
    print_log("Driver Started")

    # Open Athena
    driver.get("https://athena.itslearning.com/main.aspx?TextURL=CourseCards")
    print_log("Opened Athena")

    # Login
    login(driver)

    driver.get(f"https://athena.itslearning.com/Resources?FolderID={FolderID}")
    print_log("Folder Opened")

    urldict = list_files(driver)
    print_log("All Files URL Listed")
    pathdict = list_paths(urldict)
    print_log("All Files Path Listed")
    downloadlist = list_downloads(driver, pathdict, urldict)
    print_log("All Files Download List Generated")

    try:
        for item in downloadlist:
            download(driver, item[0], item[1])
        folder = Path(DownloadPath)
        size = sum(f.stat().st_size for f in folder.rglob("*") if f.is_file())
        readable_size = humanize.naturalsize(size, binary=True)
        print_log(
            f"All {len(downloadlist)} files downloaded successfully, total size: {readable_size}."
        )
        while True:
            pass
    except Exception as e:
        print_log(f"Download Failed: {e}")
