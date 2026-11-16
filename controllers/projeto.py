# OPERAÇÕES CRUD DO PROJETO (Controller / DAO)
from database import connection, cursor
from models.projeto import Projeto

class ProjetoController:

  @classmethod
  def cadastrar(cls, projeto: Projeto) -> int:
    """Insere um novo projeto associado ao usuário logado."""
    cursor.execute('''
      INSERT INTO Projetos (nome, descricao, id_usuario_fk)
      VALUES (?, ?, ?)
    ''', (projeto.nome, projeto.descricao, projeto.id_usuario_fk))
    connection.commit()
    return cursor.lastrowid

  @classmethod
  def listar_por_usuario(cls, id_usuario: int) -> list:
    """
    Retorna os projetos do usuário com a contagem de etapas pendentes.
    LEFT JOIN: garante a exibição mesmo de projetos sem etapas cadastradas.
    COUNT CASE WHEN: contabiliza somente as etapas com status 'pendente'.
    """
    cursor.execute('''
      SELECT 
        Projetos.id_projeto, 
        Projetos.nome, 
        Projetos.descricao, 
        COUNT(CASE WHEN Etapas.status = 'pendente' THEN 1 END) as pendentes
      FROM Projetos
      LEFT JOIN Etapas ON Etapas.id_projeto_fk = Projetos.id_projeto
      WHERE Projetos.id_usuario_fk = ?
      GROUP BY Projetos.id_projeto
    ''', (id_usuario,))
    return cursor.fetchall()

  @classmethod
  def buscar_por_id(cls, id_projeto: int, id_usuario: int):
    """Busca um projeto específico garantindo que pertença ao usuário logado."""
    cursor.execute('''
      SELECT id_projeto, nome, descricao, id_usuario_fk 
      FROM Projetos 
      WHERE id_projeto = ? AND id_usuario_fk = ?
    ''', (id_projeto, id_usuario))
    return cursor.fetchone()

  @classmethod
  def listar_ids_do_usuario(cls, id_usuario: int) -> list:
    """Retorna uma lista simples de IDs de projetos do usuário para validação de entrada."""
    cursor.execute('SELECT id_projeto FROM Projetos WHERE id_usuario_fk = ?', (id_usuario,))
    return [linha[0] for linha in cursor.fetchall()]

  @classmethod
  def atualizar_nome(cls, id_projeto: int, novo_nome: str) -> bool:
    """Atualiza o título/nome de um projeto existente."""
    cursor.execute('UPDATE Projetos SET nome = ? WHERE id_projeto = ?', (novo_nome, id_projeto))
    connection.commit()
    return True

  @classmethod
  def atualizar_descricao(cls, id_projeto: int, nova_descricao: str) -> bool:
    """Atualiza o texto de descrição de um projeto existente."""
    cursor.execute('UPDATE Projetos SET descricao = ? WHERE id_projeto = ?', (nova_descricao, id_projeto))
    connection.commit()
    return True

  @classmethod
  def excluir(cls, id_projeto: int) -> bool:
    """Exclui o projeto do banco (as etapas e comentários vinculados caem em cascata)."""
    cursor.execute('DELETE FROM Projetos WHERE id_projeto = ?', (id_projeto,))
    connection.commit()
    return True
