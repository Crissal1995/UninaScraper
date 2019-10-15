import requests
import getpass
import pathlib
import urllib3
from urllib.parse import quote, unquote
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
                        UNINA SCRAPER
              Made with <3 by Cristiano Salerno
---
Questo tool è in grado di scaricare tutti i file caricati da un professore su
WebDocenti in maniera automatica, al patto di fornire allo strumento
delle credenziali valide ed essersi iscritti al corso in questione
se l'accesso al materiale è bloccato ad utenti non autenticati.
"""
print(prompt)
print('Inserire le credenziali Unina [username@studenti.unina.it]')
username = input('Username: ')
password = getpass.getpass()
auth = (username, password)

# base path for saving scraped files
basepath = pathlib.Path.cwd() / 'unina_scraper'

# disable warning for don't using SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# lambda for don't writing the same code
rget = lambda url: requests.get(url, auth=auth, verify=False)
mkdir = lambda path: pathlib.Path.mkdir(basepath / path, parents=True, exist_ok=True)

# str formats
search_prof = 'https://www.docenti.unina.it/webdocenti-be/docenti?nome={name}&s=1000'
get_teachings_format = 'https://www.docenti.unina.it/webdocenti-be/docenti/{id_prof}/materiale-didattico/areapubb/?codIns='
get_folders_format = 'https://www.docenti.unina.it/webdocenti-be/docenti/{id_prof}/materiale-didattico/areapubb/{id_}?codIns='
file_format = 'https://www.docenti.unina.it/webdocenti-be/allegati/materiale-didattico/{id_file}'

# 1. select teacher
print()
selected = False
while not selected:
  t_name = quote(input('Inserisci nome e cognome del professore desiderato: '))
  teachers = [Teacher(t) for t in rget(search_prof.format(name=t_name)).json()['content']]
  if not teachers:
    print("Risultato vuoto per", unquote(t_name))
    continue
  elif len(teachers) == 1:
    teacher = teachers[0]
    print("Trovato un solo professore:", teacher)
  else:
    teacher = choice_from_list(teachers, prompt='Selezionare l\'insegnante desiderato: ')
  selected = True

# 2. parse id
id_prof = teacher.id_

# 3. parse teachings
teachings = [Teaching(val) for val in rget(get_teachings_format.format(id_prof=id_prof)).json()]
if not teachings:
  raise ValueError('Il professore {t} non ha alcun insegnamento associato!'.format(t=teacher))
# 3a. select a single teaching
print()
teaching = choice_from_list(teachings, prompt="Scegli un insegnamento: ")
print('\nInsegnamento scelto:\n{t}'.format(t=teaching))
# 3b. parse info from teaching
name = teaching.name
id_teaching = teaching.id_

# 4. get root dir for that teaching
dirjson = rget(get_folders_format.format(id_prof=id_prof, id_=id_teaching)).json()
if dirjson.get('code') and int(dirjson['code']) == 403:
  raise ConnectionRefusedError(
    'Devi essere autenticato ed iscritto al corso '
    'per poter visualizzare questo contenuto!'
  )
rootdir = Directory(dirjson)
if not rootdir.content:
  raise ValueError("La cartella dell'insegnamento è vuota!")
# 4a. create root dir in filesystem too
mkdir(rootdir.path)

# 5. setup dirs to explore
dirs_to_explore = [rootdir]
paths_already_explored = []

# 6. utility function to download all files from dir
#   TODO: check if is already downloaded and,
#   if yes, if last-modified dates match or not
def download_files(directory):
  fs = [f for f in directory.content if f.is_file()]
  def _download(f):
      with open(basepath / directory.path / f.name, 'wb') as handler:
        handler.write(rget(file_format.format(id_file=f.id_)).content)
  
  for f in fs:
    print('Download {} in corso... '.format(f.name), end='', flush=True)
    _download(f)
    print('OK')

# 7. explore all teaching folders
while dirs_to_explore:
  # 7a. get first dir from the ones to explore
  currdir = dirs_to_explore.pop(0)
  # 7b. if it's a File, cast it to Directory with a GET
  if isinstance(currdir, File):
    currdir = Directory(rget(get_folders_format.format(id_prof=id_prof, id_=currdir.id_)).json())
  # 7c. now currdir is a Directory object
  #   but if it was already explored continue to next directory
  if currdir.path in paths_already_explored:
    continue
  # 7d. else I can append its path (that's unique)
  #   to the paths explored
  paths_already_explored.append(currdir.path)
  # 7e. and then I can work
  mkdir(currdir.path)
  download_files(currdir)
  dirs_to_explore += [d for d in currdir.content if d.is_dir()]

# 8. Done
print('Finito! Arrivederci...')
