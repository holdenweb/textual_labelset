"""
demo_tagset_selector.py: demonstrate the basic features of textual_tagset.
"""
from textual.app import App
from textual_tagset import TagSetSelector
from textual.containers import Horizontal
from textual.widgets import Button, Static
from textual_tagset.demo.data import selected, deselected

from .baseapp import BaseApp

def build_app(s: list[str], u: list[str]) -> App:

    class SelTestApp(BaseApp):
        def compose(self):
            with Horizontal():
                yield TagSetSelector(s, u, sep=" ", select_hook=self.log_select, deselect_hook=self.log_deselect)
                yield Button("Click to Quit")
            yield Static(":eyes: WATCH THIS SPACE :eyes:", id="message-box")
        def log_select(self, i, v):
            self.set_message(f"{v} selected")
        def log_deselect(self, i, v):
            self.set_message(f"{v} deselected")

    return SelTestApp

SelTestApp = build_app(selected, deselected)
app = SelTestApp()

if __name__ == '__main__':
    app.run()
