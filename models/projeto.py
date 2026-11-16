# DEFINIÇÃO DA ENTIDADE PROJETO

class Projeto:
  def __init__(self, nome: str, descricao: str, id_usuario_fk: int, id_projeto: int = None):
    # Atributos protegidos (Encapsulamento)
    self._id_projeto = id_projeto
    self._nome = nome
    self._descricao = descricao
    self._id_usuario_fk = id_usuario_fk

  @property
  def id_projeto(self):
    return self._id_projeto

  @property
  def nome(self):
    return self._nome

  @nome.setter
  def nome(self, nome):
    self._nome = nome

  @property
  def descricao(self):
    return self._descricao

  @descricao.setter
  def descricao(self, descricao):
    self._descricao = descricao

  @property
  def id_usuario_fk(self):
    return self._id_usuario_fk

  @id_usuario_fk.setter
  def id_usuario_fk(self, id_usuario_fk):
    self._id_usuario_fk = id_usuario_fk
