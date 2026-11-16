# VIEW / TELA DE AUTENTICAÇÃO (Cadastro e Login)
from uteis.interface import limpar_tela, exibir_header, console
from models.usuario import Usuario
from controllers.usuario import UsuarioController

def menu_autenticacao():
  """
  Exibe o menu de acesso inicial.
  Retorna o objeto 'usuario_logado' em caso de sucesso no login, ou False para sair.
  """
  while True:
    limpar_tela()
    exibir_header("GERENCIADOR DE PROJETOS", "Acesso ao Sistema")
    console.print('[1] - Cadastrar\n[2] - Logar\n[0] - Sair')

    opcao = console.input("\n[bold]Escolha uma opção: [/bold]").strip()

    match opcao:
      case '1':
        # Fluxo de Cadastro de Usuário
        limpar_tela()
        exibir_header("CADASTRO DE USUÁRIO")
        nome = console.input('Informe seu nome: ').strip().lower()

        # Validação: nome não pode conter dígitos nem ser vazio
        if any(c.isdigit() for c in nome) or not nome:
          console.print('[bold red]Nome inválido (não deve conter números ou ser vazio).[/bold red]')
          console.input('\nPressione Enter para continuar...')
          continue

        # Validação: verifica se o nome já existe no banco
        nomes_cadastrados = UsuarioController.listar_nomes()
        if nome in nomes_cadastrados:
          console.print('[bold red]Nome já cadastrado no banco de dados. Tente outro![/bold red]')
          console.input('\nPressione Enter para continuar...')
          continue

        senha = console.input('Informe sua senha: ').strip()
        if not senha:
          console.print('[bold red]A senha não pode ser vazia.[/bold red]')
          console.input('\nPressione Enter para continuar...')
          continue

        # Criação da entidade e persistência via Controller
        novo_usuario = Usuario(nome, senha)
        novo_id = UsuarioController.cadastrar(novo_usuario)

        console.print(f'\n[bold green]Usuário cadastrado com sucesso! ID: {novo_id}[/bold green]')
        console.input('\nPressione Enter para continuar...')

      case '2':
        # Fluxo de Autenticação / Login
        limpar_tela()
        exibir_header("LOGIN")
        nome = console.input('Informe seu nome: ').strip().lower()
        senha = console.input('Informe sua senha: ').strip()

        # Busca o registro no banco pelo nome
        usuario_encontrado = UsuarioController.buscar_por_nome(nome)

        if not usuario_encontrado:
          console.print('\n[bold red]Usuário não encontrado. Tente novamente![/bold red]')
          console.input('\nPressione Enter para continuar...')
          continue

        # Valida a senha usando a regra de negócio da classe Usuario (hash SHA-256)
        if usuario_encontrado.validar_senha(senha):
          console.print(f'\n[bold green]Acesso liberado! Bem-vindo(a), {usuario_encontrado.nome.capitalize()}![/bold green]')
          console.input('\nPressione Enter para entrar...')
          return usuario_encontrado
        else:
          console.print('\n[bold red]Senha incorreta. Tente novamente![/bold red]')
          console.input('\nPressione Enter para continuar...')
          continue

      case '0':
        return False

      case _:
        console.print('\n[bold red]Opção inválida. Tente novamente![/bold red]')
        console.input('\nPressione Enter para continuar...')
