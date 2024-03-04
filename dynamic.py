import os
from urllib.parse import urlparse
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def extract_data(driver, folder):
    img_sources = []
    videos = []
    links = []
    texts = []

    for img in driver.find_elements(By.TAG_NAME, 'img'):
        img_url = img.get_attribute('src')
        img_sources.append(img_url)
        download_image(img_url, folder)

    for video in driver.find_elements(By.TAG_NAME, 'video'):
        video_url = video.get_attribute('src')
        videos.append(video_url)

    for iframe in driver.find_elements(By.TAG_NAME, 'iframe'):
        if iframe.get_attribute('src'):
            videos.append(iframe.get_attribute('src'))

    for link in driver.find_elements(By.TAG_NAME, 'a'):
        link_url = link.get_attribute('href')
        links.append(link_url)

    for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div']:
        for element in driver.find_elements(By.TAG_NAME, tag):
            texts.append(element.text)

    return img_sources, videos, links, texts

def download_image(url, folder):
    try:
        filename = os.path.join(folder, url.split('/')[-1].split('?')[0])
        with open(filename, 'wb') as f:
            response = requests.get(url)
            if response.status_code == 200:
                f.write(response.content)
            else:
                print(f"Failed to download image from {url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}")
    except FileNotFoundError as e:
        print(f"Error: The specified folder '{folder}' does not exist.")

def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Value'])
    df.to_csv(filename, index=True)
    print(f"Data saved to {filename}")

# Functions Below are Written By Assistance of ChatGPT

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

def scrape_and_save(url, base_folder):
    options = webdriver.EdgeOptions()
    options.add_argument('headless')
    driver = webdriver.Edge(options=options)
    driver.get(url)

    try:
        domain = urlparse(url).netloc
        folder = os.path.join(base_folder, domain)
        if not os.path.exists(folder):
            os.makedirs(folder)

        for _ in range(5):
            scroll_to_bottom(driver)
            img_sources, videos, links, texts = extract_data(driver, folder)

        save_to_csv(img_sources, os.path.join(folder, 'image_data.csv'))
        save_to_csv(videos, os.path.join(folder, 'video_data.csv'))
        save_to_csv(links, os.path.join(folder, 'link_data.csv'))
        save_to_csv(texts, os.path.join(folder, 'text_data.csv'))
    finally:
        driver.quit()

if __name__ == "__main__":
    url = 'https://mastodon.social/explore'
    base_folder = 'Dynamic Websites'  # Base folder to store website-specific folders
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    scrape_and_save(url, base_folder)
