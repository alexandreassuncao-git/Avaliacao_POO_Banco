# DEFINIÇÃO DA ENTIDADE USUÁRIO
from hashlib import sha256

class Usuario:
  def __init__(self, nome: str, senha: str, id_usuario: int = None, senha_hash: bool = False):
    # Atributos protegidos/privados (Encapsulamento em POO)
    self._id_usuario = id_usuario
    self._nome = nome
    
    # Se a senha já vier como hash do banco, armazena direto sem re-hashear
    if senha_hash:
      self.__senha = senha
    else:
      self.senha = senha  # Aciona o @senha.setter para criptografar com SHA-256

  @property
  def id_usuario(self):
    return self._id_usuario

  @property
  def nome(self):
    return self._nome

  @nome.setter
  def nome(self, nome):
    self._nome = nome

  @property
  def senha(self):
    return self.__senha

  @senha.setter
  def senha(self, senha):
    # Converte a senha para bytes em UTF-8 e gera o resumo hexadecimal em SHA-256
    self.__senha = sha256(senha.encode('utf-8')).hexdigest()

  def validar_senha(self, senha_digitada: str) -> bool:
    """Verifica se a senha digitada em texto puro confere com o hash salvo."""
    return self.__senha == sha256(senha_digitada.encode('utf-8')).hexdigest()