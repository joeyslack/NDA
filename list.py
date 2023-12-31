from models.report import data
from urllib.parse import urlparse
import undetected_chromedriver as uc
import getpass

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC  # noqa

from models import report as report_model

# path = f'/Users/{getpass.getuser()}/Library/Application Support/Google/Chrome/NDA_Profile'
# options = uc.ChromeOptions()
# driver = uc.Chrome(headless=False, use_subprocess=True, user_data_dir=path)

# Decide which sources to scrape
# Use the [COMPANY_NAME] nomenclature to denote where TARGET variable goes for each site
sources = [
  "https://www.crunchbase.com/organization/[COMPANY_NAME]",
  "https://www.crunchbase.com/organization/[COMPANY_NAME]/company_financials",
  "https://www.crunchbase.com/organization/[COMPANY_NAME]/people",
  "https://www.crunchbase.com/organization/[COMPANY_NAME]/technology",
  "https://www.crunchbase.com/organization/[COMPANY_NAME]/signals_and_news",
  "https://www.crunchbase.com/organization/[COMPANY_NAME]/org_similiarity_overview",
  # "https://www.linkedin.com",
  # "https://www.pitchbook.com", # https://my.pitchbook.com/loginAction.do?action=login
  # "https://www.owler.com",
  # "https://tracxn.com/" # Technology + Human-in-the-Loop for Deal Discovery
  # https://w.tracxn.com/offerings/dd-pack
  # "https://www.harmonic.ai/" # 
]

# TODO: Add selectors for each list item, ie:
# selectors = [idx for idx, l in enumerate(list)]
# ... Then grab innerText from each selector, 1->Many LiteItem->selector matching. 
# Allows each list item to have many subselectors per page

# Selectors represent targets for each List Item. Make sure selectors length is the same as list length.
# For ONE list item, we may have MANY selectors, specified here
selectors = [
  [
    # Company Description
    { 'category': 'company', 'field': 'description', 'element': "driver.find_elements(By.TAG_NAME, 'description-card')[0].text" },
    # Product Description
    { 'category': 'product', 'field': 'description', 'element': "driver.find_elements(By.TAG_NAME, 'description-card')[1].text" },
    
    # Competitors
    # { 'category': 'company', 'field': 'competitors', 'element': "driver.find_elements(By.TAG_NAME, 'description-card')[1].text" },
    
    # Fundraising (History & Valuation)

    # Opportunities

    # Concerns
    # Not sure?

    # Founder Background

    # Key Questions
    # This one isn't perfect, but close enough
    { 'category': 'insights', 'field': 'questions', 'element': "driver.find_elements(By.TAG_NAME, 'phrase-list-card')" },

    # Misc?
    # ? News
    { 'category': 'raw', 'field': 'data', 'element': "driver.find_elements(By.TAG_NAME, 'profile-section')" },
  ], # Selectors for list[0] (ie: "https://www.crunchbase.com/organization/[COMPANY_NAME]")
  [
    # Fundraising (History & Valuation)
    { 'category': 'finance', 'field': 'history', 'element': "driver.find_elements(By.TAG_NAME, 'phrase-list-card')" },
    # { 'category': 'finance', 'field': 'valuation', 'element': "driver.find_elements(By.TAG_NAME, 'description-card')[1].text" },
  ], # Selectors for list[1] (financials)
  [
    { 'category': 'company', 'field': 'staff', 'element': "driver.find_elements(By.TAG_NAME, 'phrase-list-card')" },
  ], # Selectors for list[2] (people)
  [
    { 'category': 'product', 'field': 'technology', 'element': "driver.find_elements(By.TAG_NAME, 'phrase-list-card')" },
  ], # Selectors for list[3] (technology)
  [
    { 'category': 'company', 'field': 'news', 'element': "driver.find_elements(By.TAG_NAME, 'inline-timeline-card')" },
  ], # Selectors for list[4]] (news)
  [
    { 'category': 'company', 'field': 'competitors', 'element': "driver.find_elements(By.TAG_NAME, 'org-similarity-card-item')" },
  ], # Selectors for list[5] (competitors)
]

# def fe():
#   yield driver.find_elements('description-card')[1].text

def evalTarget(driver, x):
  return

def doSelection(driver, x):
  f = driver.find_elements(By.TAG_NAME, 'description-card')
  x = driver.find_elements(By.TAG_NAME, 'description-card')[len(f)-1].text
  return x