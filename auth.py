import time
import getpass
from selenium import webdriver
import undetected_chromedriver as uc
from urllib.parse import urlparse
from list import sources

# NOTE: Will create a `NDA_Profile` user in Chrome.
# For simplicity, just log into all of the services using this new profile, trust me it's easier than any alternative currently.
path = f'/Users/{getpass.getuser()}/Library/Application Support/Google/Chrome/NDA_Profile'
options = uc.ChromeOptions()
# options.add_argument(f'--user-data-dir={path}')
# options.add_argument(f'--profile-directory=Profile 1')
# options.add_argument(f"user-data-dir={path}")
# driver = uc.Chrome(headless=False, use_subprocess=True)
driver = uc.Chrome(headless=False, use_subprocess=True, user_data_dir=path) # Force port to fix 'remote debug' issue https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/1639

# # get the 6th child (any tag) of body, and grab all img's within (recursive).
# images = body.children()[6].children('img', True)
# srcs = list(map(lambda _:_.attrs.get('src'), images))

print('~ Authenticating on each source... Ensure you are _LOGGED IN_ on each platform ~')


for idx, l in enumerate(sources):
  # Check only once per original domain
  if idx > 0 and urlparse(list[idx-1]).hostname == urlparse(l).hostname: # Skip if domain is same as last (check once per site)
    break
  driver.get(url=l.replace('[COMPANY_NAME]', 'microsoft'))
  time.sleep(1)
  input ("Verify login status in browser. Authenticate if necessary now... [Press ENTER to continue]")
  time.sleep(1)

time.sleep(1)
