import os
from pathlib import Path
import humanize
from print_log import print_log
from selenium.webdriver.common.by import By
import sys
from time import sleep

from src.page import page_type

from load_config import *

# === Download components ===


class DownloadStatus:

    def __init__(self):
        self.download_dir_set = set([])

    def add_dir(self, download_dir):
        self.download_dir_set.add(download_dir)

    def add_file(self, download_path):
        download_dir = os.path.dirname(download_path)
        self.download_dir_set.add(download_dir)

    def queueLen(self):
        ql = 0
        for download_dir in self.download_dir_set:
            for filename in os.listdir(download_dir):
                if os.path.isdir(filename):
                    continue
                else:
                    if filename.endswith(".crdownload"):
                        ql += 1
        return ql


download_status = DownloadStatus()


def _set_download_path(driver, path):
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": path}
    )


# === Type 1: Download Page ===


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
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    _set_download_path(driver, download_path)
    print_log(f"Set download directory to {download_path}")

    # Get Download Button
    db = _download_button(driver)

    # Download
    if db:
        db.click()
        download_status.add_dir(download_path)
        print_log(f"Downloaded {path}")
    else:
        print_log(f"No download button found for {path}")


# === Type 2: Link Page ===


def _write_link(driver, path):

    # Link Save Path
    link_path = os.path.join(DownloadPath, path + ".txt")
    link_dir = os.path.dirname(link_path)
    os.makedirs(link_dir, exist_ok=True)
    print_log(f"Save Link to {link_path}")

    # Get Link
    frame_id = "ctl00_ContentPlaceHolder_ExtensionIframe"
    div_id = "embedPreview"

    link_content = ""
    try:
        driver.switch_to.frame(frame_id)
        sub_frame = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(sub_frame)
        _div = driver.find_element(By.ID, div_id)
        _a = _div.find_element(By.TAG_NAME, "a")
        link_content = _a.get_attribute("href")
        print_log(f"Detected link: {link_content}")
    except:
        print_log("Failed to locate the link")
    driver.switch_to.default_content()

    # Save Link
    with open(link_path, "w") as f:
        f.write(link_content)


# === Type 3: Group Registration Page ===


def _write_group_registration_info(driver, path):

    # Info Save Path
    info_path = os.path.join(DownloadPath, path + ".txt")
    info_dir = os.path.dirname(info_path)
    os.makedirs(info_dir, exist_ok=True)
    print_log(f"Save group registration info to {info_path}")

    # Get Info
    frame_id = "ctl00_ContentPlaceHolder_ExtensionIframe"
    div_class = "ccl-categorybox-contentpanel"

    text = ""
    try:
        driver.switch_to.frame(frame_id)
        _div_list = driver.find_elements(By.CLASS_NAME, div_class)
        for _div in _div_list:
            text += _div.text + "\n\n"
    except:
        print_log("Failed to read group registration info")
    driver.switch_to.default_content()

    # Save Info
    with open(info_path, "w") as f:
        f.write(text)


# === Type 5: Custom Page ===


def _download_custom_page(driver, path):

    # Page Save Path
    page_path = os.path.join(DownloadPath, path + ".html")

    page_dir = os.path.dirname(page_path)
    os.makedirs(page_dir, exist_ok=True)
    print_log(f"Save custom page to {page_path}")

    # Get Page
    frame_id = "ctl00_ContentPlaceHolder_ExtensionIframe"

    html = ""
    try:
        driver.switch_to.frame(frame_id)
        html = driver.page_source
    except:
        print_log("Failed to fetch custom page")
    driver.switch_to.default_content()

    # Save custom page source
    with open(page_path, "w") as f:
        f.write(html)


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
    elif current_page_type == "Link Page":
        if DownloadLinkPage:
            _write_link(driver, path)
        else:
            print_log("Link Page Ignored by Config")
    elif current_page_type == "Group Registration Page":
        if DownloadGroupRegistrationPage:
            _write_group_registration_info(driver, path)
        else:
            print_log("Group Registration Info Ignored by Config")
    elif current_page_type == "Custom Page":
        if DownloadCustomPage:
            _download_custom_page(driver, path)
        else:
            print_log("Custom Page Ignored by Config")
    else:
        print_log(f"Page Type {current_page_type} not supported")


def download(driver, urldict, pathdict, downloadlist):
    try:
        # Route Pages
        for item in downloadlist:
            print_log("")
            _route_page(driver, item[0], item[1])

        # Summary
        while download_status.queueLen() > 0:
            pass
        folder = Path(DownloadPath)
        size = sum(f.stat().st_size for f in folder.rglob("*") if f.is_file())
        readable_size = humanize.naturalsize(size, binary=True)
        print_log("")
        print_log(
            f"All {len(downloadlist)} files downloaded successfully, total size: {readable_size}."
        )
        driver.quit()
        sys.exit(0)

    except Exception as e:
        print_log(f"Download Failed: {e}")
        driver.quit()
        sys.exit(1)
