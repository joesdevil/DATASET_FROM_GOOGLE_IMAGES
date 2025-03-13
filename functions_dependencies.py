import logging
import random
import requests
import time
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pyfiglet

 


def code_run():
    banner = pyfiglet.figlet_format("Sif Eddine Salem")
    print(banner)
    print("\033[1;32mCredits\033[0m")  # Bold Green Text
    print("\033[1;34m╰┈➤\033[0m")  # Blue Arrow
    print("    \033[1;36m[in] LinkedIn:\033[0m sif eddine salem")  # Cyan Label
    print("     \033[1;33m🖂    Gmail:\033[0m salemsifeddine1@gmail.com")  # Yellow Label
    print("")

def is_connected():
    """Check internet connection."""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def search_and_download_images(driver, query, num_images, save_folder, logger,download_choice):
    """Search and download images, handling network failures."""
    
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        logger.info(f"📁 Created folder: {save_folder}")

    search_url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"
    
    while not is_connected():
        logger.warning(f"⚠️ No internet. Waiting to retry {query}...")
        time.sleep(5)  

    driver.get(search_url)
    logger.info(f"🔍 Searching images for: {query}")

    image_urls = set()
    image_count = 0
    results_start = 0

    while image_count < num_images:
        if not is_connected():
            logger.warning(f"❌ Lost internet. Pausing search for {query}...")
            while not is_connected():
                time.sleep(5)  # Wait for internet recovery
            logger.info(f"✅ Internet restored! Restarting WebDriver for {query}...")
            return "RESTART"

        thumbnails = driver.find_elements(By.CSS_SELECTOR, "div.czzyk.XOEbc")

        for img in thumbnails[results_start:]:
            time.sleep(random.uniform(1.0, 3.5))
            try:
                img.click()
                time.sleep(random.uniform(1.0, 3.5))

                start_time = time.time()
                image = None
                while not image:
                    if time.time() - start_time > 10:
                        break
                    try:
                        image = driver.find_element(By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb")
                    except NoSuchElementException:
                        time.sleep(1)

                if image:
                    src = image.get_attribute('src')
                    if src and 'http' in src:
                        image_urls.add(src)
                        image_count += 1
                        logger.info(f"✅ Found {image_count}/{num_images} images for {query}")

                        if download_choice == "yes":
                            download_image(src, save_folder, f"{query}_{image_count}.jpg",image_count,num_images, logger)

                        if image_count >= num_images:
                            logger.info(f"✨ Successfully collected {num_images} images for '{query}'!")
                            break 

            except Exception:
                pass

        results_start = len(thumbnails)

    if download_choice == "no":
        logger.info(f"📥 Downloading all collected images for '{query}'...")
        for idx, img_url in enumerate(image_urls):
            download_image(src, save_folder, f"{query}_{image_count}.jpg",image_count,num_images, logger)

    return image_urls

def download_image(url, save_folder, filename,image_count,num_images, logger):
    """Download an image from a URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(os.path.join(save_folder, filename), 'wb') as f:
            f.write(response.content)
        logger.info(f"📥 Downloaded: {filename}")
        logger.info(f"⚡ progress: {(image_count/num_images)*100}%")
    except Exception as e:
        logger.warning(f"⚠️ Failed to download {url}: {e}")
