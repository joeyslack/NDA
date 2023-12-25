#!/usr/bin/env python3
import json
from jinja2 import Environment, FileSystemLoader
import sys
import os

if (sys.argv[1] is None):
  exit();

f = open(sys.argv[1])
data = json.load(f)
head, tail = os.path.split(sys.argv[1])

file_loader = FileSystemLoader('./report')
env = Environment(loader=file_loader)
template = env.get_template('report.html')
output = template.render(data=data)

# print(output)
f = open('./output/' + tail + '_report.html', "w+")
f.write(output)
f.close()