# Scraping for Paula.csv skincare stuff

import time
import re
import random

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

curr.execute(f"SELECT id, linkhref FROM paula WHERE linkhref IS NOT NULL ORDER BY id ASC");
rows = curr.fetchall()

for id, link in rows:
  # 2. Open each link in browser
  driver.get(url=f"{link}")
  time.sleep(random.randint(3, 4))

  # 3. Get page content
  # html = driver.find_element(By.XPATH, "//div[contains(@class, 'iWReRk')]")
  # IngredientPagestyles__Content-sc-rgh8tc-1 iWReRk
  text = driver.find_element(By.XPATH, "//div[contains(@class, 'iWReRk')]").text
  html = driver.find_element(By.XPATH, "//div[contains(@class, 'iWReRk')]").get_attribute("innerHTML")
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


# input("Open the browser, do your full authentication, and press [ENTER] to continue....")

# startRow = 0
# listName = "Ninas List"
# driver.get(url=f"https://www.harmonic.ai/")

# # 2. Save results to table, paginate
# while i <= 201:
#   delay = 3
#   wrapper = WebDriverWait(driver, delay).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, '.cstm-table'))
#   )

#   time.sleep(3)

#   df = driver.find_element(By.CSS_SELECTOR, '.jss31.cstm-table')
#   dfs = pd.read_html(df.get_attribute("outerHTML"))
#   df = dfs[0]
#   df2 = df[['Rank','Company', 'City', 'Country', 'Funding', 'Industry', 'Employees', 'Revenue', 'Emp Growth %']]
#   print(dfs)
#   df2.to_csv('./output/ninaslist.csv', mode='a', index=False, header=False)
#   # with pd.ExcelWriter('./output/growjo.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:  
#     # df2.to_excel(writer, header=False, index=False, startrow=writer.sheets[listName].max_row)
#   print (f"Finished page: {i}, Next is: {i+1}, Next record start @: {startRow}")
  
#   startRow += 51
#   nextButton = driver.find_element(By.XPATH, "//li[@class='next']//a")
#   driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#   nextButton.click()
  
#   time.sleep(3)
#   i = i + 1