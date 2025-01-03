from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time
from datetime import datetime
import requests
import config

# MongoDB setup
client = MongoClient(config.MONGO_URI)
db = client["Aerth"]
collection = db["Twitter"]

# ProxyMesh setup
PROXYMESH_URL = config.PROXYMESH_URL

def fetch_trending_topics():
    # Selenium setup
    options = Options()
    options.add_argument(f"--proxy-server={PROXYMESH_URL}")
    driver = webdriver.Chrome(service=Service('F:\Aerth_task\chromedriver-win64\chromedriver.exe'), options=options)

    try:
        # Step 1: Log in to Twitter
        driver.get("https://x.com/i/flow/login")
        time.sleep(5)

        username = driver.find_element(By.NAME, "text")
        password = driver.find_element(By.NAME, "password")
        username.send_keys(config.TWITTER_USERNAME)
        password.send_keys(config.TWITTER_PASSWORD)
        password.submit()
        time.sleep(5)

        # Step 2: Navigate to home page
        driver.get("https://twitter.com/home")
        time.sleep(5)

        # Step 3: Fetch top 5 trends
        trends = driver.find_elements(By.XPATH, '//span[contains(@class, "css-901oao")]')[:5]
        trend_names = [trend.text for trend in trends]

        # Step 4: Fetch IP address
        ip_address = requests.get("https://api.ipify.org").text

        # Step 5: Store in MongoDB
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
    finally:
        driver.quit()
