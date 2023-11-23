"""
demo_filtered_tagset.py: show selection from a large set.
"""
import sys

from textual.app import App
from textual_tagset import TagSetSelector, TagSet, TagSet, FilteredTagSet, FilteredTagSetSelector
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static
from textual_tagset.demo.data import selected, deselected

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
