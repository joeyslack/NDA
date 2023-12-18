import json

# A data model to be used for report generation. 
# The more strongly typed this is the better. Modify as needed.

company = {
  "description": [],
  "competitors": [],
  "founders": [],
  "staff": [],
}

product = {
  "desciption": [],
}

finance = {
  "history": [],
  "valuation": [],
}

insights = {
  "opportunities": [],
  "concerns": [],
  "questions": [], # {"question": "Text", "answers": []}
}

model = {
  'company': {},
  'staff': [],
  'product': {},
  'finance': {},
  'misc': {}
}

data = {
  company: company,
  product: product,
  finance: finance,
  insights: insights,
}