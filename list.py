# Decide which sites to scrape
# Use the [COMPANY_NAME] nomenclature to denote where TARGET variable goes for each site
list = [
  "https://www.crunchbase.com/organization/[COMPANY_NAME]", # https://www.crunchbase.com/organization/[COMPANY_NAME]
  # "https://www.linkedin.com",
  # "https://www.pitchbook.com", # https://my.pitchbook.com/loginAction.do?action=login
  # "https://www.owler.com",
  # https://tracxn.com/?redirect=false ? # Technology + Human-in-the-Loop for Deal Discovery
]

# TODO: Add selectors for each list item, ie:
# selectors = [idx for idx, l in enumerate(list)]
# ... Then grab innerText from each selector, 1->Many list->selector matching. Allow each list item to have many subselectors.
