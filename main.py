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

INF = 2**31 - 1
config_path = os.path.join(os.path.dirname(__file__), "config.yaml")


def read_config():
    with open(config_path, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


config = read_config()
FolderID = config["FolderID"]
DownloadPath = os.path.join(
    config["DownloadPath"], "Athena_" + datetime.now().strftime("%Y%m%d%H%M%S%f")
)
AutoLogin = config["AutoLogin"]
Username = config["Username"]
Password = config["Password"]
CommandLineLog = config["CommandLineLog"]
FileLog = config["FileLog"]
FileLogPath = os.path.join(DownloadPath, "log.txt")


def print_log(msg):
    global CommandLineLog, FileLog, FileLogPath
    log = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]}] {msg}"
    if CommandLineLog:
        print(log)
    if FileLog:
        with open(FileLogPath, "a") as f:
            f.write(log + "\n")


def is_logged_in(driver):
    url = driver.current_url
    if "athena.itslearning.com/main.aspx?TextURL=CourseCards" in url:
        return True
    elif "athena.itslearning.com/CourseCards" in url:
        return True
    else:
        return False


def set_download_path(driver, path):
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": path}
    )


def _list_files(driver):
    filedict = {}
    list = driver.find_elements(By.CLASS_NAME, "prom-link--primary")
    for item in list:
        filename = item.text
        filelink = item.get_attribute("href")
        filedict[filename] = filelink
    return filedict


def list_files(driver, _visited=None):
    if _visited is None:
        _visited = set()
    print_log(f"Listing files from {driver.current_url}")
    filedict = _list_files(driver)
    keys = list(filedict.keys())
    for key in keys:
        url = filedict[key]
        if "FolderID" in url and url not in _visited:
            _visited.add(url)
            driver.get(url)
            filedict[key] = list_files(driver, _visited)
            driver.back()
    return filedict


def list_paths(files, _path=""):
    pathdict = {}
    for filename in files:
        if isinstance(files[filename], dict):
            pathdict[filename] = list_paths(
                files[filename], os.path.join(_path, filename)
            )
        else:
            pathdict[filename] = os.path.join(_path, filename)
    return pathdict


def list_downloads(driver, pathdict, urldict, _bp="", _files=[]):
    if type(pathdict) == str:
        _files.append((_bp, urldict))
        return _files
    else:
        for path in pathdict:
            new_bp = os.path.join(_bp, path)
            list_downloads(driver, pathdict[path], urldict[path], new_bp, _files)
        return _files


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

    print("Hydrangea Athena Downloader © 2024 by Acan. All rights reserved.")
    if not os.path.exists(DownloadPath):
        os.makedirs(DownloadPath, exist_ok=True)
        print_log("Download Path Created")
    prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    print_log("Chrome Options Set")
    options = Options()
    options.add_experimental_option("prefs", prefs)
    print_log(f"Download Path: {DownloadPath}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.set_page_load_timeout(INF)
    print_log("Driver Started")

    driver.get("https://athena.itslearning.com/main.aspx?TextURL=CourseCards")
    print_log("Opened Athena")

    if not AutoLogin:
        print_log("Auto Login Disabled by Config")
        while not is_logged_in(driver):
            pass
        print_log("Login Successful")
    else:
        print_log("Auto Login Enabled by Config, Logging in")
        try:
            element = WebDriverWait(driver, INF).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "itsl-native-login-button")
                )
            )
            _to_login = driver.find_element(By.CLASS_NAME, "itsl-native-login-button")
            _to_login.click()
            print_log("Clicked Login Button")
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
            print_log("Filled in Username and Password")
            _login = driver.find_element(By.NAME, "_eventId_proceed")
            _login.click()
            print_log("Clicked Login Submit Button")
            while not is_logged_in(driver):
                if "Incorrect username or password." in driver.page_source:
                    raise Exception("Incorrect username or password.")
        except Exception as e:
            print_log(f"Login Failed: {e}")
            driver.quit()
            sys.exit(1)
        print_log("Login Successful")

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
