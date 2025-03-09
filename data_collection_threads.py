import threading
import time
from dataCollection import search_and_download_images

user_inputs=[]
def input_listener():
    """Function to listen for 'q' input to start the threads"""
    while True:
        try:
            imgs_number = int(input("Enter number of images: "))  # Convert input to integer
            if imgs_number > 0:  # Ensure it's a positive number
                break
            else:
                print("Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    while True:
        
                
        user_input = input("Press 'q' to start the threads: ")
        if user_input.lower() != 'q':
            user_inputs.append(user_input)
        if user_input.lower() == 'q':
            print("Starting threads...")
            # Create 4 threads
            threads = []
            for input_id, query in enumerate(user_inputs):
                thread = threading.Thread(target=worker, args=(input_id,query,imgs_number))
                threads.append(thread)
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            
            break


def worker(thread_id,input,imgs_number):
    """Function that each thread will run"""
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    # Set up the webdriver
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (sometimes needed for headless)
    chrome_options.add_argument("--window-size=1920x1080")  # Set window size to avoid rendering issues
    chrome_options.add_argument("--no-sandbox")  # Helps with running in some environments
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    search_and_download_images(driver,input, int(imgs_number), f'images/{input}')
    time.sleep(5)
    driver.quit()

# Start the input listener
input_listener()
