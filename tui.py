import asyncio
from datetime import datetime
from types import SimpleNamespace

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Container
from textual.widgets import Input, Static

from connection import um_handler


class MessageBar(Container):
    def __init__(self, sender: str, message: str, time: str = None):
        super().__init__()
        self.mount(Static(message, classes='message'))
        self.border_title = sender
        self.border_subtitle = time


class NotificationBar(Static):
    pass


class Voxx(App):
    CSS_PATH = "tui.css"

    def __int__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        vert = VerticalScroll(id="results-container")
        vert.border_title = "Voxx-cli"
        yield vert
        yield Input(id="msg-input", placeholder="Enter Message")

    def _on_compose(self) -> None:
        """A coroutine to handle a text changed message."""
        asyncio.create_task(self.after_mount())

    async def after_mount(self):
        msg = "Welcome to Voxx-CLI! This chat is not moderated, please be nice and civil."
        time = datetime.now().strftime("%m/%d/%y %I:%M %p")
        await self.add_message(msg, time, 'System')

    @um_handler
    def nu(self, msg: SimpleNamespace) -> None:
        """Handles new user update message"""
        pass

    @um_handler
    def nm(self, msg: SimpleNamespace) -> None:
        """Handles new message update message"""
        pass

    @um_handler
    def ud(self, msg: SimpleNamespace) -> None:
        """Handles user disconnect update message"""
        pass

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        """A coroutine to handle a text changed message."""
        if not message.value:
            return

        if message.value == '/exit':
            self.exit()
            return

        if message.value == '/ul':
            asyncio.create_task(self.get_users())
            return

        if message.value:
            asyncio.create_task(self.add_message(message.value))

    async def get_users(self):
        pass

    async def add_message(self, message: str, time: str = datetime.now().strftime("%m/%d/%y %I:%M %p"),
                          sender: str = 'System') -> None:
        """Add message to the result container."""
        bar = MessageBar(sender, message, time)
        await self.query_one("#results-container").mount(bar)
        self.call_after_refresh(self.query_one("#results-container").scroll_end, animate=False)


if __name__ == "__main__":
    try:
        app = Voxx()
    except Exception as e:
        print(e)
        print("Could not connect to server")
        exit(1)
    app.run()
