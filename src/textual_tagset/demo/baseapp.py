import sys

from textual.app import Screen
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Button, Static

from textual_tagset.demo.data import random_names

class BaseScreen(Screen):
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
        self.items =list(random_names(self.n))
        super().__init__("MyBaseScreen")

    CSS_PATH = "../tagset.tcss"

    def compose(self):
        with Horizontal():
            yield self.demo_widget()
            yield Button("Click to Dismiss")
    def on_button_pressed(self, e):
        self.dismiss("Message!")
