import sys

from textual.app import Screen
from textual.containers import Horizontal, VerticalScroll
from textual.message import Message
from textual.widgets import Button, Static

from textual_tagset.demo.data import random_names

class BaseScreen(Screen):

    CSS = """
    #widget-container {
        height: 1fr;
    }
    #message-box {
        dock: bottom; text-align: center;
    }
    """

    def __init__(
        self,
        n,
        item_fmt: str | None = "\\[!]",
        link_fmt: str | None = "{v}",
        sep: str | None = "\n",
    ):
        self.n = n
        self.item_fmt = item_fmt
        self.link_fmt = link_fmt
        self.sep = sep
        self.items = list(random_names(self.n))
        super().__init__("MyBaseScreen")

    def compose(self):
        self.message_box = Static(":eyes: WATCH THIS SPACE :eyes:", id="message-box")
        with Horizontal(id="widget-container"):
            with VerticalScroll():
                yield self.demo_widget()
            yield Button("Click to Dismiss")
        yield self.message_box

    def on_button_pressed(self, e):
        self.dismiss("Message!")
