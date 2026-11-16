# VIEW / TELA DE DETALHES DO PROJETO (Etapas e Comentários integrados)
from uteis.interface import limpar_tela, exibir_header, confirmar_acao, console
from rich.tree import Tree
from models.etapa import Etapa
from models.comentario import Comentario
from controllers.projeto import ProjetoController
from controllers.etapa import EtapaController
from controllers.comentario import ComentarioController

def menu_detalhes(id_projeto: int, usuario_logado):
  """
  Exibe o projeto selecionado com suas etapas e comentários aninhados em árvore (Tree).
  Centraliza o gerenciamento completo de etapas e comentários.
  """
  while True:
    limpar_tela()

    # Validação de segurança: o projeto deve pertencer ao usuário logado
    projeto = ProjetoController.buscar_por_id(id_projeto, usuario_logado.id_usuario)
    if not projeto:
      console.print('[bold red]Projeto não encontrado![/bold red]')
      console.input('\nPressione Enter para voltar...')
      break

    # Desestruturação de tupla
    id_proj, nome_proj, desc_proj, _ = projeto
    exibir_header(f"PROJETO: {nome_proj.upper()}", f"Descrição: {desc_proj}")

    # Carrega as etapas do projeto
    etapas = EtapaController.listar_por_projeto(id_projeto)

    # Construção visual da hierarquia com a árvore do Rich
    arvore = Tree(f"[bold cyan]📁 {nome_proj}[/bold cyan] [dim](ID: {id_proj})[/dim]")

    if etapas:
      for etapa in etapas:
        # Desestruturação de tupla
        id_etapa, texto, status, _ = etapa
        
        # Definição do badge visual baseado no status da etapa
        if status == 'concluído':
          badge = "[bold green]✔ [CONCLUÍDO][/bold green]"
        elif status == 'fazendo':
          badge = "[bold yellow]⚙ [FAZENDO][/bold yellow]"
        else:
          badge = "[bold red]⏳ [PENDENTE][/bold red]"

        ramo_etapa = arvore.add(f"[bold cyan]Etapa #{id_etapa}[/bold cyan] {badge} - {texto}")

        # Busca e aninha os comentários correspondentes logo abaixo da etapa
        comentarios = ComentarioController.listar_por_etapa(id_etapa)
        if comentarios:
          for c in comentarios:
            # Desestruturação de tupla
            id_com, texto_com, data_com, _ = c
            # Formata a data para o padrão brasileiro (DD/MM/AAAA HH:MM)
            try:
              from datetime import datetime
              data_formatada = datetime.strptime(data_com, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
            except Exception:
              data_formatada = data_com

            ramo_etapa.add(f"[magenta]💬 #{id_com}[/magenta] [dim]({data_formatada})[/dim]: {texto_com}")
        else:
          ramo_etapa.add("[dim italic](Sem comentários)[/dim italic]")
    else:
      arvore.add("[yellow italic]Nenhuma etapa cadastrada neste projeto ainda.[/yellow italic]")

    console.print(arvore)
    console.print("\n[bold]AÇÕES DISPONÍVEIS:[/bold]")
    console.print("[dim]Etapas:     [/dim] [1] Nova Etapa  | [2] Alterar Status  | [3] Editar Texto  | [4] Excluir Etapa")
    console.print("[dim]Comentários:[/dim] [5] Adicionar Comentário  | [6] Excluir Comentário")
    console.print("[dim]Navegação:  [/dim] [0] Voltar aos Projetos")

    opcao = console.input("\n[bold]Escolha uma opção: [/bold]").strip()

    # IDs de etapas deste projeto para validação de entrada
    ids_etapas = EtapaController.listar_ids_do_projeto(id_projeto)

    match opcao:
      case '1':
        # Cadastro de nova etapa
        limpar_tela()
        exibir_header("NOVA ETAPA", f"Projeto: {nome_proj}")
        texto = console.input("Texto/Descrição da etapa: ").strip()

        if not texto:
          console.print("\n[bold red]O texto da etapa não pode ser vazio.[/bold red]")
          console.input("\nPressione Enter para continuar...")
          continue

        nova_etapa = Etapa(texto=texto, id_projeto_fk=id_projeto, status='pendente')
        id_gerado = EtapaController.cadastrar(nova_etapa)

        console.print(f"\n[bold green]Etapa cadastrada com sucesso! [ID: {id_gerado}][/bold green]")
        console.input("\nPressione Enter para continuar...")

      case '2':
        # Atualização de status da etapa
        if not ids_etapas:
          console.print("\n[bold yellow]Não há etapas cadastradas neste projeto.[/bold yellow]")
          console.input("\nPressione Enter para continuar...")
          continue

        try:
          id_etapa = int(console.input("Informe o ID da etapa: ").strip())
          if id_etapa not in ids_etapas:
            console.print("\n[bold red]ID da etapa inválido para este projeto.[/bold red]")
            console.input("\nPressione Enter para continuar...")
            continue

          console.print("\nSelecione o novo status:")
          console.print("[1] Pendente\n[2] Fazendo\n[3] Concluído")
          op_status = console.input("Opção: ").strip()

          mapa_status = {'1': 'pendente', '2': 'fazendo', '3': 'concluído'}
          novo_status = mapa_status.get(op_status)

          if novo_status:
            EtapaController.atualizar_status(id_etapa, novo_status)
            console.print(f"\n[bold green]Status da etapa #{id_etapa} alterado para '{novo_status}'![/bold green]")
          else:
            console.print("\n[bold red]Opção de status inválida.[/bold red]")
          console.input("\nPressione Enter para continuar...")

        except ValueError:
          console.print("\n[bold red]Por favor, digite um número de ID válido.[/bold red]")
          console.input("\nPressione Enter para continuar...")

      case '3':
        # Atualização do texto da etapa
        if not ids_etapas:
          console.print("\n[bold yellow]Não há etapas cadastradas neste projeto.[/bold yellow]")
          console.input("\nPressione Enter para continuar...")
          continue

        try:
          id_etapa = int(console.input("Informe o ID da etapa a editar: ").strip())
          if id_etapa not in ids_etapas:
            console.print("\n[bold red]ID da etapa inválido para este projeto.[/bold red]")
            console.input("\nPressione Enter para continuar...")
            continue

          novo_texto = console.input("Novo texto da etapa: ").strip()
          if novo_texto:
            EtapaController.atualizar_texto(id_etapa, novo_texto)
            console.print("\n[bold green]Texto da etapa atualizado com sucesso![/bold green]")
          else:
            console.print("\n[yellow]Texto não alterado (vazio).[/yellow]")
          console.input("\nPressione Enter para continuar...")

        except ValueError:
          console.print("\n[bold red]Por favor, digite um número de ID válido.[/bold red]")
          console.input("\nPressione Enter para continuar...")

      case '4':
        # Exclusão de etapa
        if not ids_etapas:
          console.print("\n[bold yellow]Não há etapas cadastradas neste projeto.[/bold yellow]")
          console.input("\nPressione Enter para continuar...")
          continue

        try:
          id_etapa = int(console.input("Informe o ID da etapa a excluir: ").strip())
          if id_etapa not in ids_etapas:
            console.print("\n[bold red]ID da etapa inválido para este projeto.[/bold red]")
            console.input("\nPressione Enter para continuar...")
            continue

          if confirmar_acao(f"Excluir etapa #{id_etapa} e todos os seus comentários?"):
            EtapaController.excluir(id_etapa)
            console.print("\n[bold green]Etapa excluída com sucesso![/bold green]")
          else:
            console.print("\n[yellow]Exclusão cancelada.[/yellow]")
          console.input("\nPressione Enter para continuar...")

        except ValueError:
          console.print("\n[bold red]Por favor, digite um número de ID válido.[/bold red]")
          console.input("\nPressione Enter para continuar...")

      case '5':
        # Cadastro de comentário na etapa
        if not ids_etapas:
          console.print("\n[bold yellow]Cadastre uma etapa antes de adicionar comentários.[/bold yellow]")
          console.input("\nPressione Enter para continuar...")
          continue

        try:
          id_etapa = int(console.input("Informe o ID da etapa que receberá o comentário: ").strip())
          if id_etapa not in ids_etapas:
            console.print("\n[bold red]ID da etapa inválido para este projeto.[/bold red]")
            console.input("\nPressione Enter para continuar...")
            continue

          comentario_texto = console.input("Digite o comentário: ").strip()
          if not comentario_texto:
            console.print("\n[bold red]O comentário não pode ser vazio.[/bold red]")
            console.input("\nPressione Enter para continuar...")
            continue

          novo_comentario = Comentario(comentario=comentario_texto, id_etapa_fk=id_etapa)
          id_com = ComentarioController.cadastrar(novo_comentario)

          console.print(f"\n[bold green]Comentário adicionado com sucesso! [ID: {id_com}][/bold green]")
          console.input("\nPressione Enter para continuar...")

        except ValueError:
          console.print("\n[bold red]Por favor, digite um número de ID válido.[/bold red]")
          console.input("\nPressione Enter para continuar...")

      case '6':
        # Exclusão de comentário
        ids_comentarios = ComentarioController.listar_ids_do_projeto(id_projeto)
        if not ids_comentarios:
          console.print("\n[bold yellow]Não há comentários cadastrados neste projeto.[/bold yellow]")
          console.input("\nPressione Enter para continuar...")
          continue

        try:
          id_com = int(console.input("Informe o ID do comentário a excluir: ").strip())
          if id_com not in ids_comentarios:
            console.print("\n[bold red]ID de comentário inválido para este projeto.[/bold red]")
            console.input("\nPressione Enter para continuar...")
            continue

          if confirmar_acao(f"Excluir comentário #{id_com}?"):
            ComentarioController.excluir(id_com)
            console.print("\n[bold green]Comentário excluído com sucesso![/bold green]")
          else:
            console.print("\n[yellow]Exclusão cancelada.[/yellow]")
          console.input("\nPressione Enter para continuar...")

        except ValueError:
          console.print("\n[bold red]Por favor, digite um número de ID válido.[/bold red]")
          console.input("\nPressione Enter para continuar...")

      case '0':
        # Retorna ao painel de projetos
        break

      case _:
        console.print("\n[bold red]Opção inválida. Tente novamente![/bold red]")
        console.input("\nPressione Enter para continuar...")
