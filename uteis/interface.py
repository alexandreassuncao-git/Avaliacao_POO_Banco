# MÓDULO DE UTILITÁRIOS DE INTERFACE (Terminal / Rich)
import os
from time import sleep
from rich.console import Console
from rich.panel import Panel

# Instância compartilhada do console Rich para formatação de texto e cores
console = Console()

def limpar_tela():
  """Aplica uma breve pausa de transição e limpa o console (Windows/Linux/Mac)."""
  sleep(0.3)
  os.system('cls' if os.name == 'nt' else 'clear')

def exibir_header(titulo: str, subtitulo: str = ""):
  """Renderiza um cabeçalho padronizado em caixa (Panel) no topo da tela."""
  conteudo = f"[bold cyan]{titulo}[/bold cyan]"
  if subtitulo:
    conteudo += f"\n[dim]{subtitulo}[/dim]"
  console.print(Panel(conteudo, expand=False))

def confirmar_acao(mensagem: str) -> bool:
  """
  Solicita confirmação binária (sim/não) ao usuário antes de operações destrutivas.
  Nota: A barra invertida antes de '[' (escape) é necessária para o Rich não interpretar [S/N] como tag de estilo.
  """
  resposta = console.input(f"\n[yellow]{mensagem} \\[S/N]: [/yellow]").strip().lower()
  return resposta == 's'
