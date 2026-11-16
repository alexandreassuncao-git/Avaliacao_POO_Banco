# VIEW / TELA DE PROJETOS (Painel Principal do Usuário Logado)
from uteis.interface import limpar_tela, exibir_header, confirmar_acao, console
from rich.table import Table
from models.projeto import Projeto
from controllers.projeto import ProjetoController
from telas.detalhes import menu_detalhes

def menu_projetos(usuario_logado):
  """Exibe o painel de projetos pertencentes ao usuário logado."""
  while True:
    limpar_tela()
    exibir_header("PAINEL DE PROJETOS", f"Usuário logado: {usuario_logado.nome.capitalize()}")

    # Montagem da tabela formatada com a biblioteca Rich
    tabela = Table(title='MEUS PROJETOS')
    tabela.add_column('ID', justify='center', style='cyan')
    tabela.add_column('Nome', justify='left', style='bold')
    tabela.add_column('Descrição', justify='left')
    tabela.add_column('Etapas Pendentes', justify='center', style='yellow')

    # Busca projetos do usuário no banco
    projetos = ProjetoController.listar_por_usuario(usuario_logado.id_usuario)

    if projetos:
      for proj in projetos:
        # proj: (id_projeto, nome, descricao, total_pendentes)
        tabela.add_row(str(proj[0]), proj[1], proj[2], f'{proj[3]} pendente(s)')
      console.print(tabela)
    else:
      console.print('[yellow]Você ainda não possui projetos cadastrados.[/yellow]\n')

    console.print('\n[1] - Abrir Projeto\n[2] - Novo Projeto\n[3] - Editar Projeto\n[4] - Excluir Projeto\n[0] - Deslogar')

    opcao = console.input("\n[bold]Escolha uma opção: [/bold]").strip()

    # Obtém os IDs dos projetos do usuário para validações de segurança
    ids_do_usuario = ProjetoController.listar_ids_do_usuario(usuario_logado.id_usuario)

    match opcao:
      case '1':
        # Abrir detalhes do projeto (visualizar etapas e comentários)
        if not ids_do_usuario:
          console.print('\n[bold yellow]Você não possui projetos para abrir.[/bold yellow]')
          console.input('\nPressione Enter para continuar...')
          continue

        try:
          id_projeto = int(console.input('Informe o ID do projeto que deseja abrir: ').strip())
          if id_projeto in ids_do_usuario:
            menu_detalhes(id_projeto, usuario_logado)
          else:
            console.print('\n[bold red]ID não encontrado ou não pertence a você.[/bold red]')
            console.input('\nPressione Enter para continuar...')
        except ValueError:
          console.print('\n[bold red]Por favor, digite um número de ID válido.[/bold red]')
          console.input('\nPressione Enter para continuar...')

      case '2':
        # Cadastro de novo projeto
        limpar_tela()
        exibir_header("NOVO PROJETO")
        nome = console.input('Nome do projeto: ').strip()
        descricao = console.input('Descrição do projeto: ').strip()

        if not nome:
          console.print('\n[bold red]O nome do projeto não pode ser vazio.[/bold red]')
          console.input('\nPressione Enter para continuar...')
          continue

        novo_projeto = Projeto(nome, descricao, usuario_logado.id_usuario)
        novo_id = ProjetoController.cadastrar(novo_projeto)

        console.print(f'\n[bold green]Projeto criado com sucesso! [ID: {novo_id}][/bold green]')
        console.input('\nPressione Enter para continuar...')

      case '3':
        # Edição de nome ou descrição do projeto
        if not ids_do_usuario:
          console.print('\n[bold yellow]Você não possui projetos para editar.[/bold yellow]')
          console.input('\nPressione Enter para continuar...')
          continue

        try:
          id_projeto = int(console.input('Informe o ID do projeto que deseja editar: ').strip())
          if id_projeto not in ids_do_usuario:
            console.print('\n[bold red]ID não encontrado ou não pertence a você.[/bold red]')
            console.input('\nPressione Enter para continuar...')
            continue

          novo_nome = console.input('Novo nome (Enter para manter atual): ').strip()
          nova_descricao = console.input('Nova descrição (Enter para manter atual): ').strip()

          if novo_nome:
            ProjetoController.atualizar_nome(id_projeto, novo_nome)
          if nova_descricao:
            ProjetoController.atualizar_descricao(id_projeto, nova_descricao)

          if novo_nome or nova_descricao:
            console.print('\n[bold green]Projeto atualizado com sucesso![/bold green]')
          else:
            console.print('\n[yellow]Nenhuma alteração realizada.[/yellow]')
          console.input('\nPressione Enter para continuar...')

        except ValueError:
          console.print('\n[bold red]Por favor, digite um número de ID válido.[/bold red]')
          console.input('\nPressione Enter para continuar...')

      case '4':
        # Exclusão do projeto (com confirmação explícita de segurança)
        if not ids_do_usuario:
          console.print('\n[bold yellow]Você não possui projetos para excluir.[/bold yellow]')
          console.input('\nPressione Enter para continuar...')
          continue

        try:
          id_projeto = int(console.input('Informe o ID do projeto que deseja excluir: ').strip())
          if id_projeto not in ids_do_usuario:
            console.print('\n[bold red]ID não encontrado ou não pertence a você.[/bold red]')
            console.input('\nPressione Enter para continuar...')
            continue

          if confirmar_acao('Tem certeza que deseja excluir o projeto e tudo associado a ele?'):
            ProjetoController.excluir(id_projeto)
            console.print('\n[bold green]Projeto excluído com sucesso![/bold green]')
          else:
            console.print('\n[yellow]Exclusão cancelada.[/yellow]')
          console.input('\nPressione Enter para continuar...')

        except ValueError:
          console.print('\n[bold red]Por favor, digite um número de ID válido.[/bold red]')
          console.input('\nPressione Enter para continuar...')

      case '0':
        # Desloga e volta para o menu de autenticação
        limpar_tela()
        break

      case _:
        console.print('\n[bold red]Opção inválida. Tente novamente![/bold red]')
        console.input('\nPressione Enter para continuar...')
