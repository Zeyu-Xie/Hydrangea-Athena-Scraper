import os
from pathlib import Path
import humanize
from print_log import print_log
from selenium.webdriver.common.by import By
import sys
from time import sleep

from src.page import page_type

from load_config import *

# === Type 1: Download Page ===


def _set_download_path(driver, path):
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": path}
    )


def _download_button(driver):
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


def _download(driver, path):

    driver.switch_to.default_content()

    # Set Download Path
    download_path = os.path.dirname(os.path.join(DownloadPath, path))
    _set_download_path(driver, download_path)
    print_log(f"Set download directory to {download_path}")

    # Get Download Button
    db = _download_button(driver)

    # Download
    if db:
        db.click()
        print_log(f"Downloaded {path}")
    else:
        print_log(f"No download button found for {path}")


# === Overall Functions ===


def _route_page(driver, path, url):

    # Open page
    driver.get(url)
    print_log(f"Opened {url}")

    # Get Page Type
    current_page_type = page_type(driver)
    print_log(f"Page Type: {current_page_type}")

    # Route Page
    if current_page_type == "Download Page":
        _download(driver, path)
    else:
        print_log(f"Page Type {current_page_type} not supported")


def download(driver, urldict, pathdict, downloadlist):
    try:
        # Route Pages
        for item in downloadlist:
            print("")
            _route_page(driver, item[0], item[1])

        # Summary
        folder = Path(DownloadPath)
        size = sum(f.stat().st_size for f in folder.rglob("*") if f.is_file())
        readable_size = humanize.naturalsize(size, binary=True)
        sleep(3)
        print("")
        print_log(
            f"All {len(downloadlist)} files downloaded successfully, total size: {readable_size}."
        )

        # Wait for user to close
        print_log("Print any key to exit.")
        input()
        driver.quit()
        sys.exit(0)
    except Exception as e:
        print_log(f"Download Failed: {e}")
        driver.quit()
        sys.exit(1)
