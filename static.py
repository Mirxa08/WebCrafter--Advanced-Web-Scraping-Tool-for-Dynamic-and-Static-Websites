import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def extract_text(url, website_folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = soup.find_all('p')

    text_list = [paragraph.get_text() for paragraph in paragraphs]

    with open(f'{website_folder}/text.txt', 'w', encoding='utf-8') as f:
        for text in text_list:
            f.write(text + '\n')


def extract_media_urls(url, website_folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    img_tags = soup.find_all('img')
    audio_tags = soup.find_all('audio')
    video_tags = soup.find_all('video')

    media_folders = ['images', 'audio', 'videos']
    for folder in media_folders:
        folder_path = os.path.join(website_folder, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    counter = 1

    # Using Assistance of ChatGPT for Download Methodology

    # Download images
    for img in img_tags:
        if 'src' in img.attrs:
            image_url = img['src']
            if image_url and not image_url.startswith(("data:image", "//")):
                filename = f"{website_folder}/images/image{counter}.jpg"
                download_media(image_url, filename)
                counter += 1

    # Download audio files
    for audio in audio_tags:
        if 'src' in audio.attrs:
            audio_url = audio['src']
            if audio_url and not audio_url.startswith(("data:audio", "//")):
                filename = f"{website_folder}/audio/audio{counter}.mp3"
                download_media(audio_url, filename)
                counter += 1

    # Extract video links
    for video in video_tags:
        if 'src' in video.attrs:
            video_url = video['src']
            if video_url and not video_url.startswith(("data:video", "//")):
                filename = f"{website_folder}/videos/video{counter}.mp4"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(video_url + '\n')
                counter += 1


def download_media(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Media downloaded successfully as {filename}")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to download media from {url}: {e}")
    except Exception as e:
        print(f"An error occurred while downloading media from {url}: {e}")


url = 'https://docs.autodistill.com'

base_folder = 'Static Websites'  # Base folder to store website-specific folders
domain = urlparse(url).netloc
website_folder = os.path.join(base_folder, domain)

if not os.path.exists(website_folder):
    os.makedirs(website_folder)

if not os.path.exists(website_folder):
    os.makedirs(website_folder)

extract_media_urls(url, website_folder)
extract_text(url, website_folder)
