import asyncio
from datetime import datetime
from types import SimpleNamespace

import pkg_resources
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll, Container
from textual.widgets import Input, Static, Footer

import voxx.model
from voxx import connection
from voxx.connection import um_handler, assert_rr, send_message, get_user_list
from voxx.model import UID, User


class MessageBar(Container):
    def __init__(self, sender: str, message: str, time: str = None):
        super().__init__()
        self.mount(Static(message, classes='message'))
        self.border_title = sender
        if time is not None:
            self.border_subtitle = time


class NotificationBar(Container):
    def __init__(self, message: str, title: str = None, subtitle: str = None):
        super().__init__()
        self.mount(Static(message, classes='message'))
        if title is not None:
            self.border_title = title
        if subtitle is not None:
            self.border_subtitle = subtitle


class Voxx(App):
    CSS_PATH = pkg_resources.resource_filename(__name__, "css/tui.css")
    BINDINGS = [
        Binding('ctrl+c', "quit", "Quit", show=True, priority=True),
        Binding('ctrl+l', 'ul', "List users", priority=True)
    ]

    def __int__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        vert = VerticalScroll(id="results-container")
        vert.border_title = "Voxx-cli"
        yield vert
        yield Input(id="msg-input", placeholder="Enter Message")
        yield Footer()

    def _on_compose(self) -> None:
        """A coroutine to handle a text changed message."""
        asyncio.create_task(self.after_mount())
        connection.um_conn.set_runner_instance(self)

    def clear_input(self) -> None:
        self.query_one('#msg-input').action_delete_left_all()

    async def after_mount(self):
        msg = "Welcome to Voxx-CLI! This chat is not moderated, please be nice and civil."
        time = datetime.now().astimezone().strftime(voxx.model.TIME_FORMAT)
        await self.add_message(msg, time, 'System')

    @um_handler
    def nu(self, msg: SimpleNamespace) -> None:
        """Handles new user update message: called from thread-2"""
        self.call_from_thread(self._add_notif, f'{msg.body.user.uname} has connected', 'User Connect', None)

    @um_handler
    def nm(self, msg: SimpleNamespace) -> None:
        """Handles new message update message: called from thread-2"""
        sender = User(UID.of(int(msg.body.sender.uid)), msg.body.sender.uname)
        time = UID.of(int(msg.body.message.uid)).get_timestamp_string()
        try:
            self.call_from_thread(self._add_msg, msg.body.message.content, sender.username, time)
        except Exception as e:
            send_message(f'Exception: {e}')

    @um_handler
    def ud(self, msg: SimpleNamespace) -> None:
        """Handles user disconnect update message: called from thread-2"""
        self.call_from_thread(self._add_notif, f'{msg.body.user.uname} has disconnected', 'User Disconnect', None)

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        """A coroutine to handle a text changed message."""
        if not message.value:
            return

        if not await self.handle_command(message):
            return

        if message.value:
            response = send_message(message.value)
            msg = response.body.message.content
            user = connection.assoc_user.username
            time = UID.of(int(response.body.message.uid))
            self.run_worker(self.add_message(msg, sender=user, time=time.get_timestamp_string()))
        self.clear_input()

    async def handle_command(self, command: Input.Submitted) -> bool:
        if command.value == '/exit':
            await self.action_quit()

        if command.value == '/ul':
            await self.get_users()
            self.clear_input()
            return True

        # If not a command we just don't send this message
        if command.value.startswith('/'):
            self.clear_input()
            return False
        return True

    async def action_ul(self):
        await self.get_users()

    async def action_quit(self) -> None:
        connection.close()
        await super().action_quit()

    async def get_users(self):
        response = get_user_list()
        names = [(f'{user.uname} (you)' if user.uname == connection.get_assoc_user().username else user.uname) for user
                 in response.body.users]
        ul = ', '.join(names)
        asyncio.create_task(self.add_notif(ul, title='Connected users'))

    async def add_notif(self, message: str, title=None, subtitle=None) -> None:
        bar = NotificationBar(message, title, subtitle)
        await self.query_one("#results-container").mount(bar)
        self.call_after_refresh(self.query_one("#results-container").scroll_end, animate=False)

    def _add_notif(self, *args) -> None:
        """Non-coroutine version of add_notif"""
        asyncio.create_task(self.add_notif(args[0], title=args[1], subtitle=args[2]))

    async def add_message(self, message: str, time: str = datetime.now().strftime(voxx.model.TIME_FORMAT),
                          sender: str = 'System') -> None:
        """Add message to the result container."""
        bar = MessageBar(sender, message, time)
        await self.query_one("#results-container").mount(bar)
        self.call_after_refresh(self.query_one("#results-container").scroll_end, animate=False)

    def _add_msg(self, *args) -> None:
        """Non-coroutine version of add_message"""
        asyncio.create_task(self.add_message(args[0], sender=args[1], time=args[2]))


@assert_rr
def start_tui():
    app = Voxx()
    app.run()
