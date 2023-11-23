"""
demo_tagset.py: show off the features of textual_tagset.
"""
import sys

from textual.app import App
from textual_tagset import TagSetSelector, TagSet, TagSet, FilteredTagSet, FilteredTagSetSelector
from textual.containers import Horizontal, Vertical, Center
from textual.widgets import Static, Button
from textual_tagset.demo.data import selected


def build_app(s: list[str], u: list[str]) -> App:

    class BaseApp(App):
        CSS_PATH = "../tagset.tcss"
        def on_button_pressed(self, e):
            sys.exit()
        def on_click(self, event):
            self.log(self.tree)
            self.log(self.css_tree)
        def set_message(self, m):
            self.query_one("#message-box").update(m)

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
