import argparse
import re
import sys

from rich import box
from rich.box import Box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from voxx.connection import console, close
from voxx.connection import establish_voxx_connection
from voxx.tui import start_tui
from voxx import __voxx_version__, __app_name__, __description__

UNAME_RE = r'^[A-Za-z][A-Za-z0-9_]{3,6}$'
ADDR_RE = r'(.*):(\d+)'

EMPTY: Box = Box(
    """\
    
    
    
    
    
    
    
    
"""
)


class VoxxParser(argparse.ArgumentParser):
    def _print_message(self, message, file=None):
        console.print(message)

    def format_help(self):
        out: str
        table = Table(box=EMPTY,
                      show_header=False,
                      show_lines=False,
                      pad_edge=False)

        table.add_column(min_width=1)
        table.add_column(min_width=25)
        table.add_column(min_width=10)

        for action in self._actions:
            metavar = action.metavar if action.metavar else ''
            table.add_row(f'[aquamarine1]{action.option_strings[0]}[/aquamarine1]',
                          f'[cyan3]{action.option_strings[1]}[/cyan3] [gold3]{metavar}[/gold3]',
                          f'[bright_black]{action.help}[/bright_black]')

        group = Group(
            Text.assemble('Voxx CLI ', (f'v{__voxx_version__}', 'bold magenta'), justify='center', end='\n\n'),
            Text.assemble((f'{__description__}', 'bright_black'), justify='center', end='\n\n'),
            Text.assemble(f' Usage: {__app_name__} [options] ', (f'<arg>', 'bold gold3'), justify='left', end='\n\n'),
            Panel.fit(table, title='options', title_align='left', border_style='bright_black')
        )
        return Panel.fit(group, box=EMPTY)


parser = VoxxParser(prog='voxx-cli', description=__description__)
parser.add_argument('-a', '--address', metavar='ADDRESS', type=str, help='voxx server address',
                    default='localhost:8008')
parser.add_argument('-u', '--user', metavar='USERNAME', type=str, help='username to register as', required=True)
parser.add_argument('-v', '--version', action='version',
                    version=f'[bold magenta]{__app_name__}[/bold magenta] version {__voxx_version__}')


def main():
    args = parser.parse_args()
    addr = args.a if hasattr(args, 'a') else args.address
    user = args.u if hasattr(args, 'u') else args.user
    if not re.match(ADDR_RE, addr):
        console.print(f'[warning]Invalid address: [bold red]{args.addr}[/bold red][/warning]')
        console.print(f'[italic]Address must be in the form of [bold green]host:port[/bold green][/italic]')
        sys.exit(1)
    if not re.match(UNAME_RE, user):
        console.print(f'[warning]Invalid username: [bold red]{args.user}[/bold red][/warning]')
        console.print(f'[italic]Username must be 4-7 characters long and start with a letter[/italic]')
        sys.exit(1)
    with console.status("[bold green]Connecting to server...") as status:
        addr = tuple(addr.split(':'))
        establish_voxx_connection(args.user, (addr[0], int(addr[1])))
    start_tui()
    close()


if __name__ == '__main__':
    main()
