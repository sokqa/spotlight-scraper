import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://windows10spotlight.com/"
UNTIL_PAGE = 1106


def get_urls_from_page(driver):
    image_class = "wp-post-image"
    img_elements = driver.find_elements(By.CLASS_NAME, image_class)
    image_urls = [element.get_attribute("src") for element in img_elements]
    return image_urls


def collect_urls(driver):
    image_urls = []
    for page_number in range(1, UNTIL_PAGE + 1):
        url = f"{BASE_URL}/page/{page_number}"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "wp-post-image")))
        urls_from_page = get_urls_from_page(driver)
        image_urls.append(*urls_from_page)
    return image_urls


if __name__ == '__main__':
    driver = selenium.webdriver.Firefox()
    collect_urls(driver)
