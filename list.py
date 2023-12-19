from models.report import data
from urllib.parse import urlparse

# Decide which sites to scrape
# Use the [COMPANY_NAME] nomenclature to denote where TARGET variable goes for each site
list = [
  "https://www.crunchbase.com/organization/[COMPANY_NAME]", # https://www.crunchbase.com/organization/[COMPANY_NAME]
  "https://www.crunchbase.com/organization/[COMPANY_NAME]/company_financials",
  "https://www.crunchbase.com/organization/[COMPANY_NAME]/technology",
  "https://www.crunchbase.com/organization/[COMPANY_NAME]/signals_and_news",
  # "https://www.linkedin.com",
  # "https://www.pitchbook.com", # https://my.pitchbook.com/loginAction.do?action=login
  # "https://www.owler.com",
  # "https://tracxn.com/" # Technology + Human-in-the-Loop for Deal Discovery
]

# TODO: Add selectors for each list item, ie:
# selectors = [idx for idx, l in enumerate(list)]
# ... Then grab innerText from each selector, 1->Many LiteItem->selector matching. 
# Allows each list item to have many subselectors per page

selectors = [

]


data['company']['description'] = 'description-card'