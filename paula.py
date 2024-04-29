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
    with psycopg2.connect(host='localhost', user='jslack', dbname='paula_scrape', port='5432') as conn:
      print('Connected to the PostgreSQL server.')
      return conn
  except (psycopg2.DatabaseError, Exception) as error:
    print(error)


if __name__ == '__main__':
  config = load_config(filename='paula.ini')
  # connect(config)

# 1. Load from db
conn = connect(config)
curr = conn.cursor()

# Use argument for start position
start = sys.argv[1] if len(sys.argv) > 1 else 0
print(f"Start at: {start}")
curr.execute(f"SELECT id, linkhref FROM paula WHERE linkhref IS NOT NULL AND id >= {start} ORDER BY id ASC");
rows = curr.fetchall()

for id, link in rows:
  # 2. Open each link in browser
  driver.get(url=f"{link}")
  time.sleep(random.randint(3, 4))

  # 3. Get page content
  # html = driver.find_element(By.XPATH, "//div[contains(@class, 'iWReRk')]")
  # IngredientPagestyles__Content-sc-rgh8tc-1 iWReRk
  try: 
    text = driver.find_element(By.XPATH, "//div[contains(@class, 'iWReRk')]").text
    html = driver.find_element(By.XPATH, "//div[contains(@class, 'iWReRk')]").get_attribute("innerHTML")
  except:
    text = driver.find_element(By.XPATH, "//div[contains(@class, 'jPBQaK')]").text
    html = driver.find_element(By.XPATH, "//div[contains(@class, 'jPBQaK')]").get_attribute("innerHTML")
  
  
  # jPBQaK
  # Escaping
  text = text.replace("'", "\\'")
  html = html.replace("'", "\\'")

  # 4. Update row w/ text & html
  sql = "UPDATE paula SET html=%s, text=%s WHERE id=%s"
  curr.execute(sql, (html, text, id));
  conn.commit()
  print(f"Updated id = {id}")

print('All done. Quitting in 5 seconds...')
time.sleep(5)
curr.close()
conn.close()

# Last ran to: Updated id = 644