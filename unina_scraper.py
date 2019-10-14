import requests
import getpass
import pathlib
import urllib3
from unina_scraper_model import *

# utility function
def choice_from_list(llist, start=1, prompt='Select a valid number: '):
  n = len(llist)
  for i, val in enumerate(llist):
    print('{idx}: {val}'.format(idx=i+start, val=val))
  choice = start-1
  while not start <= choice < start + n:
    try:
      choice = int(input(prompt))
    except ValueError:
      pass
  return llist[choice-start]

prompt = """
### UNINA SCRAPER ###
Made with <3 by Cristiano Salerno

---
Questo tool è in grado di scaricare tutti i file caricati da un professore su
WebDocenti in maniera automatica, al patto di fornire allo strumento
delle credenziali valide ed essersi iscritti al corso in questione.

L'unico parametro richiesto è l'ID del professore; per ottenerlo basta
semplicemente andare su WebDocenti, aprire la pagina di un professore, e prendere
la lunga stringa di numeri e lettere compresa fra due slash /
"""
print(prompt.strip())
print()
username = input('Username: ')
password = getpass.getpass()
auth = (username, password)
# headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
# id_prof = input('ID del professore: ')
id_prof = '56494e43454e5a4f4d4f534341544f4d534356434e37384d31354331323947'
basepath = pathlib.Path.cwd() / 'unina_scraper'

# disable warning for don't using SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# lambda for don't writing the same code
rget = lambda url: requests.get(url, auth=auth, verify=False)
mkdir = lambda path: pathlib.Path.mkdir(basepath / path, parents=True, exist_ok=True)

# str formats
get_teachings_format = 'https://www.docenti.unina.it/webdocenti-be/docenti/{id_prof}/materiale-didattico/areapubb/?codIns='
get_folders_format = 'https://www.docenti.unina.it/webdocenti-be/docenti/{id_prof}/materiale-didattico/areapubb/{id_}?codIns='
# folder_format = 'https://www.docenti.unina.it/webdocenti-be/docenti/{prof_id}/materiale-didattico/areapubb/{id_}?codIns={cod_ins}'
file_format = 'https://www.docenti.unina.it/webdocenti-be/allegati/materiale-didattico/{id_file}'

teachings = [Teaching(val) for val in rget(get_teachings_format.format(id_prof=id_prof)).json()]
# select a single teaching
teaching = choice_from_list(teachings, prompt='Scegli un insegnamento: ')
print(teaching)
name = teaching.name
id_teaching = teaching.id_
# cod_ins = teaching.cod_inse
# get root dir for that teaching
directory = Directory(rget(get_folders_format.format(id_prof=id_prof, id_=id_teaching)).json())
# create root folder
mkdir(directory.path)
dirs_to_explore = [directory]

def download_files(directory):
  fs = [f for f in directory.content if f.is_file()]
  def _download(f):
      with open(basepath / directory.path / f.name, 'wb') as handler:
        handler.write(rget(file_format.format(id_file=f.id_)).content)
  
  for f in fs:
    print('Download {} in corso...'.format(f.name))
    _download(f)
    print('Download {} terminato!'.format(f.name))


while dirs_to_explore:
  currdir = dirs_to_explore.pop(0)
  if isinstance(currdir, File):
    currdir = Directory(rget(get_folders_format.format(id_prof=id_prof, id_=currdir.id_)).json())
  mkdir(currdir.path)
  download_files(currdir)
  dirs_to_explore += [d for d in directory.content if d.is_dir()]

print('Finito! Arrivederci...')
