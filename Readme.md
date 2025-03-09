# 📸 **Automated Image Dataset Collector using Python & Threads**  
**🔍 Multi-threaded Google Image Scraper for Efficient Dataset Collection**  

---

## 📜 **Project Overview**  
This project is designed for **automated dataset collection** by scraping images from **Google Images** using **Selenium and Python threads**. It allows users to efficiently download large datasets for **AI/ML training, research, or other applications**.  

🚀 **Key Features:**  
✅ **Multi-threading:** Faster downloads by running multiple searches in parallel.  
✅ **Progress Tracking:** Displays the percentage of completion for each search.  
✅ **Dataset Organization:** Saves images into categorized folders.  
✅ **Logging:** Stores image URLs in `image_urls.log` for reference.  
✅ **Headless Mode:** Runs Chrome in the background for efficiency.  

---

## 🔧 **Installation & Setup**  

### **📌 Prerequisites**  
Ensure you have **Python 3.x** installed. Then, install the required dependencies:  

```bash
pip install selenium webdriver-manager requests
```

---

### **📌 Running the Script**  

```bash
python dataset_scraper.py
```

🔹 The script will prompt you to:  
- **Enter the number of images per query**  
- **Enter multiple search terms (press `q` to start downloading)**  

---

## 📂 **Project Structure**  

```
📦 Image-Dataset-Collector
│── dataset_scraper.py     # Main script
│── image_urls.log         # Stores extracted image URLs
│── /images/               # Folder where images are saved (organized by search query)
│── README.md              # Project documentation
```

---

## 🎯 **How It Works**  

1️⃣ **User Input:** Enter search queries & number of images to download per query.  
2️⃣ **Multi-threading:** The script launches multiple threads for parallel scraping.  
3️⃣ **Google Image Search:** Selenium automates searching & extracts image URLs.  
4️⃣ **Downloading:** Images are saved in `/images/query_name/`.  
5️⃣ **Progress Display:** Shows real-time completion percentage.  
6️⃣ **Logging:** All image URLs are stored in `image_urls.log`.  

---

## 🚀 **Demo Output**  
```
Enter number of images per query: 5
Enter a search query (or press 'q' to start the threads): cats
Enter a search query (or press 'q' to start the threads): dogs
Enter a search query (or press 'q' to start the threads): q

Starting threads...

🔄 Progress: 3/5 images downloaded (60.00%)
✅ Downloaded 5/5 images (100.00%)
✅ Dataset collection completed!
```

---

## 📌 **Use Cases**  
🔹 **AI & Machine Learning:** Collect image datasets for training models.  
🔹 **Research & Analysis:** Automate large-scale image collection.  
🔹 **Computer Vision