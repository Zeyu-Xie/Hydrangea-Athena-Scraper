import os
from selenium.webdriver.common.by import By

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
    # print_log(f"Listing files from {driver.current_url}")
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