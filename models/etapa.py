# DEFINIÇÃO DA ENTIDADE ETAPA

class Etapa:
  def __init__(self, texto: str, id_projeto_fk: int, status: str = 'pendente', id_etapa: int = None):
    self._id_etapa = id_etapa
    self._texto = texto
    self.status = status  # Aciona a validação do @status.setter
    self._id_projeto_fk = id_projeto_fk

  @property
  def id_etapa(self):
    return self._id_etapa

  @property
  def texto(self):
    return self._texto

  @texto.setter
  def texto(self, texto):
    self._texto = texto

  @property
  def status(self):
    return self._status

  @status.setter
  def status(self, status):
    # Regra de negócio: valida se o status pertence às opções do banco
    if status in ('pendente', 'fazendo', 'concluído'):
      self._status = status
    else:
      raise ValueError("Status inválido. Escolha entre: 'pendente', 'fazendo' ou 'concluído'")

  @property
  def id_projeto_fk(self):
    return self._id_projeto_fk

  @id_projeto_fk.setter
  def id_projeto_fk(self, id_projeto_fk):
    self._id_projeto_fk = id_projeto_fk
