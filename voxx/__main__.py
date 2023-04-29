import argparse
import re
import sys

from voxx.connection import console, close
from voxx.connection import establish_voxx_connection
from voxx.tui import start_tui

UNAME_RE = r'^[A-Za-z][A-Za-z0-9_]{3,6}$'
ADDR_RE = r'(.*):(\d+)'


class VoxxParser(argparse.ArgumentParser):
    def _print_message(self, message, file=None):
        console.print(message)


parser = VoxxParser(prog='voxx-cli', description='Voxx command line interface client')
parser.add_argument('-addr', type=str, help='Voxx server address', default='localhost:8008')
parser.add_argument('-user', type=str, help='Username to register as', required=True)


def main():
    args = parser.parse_args()
    if not re.match(ADDR_RE, args.addr):
        console.print(f'[warning]Invalid address: [bold red]{args.addr}[/bold red][/warning]')
        console.print(f'[italic]Address must be in the form of [bold green]host:port[/bold green][/italic]')
        sys.exit(1)
    if not re.match(UNAME_RE, args.user):
        console.print(f'[warning]Invalid username: [bold red]{args.user}[/bold red][/warning]')
        console.print(f'[italic]Username must be 4-7 characters long and start with a letter[/italic]')
        sys.exit(1)
    with console.status("[bold green]Connecting to server...") as status:
        addr = tuple(args.addr.split(':'))
        establish_voxx_connection(args.user, (addr[0], int(addr[1])))
    start_tui()
    close()


if __name__ == '__main__':
    main()
