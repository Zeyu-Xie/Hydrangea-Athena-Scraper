import os
from pathlib import Path
import humanize
from print_log import print_log
from selenium.webdriver.common.by import By

from src.page import page_type

from load_config import *

def _set_download_path(driver, path):
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": path}
    )


def _download_button(driver):
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


def _download(driver, path, url):
    driver.get(url)
    print_log(f"Opened {url}")

    _set_download_path(driver, os.path.dirname(os.path.join(DownloadPath, path)))
    print_log(
        f"Set download directory to {os.path.dirname(os.path.join(DownloadPath, path))}"
    )

    db = _download_button(driver)
    if db:
        db.click()
        print_log(f"Downloaded {path}")
    else:
        print_log(f"No download button found for {path}")


def download(driver, urldict, pathdict, downloadlist):
    try:
        for item in downloadlist:
            _download(driver, item[0], item[1])
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
