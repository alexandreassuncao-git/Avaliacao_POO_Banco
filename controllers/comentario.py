# OPERAÇÕES CRUD DO COMENTÁRIO (Controller / DAO)
from database import connection, cursor
from models.comentario import Comentario

class ComentarioController:

  @classmethod
  def cadastrar(cls, comentario: Comentario) -> int:
    """Insere um novo comentário vinculado a uma etapa com o horário local do sistema."""
    cursor.execute('''
      INSERT INTO Comentarios (comentario, data, id_etapa_fk)
      VALUES (?, datetime('now', 'localtime'), ?)
    ''', (comentario.comentario, comentario.id_etapa_fk))
    connection.commit()
    return cursor.lastrowid

  @classmethod
  def listar_por_etapa(cls, id_etapa: int) -> list:
    """Retorna os comentários de uma etapa ordenados por ID crescente."""
    cursor.execute('''
      SELECT id_comentario, comentario, data, id_etapa_fk
      FROM Comentarios
      WHERE id_etapa_fk = ?
      ORDER BY id_comentario ASC
    ''', (id_etapa,))
    return cursor.fetchall()

  @classmethod
  def listar_ids_do_projeto(cls, id_projeto: int) -> list:
    """
    Retorna os IDs de comentários de todas as etapas de um projeto.
    Usado para garantir que o usuário só consiga excluir comentários do projeto que está aberto.
    """
    cursor.execute('''
      SELECT c.id_comentario
      FROM Comentarios c
      INNER JOIN Etapas e ON e.id_etapa = c.id_etapa_fk
      WHERE e.id_projeto_fk = ?
    ''', (id_projeto,))
    return [linha[0] for linha in cursor.fetchall()]

  @classmethod
  def excluir(cls, id_comentario: int) -> bool:
    """Exclui um comentário específico pelo seu ID."""
    cursor.execute('DELETE FROM Comentarios WHERE id_comentario = ?', (id_comentario,))
    connection.commit()
    return True
