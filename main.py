# PONTO DE ENTRADA DA APLICAÇÃO (Main)
from database import criar_tabelas
from telas.auth import menu_autenticacao
from telas.projeto import menu_projetos

def main():
  # Garante que as tabelas SQLite estejam criadas antes de iniciar a interface
  criar_tabelas()

  while True:
    # 1. FLUXO DE ACESSO: Solicita autenticação (Cadastro ou Login)
    usuario = menu_autenticacao()

    # Se o usuário escolheu '0' (Sair), encerra o loop principal
    if not usuario:
      print('\nVolte sempre!')
      break

    # 2. SESSÃO ATIVA: Com o objeto Usuario instanciado, abre o painel dele
    menu_projetos(usuario)
  
if __name__ == '__main__':
  main()
