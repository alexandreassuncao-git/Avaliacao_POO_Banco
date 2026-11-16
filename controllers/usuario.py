# OPERAÇÕES CRUD DO USUÁRIO (Controller / DAO)
from database import connection, cursor
from models.usuario import Usuario

class UsuarioController:
  
  @classmethod
  def cadastrar(cls, usuario: Usuario) -> int:
    """Insere um novo usuário no banco com a senha já criptografada."""
    cursor.execute('''
      INSERT INTO Usuarios (nome, senha)
      VALUES (?, ?)
    ''', (usuario.nome, usuario.senha))
    connection.commit()
    return cursor.lastrowid

  @classmethod
  def listar_nomes(cls) -> list:
    """Retorna uma lista com os nomes de todos os usuários (usado para checar duplicidade)."""
    cursor.execute('SELECT nome FROM Usuarios')
    return [linha[0] for linha in cursor.fetchall()]

  @classmethod
  def buscar_por_nome(cls, nome: str):
    """Busca o usuário pelo nome para login e reconstitui o objeto Usuario com seus dados."""
    cursor.execute('SELECT id_usuario, nome, senha FROM Usuarios WHERE nome = ?', (nome,))
    resultado = cursor.fetchone()

    if resultado:
      # Desestruturação
      id_usuario, nome_banco, senha_banco = resultado
      # Reconstrói a instância de Usuario mantendo o hash original do banco
      return Usuario(nome=nome_banco, senha=senha_banco, id_usuario=id_usuario, senha_hash=True)
    return None
