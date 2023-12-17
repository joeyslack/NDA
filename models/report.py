import json

# A data model to be used for report generation. 
# The more strongly typed this is the better. Modify as needed.
model = {
  'company': {},
  'staff': [],
  'product': {},
  'finance': {},
  'misc': {}
}

json.dumps(model)