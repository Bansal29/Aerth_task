# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from pymongo import MongoClient
# import time
# from datetime import datetime
# import requests
# import config

# # MongoDB setup
# client = MongoClient(config.MONGO_URI)
# db = client["Aerth"]
# collection = db["Twitter"]

# # ProxyMesh setup
# PROXYMESH_URL = config.PROXYMESH_URL

# def fetch_trending_topics():
#     # Selenium setup
#     options = Options()
#     options.add_argument(f"--proxy-server={PROXYMESH_URL}")
#     driver = webdriver.Chrome(service=Service('F:\Aerth_task\chromedriver-win64\chromedriver.exe'), options=options)

#     try:
#         # Step 1: Log in to Twitter
#         driver.get("https://x.com/i/flow/login")
#         time.sleep(5)

#         username = driver.find_element(By.NAME, "text")
#         password = driver.find_element(By.NAME, "password")
#         username.send_keys(config.TWITTER_USERNAME)
#         password.send_keys(config.TWITTER_PASSWORD)
#         password.submit()
#         time.sleep(5)

#         # Step 2: Navigate to home page
#         driver.get("https://twitter.com/home")
#         time.sleep(5)

#         # Step 3: Fetch top 5 trends
#         trends = driver.find_elements(By.XPATH, '//span[contains(@class, "css-175oi2r")]')[:5]
#         trend_names = [trend.text for trend in trends]

#         # Step 4: Fetch IP address
#         ip_address = requests.get("https://api.ipify.org").text

#         # Step 5: Store in MongoDB
#         unique_id = str(int(time.time()))
#         timestamp = datetime.now()
#         record = {
#             "_id": unique_id,
#             "trend1": trend_names[0],
#             "trend2": trend_names[1],
#             "trend3": trend_names[2],
#             "trend4": trend_names[3],
#             "trend5": trend_names[4],
#             "timestamp": timestamp,
#             "ip_address": ip_address,
#         }
#         collection.insert_one(record)
#         print("Record stored:", record)

#         return record
#     finally:
#         driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from datetime import datetime
import time
import requests
import os

# Improved: Use environment variables for credentials
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["Aerth"]
collection = db["Twitter"]

def fetch_trending_topics():
    options = Options()
    # Add proxy support if needed
    # options.add_argument(f"--proxy-server={PROXYMESH_URL}") 
    driver = webdriver.Chrome(service=Service('F:\Aerth_task\chromedriver-win64\chromedriver.exe'), options=options)

    try:
        driver.get("https://x.com/i/flow/login")

        # Use WebDriverWait for username and password fields 
        # (These selectors might need to be adjusted based on the latest x.com page structure)
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='text']")) 
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")) 
        )

        username_field.send_keys(TWITTER_USERNAME)
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.submit()

        # Wait for successful login (adjust selector as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "profile-link")) 
        )

        driver.get("https://twitter.com/home")

        # Find trending topics (adjust selector as needed)
        trends = driver.find_elements(By.CSS_SELECTOR, '.css-175oi2r')[:5] 
        trend_names = [trend.text for trend in trends]

        ip_address = requests.get("https://api.ipify.org").text

        unique_id = str(int(time.time()))
        timestamp = datetime.now()
        record = {
            "_id": unique_id,
            "trend1": trend_names[0],
            "trend2": trend_names[1],
            "trend3": trend_names[2],
            "trend4": trend_names[3],
            "trend5": trend_names[4],
            "timestamp": timestamp,
            "ip_address": ip_address,
        }
        collection.insert_one(record)
        print("Record stored:", record)

        return record

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

