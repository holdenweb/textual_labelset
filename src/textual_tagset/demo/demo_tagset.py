"""
demo_tagset.py: show off the features of textual_tagset.
"""
from textual.app import App
from textual_tagset import TagSet
from textual.containers import Horizontal
from textual.widgets import Static, Button
from textual_tagset.demo.data import selected

from .baseapp import BaseApp

def build_app(s: list[str], u: list[str]) -> App:

    class SelTestApp(BaseApp):
        def compose(self):
            self.tags =  dict(enumerate(s))
            with Horizontal():
                yield TagSet(self.tags, action_func=self.nmbr_message, key=None, sep="\n")
                yield Button("Click to quit")
            yield Static(":eyes: WATCH THIS SPACE :eyes:", id="message-box")
        def nmbr_message(self, i):
            self.set_message(self.tags[i])

    return SelTestApp

SelTestApp = build_app(selected, [])
app = SelTestApp()

if __name__ == '__main__':
    app.run()
