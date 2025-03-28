from selenium.webdriver.common.by import By


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
        _div = driver.find_element(By.ID, div_id)
        _a = _div.find_element(By.TAG_NAME, "a")
        return True
    except:
        return False


def is_group_registration_page(driver):
    driver.switch_to.default_content()
    h1_xpath = "//h1[text()='Group registration']"
    try:
        if driver.find_element(By.XPATH, h1_xpath):
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
            t = driver.find_element(By.XPATH, h1_xpath)
            print(t.text)
            return True
        return False
    except:
        return False


def page_type(driver):

    pt = "Unrecognized Page"

    if is_download_page(driver):
        pt = "Download Page"
    elif is_link_page(driver):
        pt = "Link Page"
    elif is_group_registration_page(driver):
        pt = "Group Registration Page"
    elif is_discussion_page(driver):
        pt = "Discussion Page"
    elif is_custom_page(driver):
        pt = "Custom Page"
    else:
        pt = "Unrecognized Page"

    driver.switch_to.default_content()
    return pt
