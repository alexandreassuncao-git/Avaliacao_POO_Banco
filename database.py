import sqlite3

# Conexão com o banco de dados local SQLite
connection = sqlite3.connect('info.db')
cursor = connection.cursor()

# Habilita suporte a chaves estrangeiras (no SQLite vem desativado por padrão)
cursor.execute('PRAGMA foreign_keys = ON;')

def criar_tabelas():
  """Cria a estrutura de tabelas do banco de dados caso ainda não existam."""
  
  # TABELA USUARIOS: Armazena credenciais (com nome único e senha com hash)
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios(
      id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL UNIQUE,
      senha TEXT NOT NULL
    )
  ''')

  # TABELA PROJETOS: Relacionamento 1:N com Usuarios (1 usuário possui N projetos)
  # ON DELETE CASCADE: se o usuário for excluído, seus projetos também são apagados
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS Projetos(
      id_projeto INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL,
      descricao TEXT NOT NULL,
      id_usuario_fk INTEGER NOT NULL,
      FOREIGN KEY (id_usuario_fk) REFERENCES Usuarios(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    )
  ''')

  # TABELA ETAPAS: Relacionamento 1:N com Projetos (1 projeto possui N etapas)
  # CHECK: Garante integridade do status apenas entre os valores permitidos
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS Etapas(
      id_etapa INTEGER PRIMARY KEY AUTOINCREMENT,
      texto TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'pendente' CHECK (status IN ('pendente', 'fazendo', 'concluído')),
      id_projeto_fk INTEGER NOT NULL,
      FOREIGN KEY (id_projeto_fk) REFERENCES Projetos(id_projeto)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    )
  ''')

  # TABELA COMENTARIOS: Relacionamento 1:N com Etapas (1 etapa possui N comentários)
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS Comentarios(
      id_comentario INTEGER PRIMARY KEY AUTOINCREMENT,
      comentario TEXT NOT NULL,
      data TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
      id_etapa_fk INTEGER NOT NULL,
      FOREIGN KEY (id_etapa_fk) REFERENCES Etapas(id_etapa)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    )
  ''')

if __name__ == '__main__':
  criar_tabelas()
  connection.commit()
