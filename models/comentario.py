# DEFINIÇÃO DA ENTIDADE COMENTÁRIO

class Comentario:
  def __init__(self, comentario: str, id_etapa_fk: int, data: str = None, id_comentario: int = None):
    self._id_comentario = id_comentario
    self._comentario = comentario
    self._data = data
    self._id_etapa_fk = id_etapa_fk

  @property
  def id_comentario(self):
    return self._id_comentario

  @property
  def comentario(self):
    return self._comentario

  @comentario.setter
  def comentario(self, comentario):
    self._comentario = comentario

  @property
  def data(self):
    return self._data

  @property
  def id_etapa_fk(self):
    return self._id_etapa_fk

  @id_etapa_fk.setter
  def id_etapa_fk(self, id_etapa_fk):
    self._id_etapa_fk = id_etapa_fk
