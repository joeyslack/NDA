#!/usr/bin/env python3
import json
from jinja2 import Environment, FileSystemLoader
import sys

if (sys.argv[1] is None):
  exit();

f = open(sys.argv[1])
data = json.load(f)
content = 'Content_Data'

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('report/report.html')
output = template.render(content=content)

print(output)