# OPERAÇÕES CRUD DA ETAPA (Controller / DAO)
from database import connection, cursor
from models.etapa import Etapa

class EtapaController:

  @classmethod
  def cadastrar(cls, etapa: Etapa) -> int:
    """Insere uma nova etapa vinculada a um projeto."""
    cursor.execute('''
      INSERT INTO Etapas (texto, status, id_projeto_fk)
      VALUES (?, ?, ?)
    ''', (etapa.texto, etapa.status, etapa.id_projeto_fk))
    connection.commit()
    return cursor.lastrowid

  @classmethod
  def listar_por_projeto(cls, id_projeto: int) -> list:
    """Retorna todas as etapas de um projeto ordenadas por ID crescente."""
    cursor.execute('''
      SELECT id_etapa, texto, status, id_projeto_fk
      FROM Etapas
      WHERE id_projeto_fk = ?
      ORDER BY id_etapa ASC
    ''', (id_projeto,))
    return cursor.fetchall()

  @classmethod
  def listar_ids_do_projeto(cls, id_projeto: int) -> list:
    """Retorna a lista de IDs de etapas daquele projeto para validação de entrada."""
    cursor.execute('SELECT id_etapa FROM Etapas WHERE id_projeto_fk = ?', (id_projeto,))
    return [linha[0] for linha in cursor.fetchall()]

  @classmethod
  def atualizar_status(cls, id_etapa: int, novo_status: str) -> bool:
    """Altera o status da etapa ('pendente', 'fazendo' ou 'concluído')."""
    cursor.execute('UPDATE Etapas SET status = ? WHERE id_etapa = ?', (novo_status, id_etapa))
    connection.commit()
    return True

  @classmethod
  def atualizar_texto(cls, id_etapa: int, novo_texto: str) -> bool:
    """Altera o texto/descrição da etapa."""
    cursor.execute('UPDATE Etapas SET texto = ? WHERE id_etapa = ?', (novo_texto, id_etapa))
    connection.commit()
    return True

  @classmethod
  def excluir(cls, id_etapa: int) -> bool:
    """Exclui a etapa (seus comentários são excluídos em cascata)."""
    cursor.execute('DELETE FROM Etapas WHERE id_etapa = ?', (id_etapa,))
    connection.commit()
    return True
