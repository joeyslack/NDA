#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader
content = 'This is about page'
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('report/report.html')
output = template.render(content=content)
print(output)