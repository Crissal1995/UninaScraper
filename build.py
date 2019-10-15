#!/usr/bin/env python3
try:
  import python_minifier as mini
  has_mini = True
except ImportError:
  has_mini = False
import os

files = ['unina_scraper_model.py', 'unina_scraper.py']
outfile = 'scraper.py'
lines_first = ["#!/usr/bin/env python3\n"]
lines_after = []
forbidden_lines = ['from unina_scraper_model import *\n']

# clean outfile if it already exists
# otherwise continue
try:
  os.remove(outfile)
except FileNotFoundError:
  pass

with open(outfile, 'a') as out:
  out.writelines(lines_first)
  for f in files:
    fh = open(f)
    ls = fh.readlines()
    out.writelines([l for l in ls if l not in forbidden_lines])
    fh.close()
  out.writelines(lines_after)

if has_mini:
  with open(outfile) as out:
    content = out.read()

  with open(outfile, 'w') as out:
    out.writelines(lines_first)
    out.write(mini.minify(content))
    out.writelines(lines_after)
