# 🚀 Gerenciador de Projetos e Tarefas (CLI)

Sistema de linha de comando (CLI) para gerenciamento de projetos, etapas e comentários, desenvolvido em **Python** integrando os conceitos de **Programação Orientada a Objetos (POO)**, persistência relacional em **SQLite** e interface interativa estilizada com a biblioteca **Rich**.

---

## 📌 Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura do Sistema (MVC)](#-arquitetura-do-sistema-mvc)
- [Tecnologias e Dependências](#-tecnologias-e-dependências)
- [Como Instalar e Executar](#-como-instalar-e-executar)
- [Instruções de Uso](#-instruções-de-uso)
- [Modelagem do Banco de Dados](#-modelagem-do-banco-de-dados)

---

## 📖 Sobre o Projeto

O projeto foi construído para demonstrar na prática:
1. **POO Avançada**: Encapsulamento com atributos privados/protegidos, decorators `@property` e `@setter`, validações de regras de negócio nas entidades e métodos de classe (`@classmethod`).
2. **Segurança de Credenciais**: Criptografia de senhas com algoritmo de dispersão **SHA-256** (as senhas nunca são armazenadas em texto puro).
3. **Persistência Relacional**: Banco SQLite com chaves estrangeiras ativas (`PRAGMA foreign_keys = ON;`) e integridade referencial com deleção em cascata (`ON DELETE CASCADE`).
4. **Design de IHC (Interação Humano-Computador)**: Redução de menus profundos ao consolidar a visualização de etapas e comentários em uma árvore hierárquica única (`rich.tree.Tree`).

---

## ✨ Funcionalidades

### 👤 Autenticação de Usuários
- Cadastro de novos usuários com validação de nome exclusivo (sem números).
- Criptografia irreversível da senha com hash SHA-256.
- Login seguro comparando o hash computado com o registrado no banco.

### 📁 Gerenciamento de Projetos
- Listagem dos projetos pertencentes exclusivamente ao usuário logado.
- Contagem dinâmica de etapas pendentes calculada via consulta agregada (`LEFT JOIN` + `COUNT CASE WHEN`).
- Criação de novos projetos.
- Atualização flexível de nome e descrição.
- Exclusão de projeto com confirmação explícita (`[S/N]`) e remoção em cascata das etapas e comentários subordinados.

### 📦 Gerenciamento de Etapas (Tarefas)
- Criação de etapas vinculadas ao projeto.
- Controle de fluxo de trabalho por status: `pendente`, `fazendo` e `concluído`.
- Edição do texto da etapa.
- Exclusão de etapa com confirmação.

### 💬 Gerenciamento de Comentários
- Adição de notas/comentários associados a uma etapa específica.
- Registro automático da data e hora local do sistema (`datetime('now', 'localtime')`).
- Visualização formatada no padrão brasileiro (`DD/MM/AAAA HH:MM`).
- Exclusão individual de comentários.

---

## 🏛 Arquitetura do Sistema (MVC)

O projeto adota a separação de responsabilidades pelo padrão **MVC (Model-View-Controller)**:

```text
Avaliacao_POO_Banco/
│
├── database.py             # Conexão SQLite, ativação de FKs e criação de tabelas (DDL)
├── main.py                 # Ponto de entrada leve da aplicação
├── info.db                 # Banco de dados relacional SQLite local
│
├── models/                 # [M] MODEL: Entidades puras e regras de negócio
│   ├── usuario.py          # Classe Usuario (encapsulamento e validação de hash)
│   ├── projeto.py          # Classe Projeto
│   ├── etapa.py            # Classe Etapa (validação de status permitidos)
│   └── comentario.py       # Classe Comentario
│
├── controllers/            # [C] CONTROLLER: Camada de persistência (DAO / CRUD)
│   ├── usuario.py          # UsuarioController (consultas e inserções parametrizadas)
│   ├── projeto.py          # ProjetoController
│   ├── etapa.py            # EtapaController
│   └── comentario.py       # ComentarioController
│
├── telas/                  # [V] VIEW: Menus, interface CLI e estilização visual
│   ├── auth.py             # Telas de cadastro e login
│   ├── projeto.py          # Painel principal de projetos com tabela Rich
│   └── detalhes.py         # Visualização integrada de etapas e comentários em árvore
│
└── uteis/                  # Módulos utilitários compartilhados
    ├── interface.py        # Limpeza de tela, cabeçalhos Rich e confirmação de ações
```

---

## 🛠 Tecnologias e Dependências

### Linguagem
- **Python 3.10+**

### Bibliotecas Nativas (Não requerem instalação externa)
- `sqlite3`: Banco de dados relacional embutido.
- `hashlib`: Geração de resumos criptográficos em SHA-256.
- `os` e `time`: Operações do sistema operacional e pausas de transição de tela.
- `datetime`: Manipulação e formatação de datas.

### Bibliotecas Externas
- **[Rich](https://github.com/Textualize/rich)**: Biblioteca para renderização de cores, tabelas (`Table`), árvores hierárquicas (`Tree`) e painéis (`Panel`) no terminal.

---

## 📥 Como Instalar e Executar

### 1. Clonar o repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd Avaliacao_POO_Banco
```

### 2. (Opcional) Criar e ativar um ambiente virtual
* **No Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* **No Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar as dependências externas
```bash
pip install rich
```

### 4. Executar a aplicação
```bash
python main.py
```

---

## 🧭 Instruções de Uso

1. **Tela Inicial (Autenticação)**:
   - Digite `1` para se cadastrar (informe um nome sem números e sua senha).
   - Digite `2` para fazer login com o nome e senha cadastrados.
   - Digite `0` para encerrar o programa.

2. **Painel de Projetos (Pós-login)**:
   - Seus projetos serão exibidos em uma tabela com o respectivo ID, nome, descrição e quantidade de etapas pendentes.
   - Digite `1` para abrir os detalhes de um projeto específico.
   - Digite `2` para criar um novo projeto.
   - Digite `3` para editar o nome ou descrição de um projeto existente.
   - Digite `4` para excluir um projeto.
   - Digite `0` para deslogar.

3. **Tela de Detalhes do Projeto**:
   - Visualize a árvore hierárquica do projeto com as etapas (`⏳ PENDENTE`, `⚙ FAZENDO`, `✔ CONCLUÍDO`) e os comentários (`💬`) correspondentes.
   - Use as opções `1` a `4` para gerenciar as etapas.
   - Use as opções `5` e `6` para adicionar ou remover comentários.
   - Digite `0` para retornar à listagem de projetos.

---

## 🗄 Modelagem do Banco de Dados

O banco de dados relacional segue a seguinte hierarquia com integridade referencial:

```text
[ Usuarios ]
     │ (1:N)
     ▼
[ Projetos ]
     │ (1:N)
     ▼
 [ Etapas ]
     │ (1:N)
     ▼
[ Comentarios ]
```

* Todas as chaves estrangeiras possuem `ON DELETE CASCADE` e `ON UPDATE CASCADE`. Excluir um projeto removerá automaticamente todas as suas etapas e comentários vinculados, garantindo consistência relacional.
