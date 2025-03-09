
# from selenium.webdriver.common.by import By
# import time
# import requests
# import os

# def search_and_download_images(driver,query, num_images, save_folder):
#     if not os.path.exists(save_folder):
#         os.makedirs(save_folder)
#         print("make folder")

#     search_url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"
#     driver.get(search_url)
#     print("search..",query)

#     image_urls = set()
#     image_count = 0
#     results_start = 0

#     while image_count < num_images: 
#         thumbnails = driver.find_elements(By.CSS_SELECTOR, "div.czzyk.XOEbc")
        
#         for img in thumbnails[results_start:]:
#             time.sleep(5) 
         
#             try:
#                 img.click() 
#                 time.sleep(5)
                                                              
#                 image = None
#                 while not image:
#                     print("wait")
#                     try:
#                         image = driver.find_element(By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb")
#                         print("here")
#                     except:
#                         time.sleep(1)
#                 src = image.get_attribute('src')
#                 print("src",src)
#                 if src and 'http' in src:
#                     image_urls.add(src)
#                     image_count += 1
#                     if image_count >= num_images:
#                         break
#             except Exception as e:
#                 print(f"Error: {e}")
#                 continue
#         results_start = len(thumbnails)

#     headers = {"User-Agent": "Mozilla/5.0"}
    
#     for i, url in enumerate(image_urls):
#         try:
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()
#             with open(os.path.join(save_folder, f"{query}_{i+1}.jpg"), 'wb') as f:
#                 f.write(response.content)
#         except Exception as e:
#             print(f"Could not download {url} - {e}")

    

# # Example usage

from selenium.webdriver.common.by import By
import time
import requests
import os
from selenium.common.exceptions import NoSuchElementException

def search_and_download_images(driver, query, num_images, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print("Created folder:", save_folder)

    search_url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"
    driver.get(search_url)
    print("Searching for:", query)

    image_urls = set()
    image_count = 0
    results_start = 0

    while image_count < num_images:
        thumbnails = driver.find_elements(By.CSS_SELECTOR, "div.czzyk.XOEbc")

        for img in thumbnails[results_start:]:
            time.sleep(2)  # Reduce wait time a bit
         
            try:
                img.click()
                time.sleep(2)

                # Wait for the larger image to appear (max 10 sec)
                start_time = time.time()
                image = None
                while not image:
                    if time.time() - start_time > 10:  # Timeout after 10 sec
                        print("Timeout: Large image not found, skipping...")
                        break
                    
                    try:
                        image = driver.find_element(By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb")
                        print("Image found!")
                    except NoSuchElementException:
                        time.sleep(1)

                if image:
                    src = image.get_attribute('src')
                    # print("Image URL:", src)
                    
                    if src and 'http' in src:
                        image_urls.add(src)
                        image_count += 1
                        progress = (image_count / num_images) * 100
                        print(f"🔄 Progress {query}: {image_count}/{num_images} images found ({progress:.2f}%)")

                        if image_count >= num_images:
                            break
                    
            except Exception as e:
                print(f"Error clicking image: {e}")
                continue

        results_start = len(thumbnails)

    # Download images
    downloaded_count = 0
    headers = {"User-Agent": "Mozilla/5.0"}
    for i, url in enumerate(image_urls):
        try:
            # ✅ Print updated download progress
            downloaded_count += 1
            progress = (downloaded_count / num_images) * 100
            print(f"✅ Downloaded {downloaded_count}/{num_images} images ({progress:.2f}%)")

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            with open(os.path.join(save_folder, f"{query}_{i+1}.jpg"), 'wb') as f:
                f.write(response.content) 
        except Exception as e:
            print(f"Could not download {url} - {e}")

# Example usage
# search_and_download_images(driver, "puppies", 5, "downloaded_images")
