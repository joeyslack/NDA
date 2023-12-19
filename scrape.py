import os
import datetime as dt
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC  # noqa
import pickle
import getpass
import json
import re
from urllib.parse import urlparse
from list import sources, selectors, doSelection # list.py
from models import report as report_model
from selenium import webdriver

path = f'/Users/{getpass.getuser()}/Library/Application Support/Google/Chrome/NDA_Profile'
options = uc.ChromeOptions()
driver = uc.Chrome(headless=False, use_subprocess=True, user_data_dir=path)

target_name = input("What is the COMPANY NAME? ")

if not target_name:
  print('You must enter a COMPANY NAME. Aborting.')
  exit()

# Assign [COMPANY_NAME] overrides on a UNIQUE per-site basis, 
# in case that the organization variable is named differently on different sources (high probability)
target_site_names = {}
# target_site_names = [input(f'Override COMPANY NAME? for { urlparse(l).hostname }? ') or target_name for l in list]
for l in sources:
  h = urlparse(l).hostname
  if h not in target_site_names:
    target_site_names[h] = input(f'Override COMPANY NAME? for { h }? ') or target_name

def do_login():
  print('do_login')

def save_cookie(driver, path):
  with open(path, 'wb+') as filehandler:
    a = driver.get_cookies()
    pickle.dump(a, filehandler)
    # print(driver.get_cookies())

def load_cookie(driver, path):
  with open(path, 'rb') as cookiesfile:
    cookies = pickle.load(cookiesfile)
    for cookie in cookies:
      driver.add_cookie(cookie)

for idx, l in enumerate(sources):
  m = re.search('https?://([A-Za-z_0-9.-]+).*', l)
  
  if not os.path.exists('./output/' + target_name):
    os.mkdir('./output/' + target_name)
 
  # 1. Load cookies?
  #load_cookie(driver, 'cookies/' + l + '.txt')

  # 2. Detect if logged in? 

  # 2a. (not logged in) Do login and save cookie.
  # If using the `auth` method and a full-headed driver, we may not need cookie saving
  # save_cookie(driver, './cookies/' + m.group(1) + '.txt')
  path = './output/' + target_name + '/'

  # 2b. Logged in - load path and dump source
  try: 
    # Open target
    driver.get(url=l.replace('[COMPANY_NAME]', target_site_names[urlparse(l).hostname]))    
    
    # Save screenshot (can be parsed later by OCR if we wish, nice to keep)
    driver.save_screenshot(os.path.abspath(path) + m.group(1) + '.png')

    # Get selectors for each source, and grab the data
    # if idx == 0: # Only run on first?
    #   report_model.data['company']['description'] = driver.find_elements(By.TAG_NAME, report_model.data['company']['description'])[1].text
    # if idx == 2:
    #   report_model.data['product']['description'] = driver.find_elements(By.TAG_NAME, 'profile-section').text

    # TODO: Add modeled data here, taken from targets (ie: driver.find_element(By.XPATH, '//input[@name="q"]'))
    if idx < len(selectors):
      
      input("Continue...") # Pausing each page load for debugging purposes, forces browser to stay open until [Enter]

      for s in selectors[idx]:
        # Assign text from selectors to our report_model (data.category_name.field_name)
        try: 
          items = eval(s['element'])
          
          # If our selector returns multiple matches...
          if isinstance(items, list):
            for i in items:
              print('isList::', i, i.text)
              report_model.data[s['category']][s['field']].append(i.text)
            # report_model.data[s['category']][s['field']].append(items)
          # Selector returns a single result, append
          else:
            report_model.data[s['category']][s['field']].append(items)
        # Should probably do something with exceptions here...
        except: continue
        
    # profile-section
    
  except WebDriverException as e:
    print(e)
    continue

  # For now just take all the source, and parse later
  s = driver.page_source

  # Save source to output dir 
  # See: https://github.com/ultrafunkamsterdam/undetected-chromedriver/blob/master/example/example.py for target examples
  f = open('./output/' + target_name + '/'  + m.group(1) + "-" + dt.datetime.utcnow().strftime("%s") + '.txt', "w+")
  f.write(s)
  f.close()

  
  # Find all images (currently for no particular reason). Maybe save them somewhere?
  # imgs = driver.find_elements(By.TAG_NAME, 'img')
  # for item in imgs:
  #   if item.get_attribute('src') is not None:
  #     print(item.get_attribute('src'))

  # sections = driver.find_elements(By.TAG_NAME, 'profile-section')
  # raw_sections
  # for item in sections:
  #   print(item.text)
  # Write data to json
  f = open('./output/' + target_name + '/'  + urlparse(l).hostname + '.json', "w+")
  f.write(json.dumps(report_model.data))
  f.close()

print('Data Model: \n', report_model.data)
input('Press [Enter] to finish')