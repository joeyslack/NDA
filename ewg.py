# Scraping for Paula.csv skincare stuff
import time
import re
import random
import sys
# import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import psycopg2
from config import load_config
options = uc.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
driver = uc.Chrome(headless=True,use_subprocess=True, options=options)

# Database setup
def connect(config):
  """ Connect to the PostgreSQL database server """
  try:
    # connecting to the PostgreSQL server
    with psycopg2.connect(**config) as conn:
      print('Connected to the PostgreSQL server.')
      return conn
  except (psycopg2.DatabaseError, Exception) as error:
    print(error)

if __name__ == '__main__':
  config = load_config(filename='ewg.ini')
  # connect(config)

# 1. Load page
category = sys.argv[1] if len(sys.argv) > 1 else "Body"
page = sys.argv[2] if len(sys.argv) > 2 else 1
count = sys.argv[3] if len(sys.argv) > 3 else 1000

# Usage: `python ewg.py Body 1 1000` {Category Page Count}
print("load page with options. Category: ", category, " Page: " , page, " Count: ", count)

# Connect to db
conn = connect(config)
curr = conn.cursor()

while 1:
  driver.get(url=f"https://www.ewg.org/skindeep/browse/category/{category}/?page={page}&per_page={count}") 

  time.sleep(10)
  start = driver.find_element(By.XPATH, "//section[contains(@class, 'product-listings')]")
  items = start.find_elements(By.XPATH, ".//div[contains(@class, 'product-tile')]")

  if items is None or items.count == 0 or  len(items) < 1:
    break

  insertValues = []
  for item in items:
    #print("inside:", item)
    a0 = item.find_elements(By.XPATH, ".//a")[0]
    a = item.find_elements(By.XPATH, ".//a")[1]
    data1 = a.find_element(By.XPATH, ".//div[contains(@class, 'text-wrapper')]")
    data2 = a.find_element(By.XPATH, ".//div[contains(@class, 'product-data-availability')]")
    find = re.search(r"^https:\/\/www.ewg.org\/skindeep/products\/([0-9]+)", a.get_attribute("href"))
    
    try:
      find = re.search(r"^https:\/\/www.ewg.org\/skindeep/products\/([0-9]+)", a.get_attribute("href"))
      id = find.group(1)
    except:
      # Alternative URL
      # https://www.ewg.org/sunscreen/about-the-sunscreens/1074787/ATTITUDE_Sunly_Lip_Balm_Coconut_SPF_15
      find = re.search(r"^https:\/\/www.ewg.org\/[a-zA-Z\-\_]+/[a-zA-Z\-\_]+\/([0-9]+)", a.get_attribute("href"))
      if find is None or find.group is None or find.group(1) is None:
        print('No ID available, skipping...', a.get_attribute("href"), data1.find_element(By.XPATH, ".//div[contains(@class, 'product-company')]").text), 
        continue
      id = find.group(1)
      
    try: 
      hazard = data2.find_element(By.XPATH, ".//div[contains(@class, 'product-score')]/div[contains(@class, 'verified-text')]").text
    except: 
      hazard = data2.find_element(By.XPATH, ".//div[contains(@class, 'product-score')]/div/div[contains(@class, 'hazard-level')]").text

    # Values are repeated for use of ON CONFLICT condition. First set is 7 values, Second is 6.
    insertValues.append([
      id,
      category, 
      data1.find_element(By.XPATH, ".//div[contains(@class, 'product-company')]").text,
      data1.find_element(By.XPATH, ".//div[contains(@class, 'product-name')]").text,
      a0.find_element(By.XPATH, ".//img").get_attribute("src"),
      a.get_attribute("href"), 
      hazard,
      category, 
      data1.find_element(By.XPATH, ".//div[contains(@class, 'product-company')]").text,
      data1.find_element(By.XPATH, ".//div[contains(@class, 'product-name')]").text,
      a0.find_element(By.XPATH, ".//img").get_attribute("src"),
      a.get_attribute("href"), 
      hazard,
    ])

  curr.executemany("INSERT INTO products(id, category, company, product, image, details, score) VALUES(%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET (category, company, product, image, details, score) = (%s, %s, %s, %s, %s, %s)", insertValues)
  conn.commit()
  print("Inserted rows for page: ", page)
  page = int(page) + 1

print("FINISHED")
conn.close()