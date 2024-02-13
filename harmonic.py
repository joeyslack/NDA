import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = uc.ChromeOptions()
driver = uc.Chrome(headless=False, use_subprocess=True)

# Harmonic needs an active session, 1 tab only, can't re-use cookies without triggering detection.
# to circumvent:
# 1. Start this script, and pause, as we login/auth appropriately, using the uc_chrome here.
input("Open the browser, do your full authentication, and press [ENTER] to continue....")

startRow = 0
listName = "Ninas List"
driver.get(url=f"https://www.harmonic.ai/")

# 2. Save results to table, paginate
while i <= 201:
  delay = 3
  wrapper = WebDriverWait(driver, delay).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.cstm-table'))
  )

  time.sleep(3)

  df = driver.find_element(By.CSS_SELECTOR, '.jss31.cstm-table')
  dfs = pd.read_html(df.get_attribute("outerHTML"))
  df = dfs[0]
  df2 = df[['Rank','Company', 'City', 'Country', 'Funding', 'Industry', 'Employees', 'Revenue', 'Emp Growth %']]
  print(dfs)
  df2.to_csv('./output/ninaslist.csv', mode='a', index=False, header=False)
  # with pd.ExcelWriter('./output/growjo.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:  
    # df2.to_excel(writer, header=False, index=False, startrow=writer.sheets[listName].max_row)
  print (f"Finished page: {i}, Next is: {i+1}, Next record start @: {startRow}")
  
  startRow += 51
  nextButton = driver.find_element(By.XPATH, "//li[@class='next']//a")
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
  nextButton.click()
  
  time.sleep(3)
  i = i + 1