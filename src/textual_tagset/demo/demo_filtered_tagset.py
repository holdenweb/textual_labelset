"""
demo_filtered_tagset.py: show selection from a large set.
"""
from textual.app import App
from textual_tagset import FilteredTagSet
from textual.containers import Horizontal
from textual.widgets import Button, Static
from textual_tagset.demo.data import selected, deselected

from .baseapp import BaseApp

def build_app(s: list[str], u: list[str]) -> App:

    class SelTestApp(BaseApp):
        def compose(self):
            with Horizontal():
                self.items = dict(enumerate(s))
                yield FilteredTagSet(self.items, action_func=self.log_item, sep=" | ")
                yield Button("Click to Quit")
            yield Static(":eyes: WATCH THIS SPACE :eyes:", id="message-box")
        def log_item(self, i):
            self.set_message(self.items[i])
    return SelTestApp

SelTestApp = build_app(selected, deselected)
app = SelTestApp()

if __name__ == '__main__':
    app.run()
