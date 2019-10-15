import string

# utility for fixing unina upper names
def fix_name(name, delimiter=' ', split='_'):
  if not name:  # empty or None
    return ''
  name = delimiter.join(elem.capitalize() for elem in name.split(split))
  if name[0] not in string.ascii_letters:
    name = name[1].upper() + name[2:]
  return name

class Teacher:
  def __init__(self, d):
    self._parse_from_vals(
      d.get('id'), d.get('nome'), d.get('cognome'), d.get('dipartimento')
    )
  
  def _parse_from_vals(self, id_, name, surname, dipartimento):
    self.id_ = id_
    self.name = fix_name(name, split=' ')
    self.surname = fix_name(surname, split=' ')
    self.dipartimento = fix_name(dipartimento, split='-').strip()
  
  def __str__(self):
    return '{name} {surname} (dipartimento {dip})'.format(
      name=self.name, surname=self.surname, 
      dip=self.dipartimento if self.dipartimento else 'mancante'
    )

class Teaching:
  def __init__(self, d):
    self._parse_from_vals(
      d.get('nome', ''), d.get('id'), d.get('pubblica'), 
      d.get('libera'), d.get('codInse'), d.get('tipo'), 
      d.get('percorso'), d.get('dataInserimento'), d.get('cancella')
    )
     
  def _parse_from_vals(self, name, id_, public, free, cod_inse, type_, path, insert_date, delete):
    self.name = fix_name(name)
    self.id_ = id_
    self.public = public
    self.free = free
    self.cod_inse = cod_inse
    self.type_ = type_
    self.path = path
    self.insert_date = insert_date
    self.delete = delete
    
  def __str__(self):
    return '{id_} - {name} (cod insegnamento {codins})'.format(id_=self.id_, name=self.name, codins=self.cod_inse)

class Directory:
  def __init__(self, d):
    self._parse_from_vals(
      d.get('percorso'), d.get('libera'), d.get('directory'), d.get('pubblica'), 
      d.get("contenutoCartella", []), d.get("listaInsegnamenti", []), d.get("cancella")
    )
  
  def _parse_from_vals(self, path, free, isdir, public, content, teachings, delete):
    self.path = fix_name(path, delimiter='_')
    self.free = free
    self.isdir = isdir
    self.public = public
    self.content = [File(v) for v in content]
    self.teachings = teachings
    self.delete = delete
    
  def __str__(self):
    return '[DIR] path is {} and content is:\n{}'.format(self.path, [str(c) for c in self.content])

class File:
  def __init__(self, d):
    self._parse_from_vals(
      d.get('nome', ''), d.get('id'), d.get('pubblica'), d.get('libera'), 
      d.get("tipo"), d.get("percorso", ''), d.get("dataInserimento"), d.get('codInse')
    )
    
  def _parse_from_vals(self, name, id_, public, free, type_, path, timestamp, cod_ins):
    self.name = name
    self.id_ = id_
    self.path = fix_name(path, delimiter='_')
    self.public = public
    self.free = free
    self.type_ = type_
    self.timestamp = float(timestamp) if timestamp else None
    self.cod_ins = cod_ins
    assert self.is_file() or self.is_dir(), 'Element is neither a file nor a dir!'
  
  def is_file(self):
    return self.type_.lower() == 'f'
  
  def is_dir(self):
    return self.type_.lower() == 'd'
    
  def __str__(self):
    return '[{type_}] {name} (id {id_})'.format(type_='FILE' if self.is_file() else 'DIR', name=self.name, id_=self.id_)

