from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

from src.page import page_type

from list_files import list_files, list_paths, list_downloads
from load_config import *
from login import login
from print_log import print_log
from download import download

INF = 2**31 - 1

if __name__ == "__main__":

    # Print Header
    print("Hydrangea Athena Downloader © 2025 by Zeyu Xie. All rights reserved.")
    print("")

    # Create Download Path
    if not os.path.exists(DownloadPath):
        os.makedirs(DownloadPath, exist_ok=True)
        print_log(f"Created download Path: {DownloadPath}")
    else:
        print_log(f"Download Path {DownloadPath} already exists")

    # Set Chrome Options
    prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options = Options()
    options.add_experimental_option("prefs", prefs)
    print_log("Chrome Options Set")

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
    print_log("Logged In")

    # Open Folder
    driver.get(f"https://athena.itslearning.com/Resources?FolderID={FolderID}")
    print_log(f"Folder (ID: {FolderID}) Opened")

    # List Files
    urldict = list_files(driver)
    print_log("All Files URL Listed")

    # List Paths
    pathdict = list_paths(urldict)
    print_log("All Files Path Listed")

    # List Downloads
    downloadlist = list_downloads(driver, pathdict, urldict)
    print_log("All Files Download List Generated")

    # Download
    download(driver, urldict, pathdict, downloadlist)
