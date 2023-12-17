# from datetime import datetime as dt
import os
import datetime as dt
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException
import pickle
import json
import re
from list import list # list.py
from selenium import webdriver
import getpass

# Use the 'getuser()' function from the 'getpass' module to retrieve the current username.
# Then, print the username to the console.
path = f'/Users/{getpass.getuser()}/Library/Application Support/Google/Chrome/NDA_Profile'
options = uc.ChromeOptions()
driver = uc.Chrome(headless=False, use_subprocess=True, user_data_dir=path)

target_name = input("What is the TARGET NAME? ")

if not target_name:
  print('You must enter a target name. Aborting.')
  exit()

target_site_names = [input(f'ENTITY  NAME for {l}? ') or target_name for l in list]
# result_t = [k for k in range(1,6)]
# print('Start scraping:', list)

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

for idx, l in enumerate(list):
  m = re.search('https?://([A-Za-z_0-9.-]+).*', l)

  # 1. Load cookies?
  #load_cookie(driver, 'cookies/' + l + '.txt')

  # 2. Detect if logged in? 

  # 2a. (not logged in) Do login and save cookie.
  # If using the `auth` method and a full-headed driver, we may not need cookie saving
  # save_cookie(driver, './cookies/' + m.group(1) + '.txt')

  # 2b. Logged in - load path and dump source
  try: 
    driver.get(url=l.replace('[COMPANY_NAME]', target_name[idx]))
  except WebDriverException as e:
    continue

  # For now just take all the source, and parse later
  s = driver.page_source
  os.mkdir('./output/' + target_name)
  f = open('./output/' + target_name + '/'  + m.group(1) + "-" + dt.datetime.utcnow().strftime("%s") + '.txt', "w+")
  #f = open(l, "w")
  f.write(s)
  f.close()