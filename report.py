#!/usr/bin/env python3
import json
from jinja2 import Environment, FileSystemLoader
import sys
import os

if (sys.argv[1] is None):
  exit();

f = open(sys.argv[1])
data = json.load(f)
content = 'Content_Data'

file_loader = FileSystemLoader('./report')
env = Environment(loader=file_loader)
t = os.path.abspath('report/report.html')
# print(t);
template = env.get_template('report.html')
output = template.render(data=data)

# print(output)
f = open('./output/output.html', "w+")
f.write(output)
f.close()