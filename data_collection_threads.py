import threading
import os
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dataCollection import search_and_download_images , code_run


code_run()
# Ensure the logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")


import logging
import os

def setup_logger(query):
    """Creates and returns a logger for a specific query."""
    
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Ensure the logs/ directory exists
    log_filename = os.path.join(log_dir, f"{query}.log")

    logger = logging.getLogger(query)
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers
    if not logger.hasHandlers():
        file_handler = logging.FileHandler(log_filename, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(console_handler)

        logger.propagate = False  # Prevent duplicate logging

    return logger


def worker(thread_id, query, imgs_number,download_choice):
    """Thread function to scrape and download images."""
    logger = setup_logger(query)
    logger.info(f"🔍 Thread {thread_id} started for query: {query}")

    while True:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920x1080")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

            result = search_and_download_images(driver, query, imgs_number, f'images/{query}', logger,download_choice)

            driver.quit()

            if result == "RESTART":
                logger.info(f"🔄 Restarting WebDriver for {query} due to network recovery...")
                continue  # Restart loop
            
            break  

        except Exception as e:
            logger.warning(f"⚠️ Error in thread {thread_id}: {e}")

        finally:
            try:
                driver.quit()
            except:
                pass  

def input_listener():
    """Get user input and start threads."""
    user_inputs = []
    
    while True:
        try:

            imgs_number = int(input("Enter number of images: "))  

            if imgs_number > 0:
                break
            else:
                print("Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        choice = input("Do you want to download images instantly? (yes/no): ").strip().lower()
        if choice in ["yes", "no"]:
            break
        print("Invalid choice. Please enter 'yes' or 'no'.")

    while True:
        user_input = input("Enter search query (or press 'q' to start): ")
        if user_input.lower() != 'q':
            user_inputs.append(user_input)
        if user_input.lower() == 'q':
            if len(user_inputs) > 0:
                print("🚀 Starting search...")

            threads = []
            for input_id, query in enumerate(user_inputs):
                thread = threading.Thread(target=worker, args=(input_id, query, imgs_number,choice))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            break

# Run the script
input_listener()
