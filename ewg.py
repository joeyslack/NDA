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
# options = uc.ChromeOptions()
driver = uc.Chrome(headless=True,use_subprocess=True)

# Database setup
def connect(config):
  """ Connect to the PostgreSQL database server """
  try:
    # connecting to the PostgreSQL server
    with psycopg2.connect(host='localhost', user='jslack', dbname='ewg_scrape', port='5432') as conn:
      print('Connected to the PostgreSQL server.')
      return conn
  except (psycopg2.DatabaseError, Exception) as error:
    print(error)

if __name__ == '__main__':
  config = load_config(filename='ewg.ini')
  # connect(config)

# 1. Load page
category = sys.argv[2] if len(sys.argv) > 2 else "Body"
page = sys.argv[1] if len(sys.argv) > 1 else 1
print("load page with options: ", category, " " , page)

# Connect to db
conn = connect(config)
curr = conn.cursor()

while 1:
  # driver.get(url=f"https://www.ewg.org/skindeep/browse/category/Blush/?category=Blush&sort=score&per_page=9000")
  driver.get(url=f"https://www.ewg.org/skindeep/browse/category/{category}/?page={page}&per_page=1") 

  time.sleep(1)
  # section = driver.find_element(By.XPATH, "//section[contains(@class, 'product_listings')]")
  items = driver.find_element(By.XPATH, "//section[contains(@class, 'product-listings')]")

  insertValues = []
  for item in items.find_elements(By.XPATH, ".//div[contains(@class, 'product-tile')]"):
    #print("inside:", item)
    a0 = item.find_elements(By.XPATH, ".//a")[0]
    a = item.find_elements(By.XPATH, ".//a")[1]
    data1 = a.find_element(By.XPATH, ".//div[contains(@class, 'text-wrapper')]")
    data2 = a.find_element(By.XPATH, ".//div[contains(@class, 'product-data-availability')]")
    id = re.search(r"^https:\/\/www.ewg.org\/skindeep/products\/([0-9]+)", a.get_attribute("href"))

    try: 
      hazard = data2.find_element(By.XPATH, ".//div[contains(@class, 'product-score')]/div[contains(@class, 'verified-text')]").text
    except: 
      hazard = data2.find_element(By.XPATH, ".//div[contains(@class, 'product-score')]/div/div[contains(@class, 'hazard-level')]").text

    insertValues.append([
      category, 
      data1.find_element(By.XPATH, ".//div[contains(@class, 'product-company')]").text,
      data1.find_element(By.XPATH, ".//div[contains(@class, 'product-name')]").text,
      a0.find_element(By.XPATH, ".//img").get_attribute("src"),
      a.get_attribute("href"), 
      hazard
    ])

  #insertValues.append(
  # insertSQL = "INSERT INTO products(category, company, product, image, details, score) VALUES('Blush', '%s', '%s', '%s', '%s', '%s')"

  curr.executemany("INSERT INTO products(category, company, product, image, details, score) VALUES(%s, %s, %s, %s, %s, %s)", insertValues)
  conn.commit()
  print("Inserted rows for page: ", page)
  page = int(page) + 1

print("FINISHED")
conn.close()