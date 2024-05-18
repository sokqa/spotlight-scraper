import os

import requests
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

BASE_URL = "https://windows10spotlight.com"
UNTIL_PAGE = 1106
OUT_FOLDER = "out"


def get_urls_from_page(driver):
    image_class = "wp-post-image"
    img_elements = driver.find_elements(By.CLASS_NAME, image_class)
    image_urls = []
    part_to_remove = "-1024x576"
    for element in img_elements:
        src_url = element.get_attribute("src")
        url = src_url.replace(part_to_remove, "")
        image_urls.append(url)
    return image_urls


def collect_urls(driver):
    image_urls = []
    for page_number in range(1, UNTIL_PAGE + 1):
        url = f"{BASE_URL}/page/{page_number}"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "wp-post-image")))
        urls_from_page = get_urls_from_page(driver)
        image_urls += urls_from_page
    driver.quit()
    return image_urls


def download_images(image_urls):
    os.makedirs(OUT_FOLDER)
    file_name_base = "spotlight_image"
    for index, url in enumerate(image_urls):
        out_path = os.path.join(OUT_FOLDER, f"{file_name_base}_{index + 1}.jpg")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(out_path, "wb") as file:
                for chunk in response:
                    file.write(chunk)
        print(f"File written to {out_path}")


if __name__ == '__main__':
    driver = selenium.webdriver.Firefox()
    image_urls = collect_urls(driver)
    download_images(image_urls)
