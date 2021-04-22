
#matrices scribe brutes se trouvent ici: https://dd.weather.gc.ca/model_gem_regional/matrices/land_regions/

 import jinja2

import csv

 

with open('dhcpd.csv', 'rb') as infile:

  reader = csv.reader(infile)

  build = list(reader)

 

 

env = jinja2.Environment(loader=jinja2.FileSystemLoader('/Users/Luca/Git/ztp/templates'))

template = env.get_template('dhcpd-build')

for data in build:

  print template.render(data=build)