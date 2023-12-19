import json

# Data Models to be used for report generation. Each keyed entry should be appended array.
# The more strongly typed this is the better. Modify as needed.

company = {
  "description": [],
  "competitors": [],
  "founders": [],
  "staff": [],
}

product = {
  "description": [],
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

# Some kind of raw dump catchall to throw unstructured data
raw = {
  'data': []
}

# Container
data = {
  'company': company,
  'product': product,
  'finance': finance,
  'insights': insights,
  'raw': raw,
}