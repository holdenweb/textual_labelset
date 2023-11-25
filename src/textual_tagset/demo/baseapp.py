import sys

from textual.app import App
from textual.containers import Horizontal
from textual.widgets import Button, Static

class BaseApp(App):
    CSS_PATH = "../tagset.tcss"
    def compose(self):
        with Horizontal():
            yield self.demo_widget()
            yield Button("Click to Quit")
        yield Static(":eyes: WATCH THIS SPACE :eyes:", id="message-box")
    def on_button_pressed(self, e):
        sys.exit()
    def on_click(self, event):
        self.log(self.tree)
        self.log(self.css_tree)
    def set_message(self, m):
        self.query_one("#message-box").update(m)
    def log_item(self, i):
        self.set_message(self.items[i])
    def log_select(self, i, v):
        self.set_message(f"{v} selected")
    def log_deselect(self, i, v):
        self.set_message(f"{v} deselected")
    def demo_widget(self):
        raise NotImplementedError
