import sys
from typing import Optional

from textual.widget import Widget
from textual.app import Screen
from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.message import Message
from textual.events import Key
from textual.widgets import Button, Static
from textual_tagset.demo.data import random_names


class BaseScreen(ModalScreen):

    CSS_PATH = "basescreen.tcss"

    def __init__(
        self,
        n,
        item_fmt: Optional[str] = "\\[!]",
        link_fmt: Optional[str] = "{v}",
        sep: Optional[str] = "\n",
    ):
        self.n = n
        self._item_fmt = item_fmt
        self._link_fmt = link_fmt
        self._sep = sep
        self.items = list(random_names(self.n))
        super().__init__("MyBaseScreen")
        self.main_widget = self.demo_widget()
        self._modal = True

    def compose(self):
        with Vertical(id="tagset-dialog"):
            self.message_box = Static(":eyes: WATCH THIS SPACE :eyes:", id="message-box")
            with Horizontal(id="widget-container"):
                with VerticalScroll():
                    yield self.main_widget
            yield self.message_box

    def on_mount(self):
        self.focus()

    def on_key(self, k: Key):
        if k.key == 'enter':
            self.dismiss(result=self.main_widget.result())

    def demo_widget(self):
        raise NotImplementedError("BaseScreen subclasses must declare a 'demo_widget' method.")