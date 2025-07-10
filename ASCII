from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

def show_banner():
    banner = """
██████╗  ╔█████╗     ╔███╗
██╔══██╗ █    ██╗   ╔█   █╗
██████╔╝ █     ██╗ ╔█     █╗
██╔═══╝  █    ██╔╝ █       █
██║      █   ██╔╝  ╚█     █╝
██║      █████═╝    ╚█   █╝
╚═╝      ╚═══╝       ╚███╝
"""
    subtitle = Text("Porn.Down.Operation", style="bold cyan")

    panel = Panel.fit(
        Text(banner, style="bold blue"),
        title="R.R",
        subtitle_align="center",
        subtitle=subtitle,
        padding=(1, 4),
        border_style="blue",
        box=box.ROUNDED
    )
    console.clear()
    console.print(panel)
