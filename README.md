<h2>Descrizione</h2>

Unina Scraper è un tool da linea di comando in grado di scaricare in maniera automatica il contenuto di una folder associata ad un insegnante.

Il tool è in grado di cercare nel database degli insegnanti in base ad una ricerca testuale, e dopo averne scelto uno è possibile vedere la sua lista di insegnamenti. 
Scelto anche l'insegnamento, partirà il download automatico di tutti i file presenti nella cartella.

Verrà mantenuta la struttura di file e cartelle adottata dal professore.

<h2>Utilizzo</h2>

Per poter utilizzare il tool è necessario installare [Python 3] e la libreria [Requests].

Una volta installato Python, digitare da linea di comando (PowerShell o Terminale dei Comandi su Windows, bash su Unix):
```bash
python -m pip install --user requests   # questo comando installerà la libreria
python scraper.py                       # questo comando lancerà lo script
```
<h3>Problemi</h3>

* ```SyntaxError: Non-ASCII character '\xXX' in file scraper.py on line YY```
  
  Stai utilizzando Python 2, riprova utilizzando `python3` al posto di `python`.

[Python 3]: https://www.python.org/downloads/
[requests]: https://it.python-requests.org/it/latest/
