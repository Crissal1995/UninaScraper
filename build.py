import python_minifier as mini
import os

files = ['unina_scraper_model.py', 'unina_scraper.py']
outfile = 'scraper_minified.py'
forbidden_lines = ['from unina_scraper_model import *\n']

# clean outfile if it already exists
os.remove(outfile)

with open(outfile, 'a') as out:
    for f in files:
        fh = open(f)
        ls = fh.readlines()
        out.writelines([l for l in ls if l not in forbidden_lines])
        fh.close()

with open(outfile) as out:
    content = out.read()

with open(outfile, 'w') as out:
    out.write(mini.minify(content))