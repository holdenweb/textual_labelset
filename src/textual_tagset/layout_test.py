from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Rule
from textual.containers import Vertical, Horizontal, VerticalScroll
from rich.text import Text

from typing import Callable

DEFAULT_SELECTED_FORMAT = "\\[{v} [@click='klick({i})']x[/]]"
DEFAULT_UNSELECTED_FORMAT = "\\[[@click='klick({i})']{v}[/]]"

def sort_key(x):
    k, v = x
    f, l = v.split(None, 1)
    return l, f

class ActionStatic(Static):

    count = 0

    def __init__(self, label, *args, **kw):
        ActionStatic.count += 1
        self.count = ActionStatic.count
        super().__init__(f"ActionStatic {self.count} {label}")

    def update(self, label):
        super().update(f"ActionStatic {self.count} (updated) {label}")

class TagSetStatic(Widget):
    """A set of labels that render as a static.

    Args:
        members: A dictionary of tags, keyed by unique integers
        action_func: The action to be taken when a member's link is clicked.
        fmt: The format of a member in the TagSet's string representation.
        key: The key function used to sort the members.
    """
    DEFAULT_CSS = 'TagSetStatic{ background: blue 100%; height: auto; } Vertical { height: auto; border: yellow 100%; }'

    def compose(self):
        with Vertical(id='tag-set-static'):
            yield ActionStatic("This is an ActionStatic inside a container (I have my reasons)")

    def on_mount(self):
        self.query_one(ActionStatic).update("This is an ActionStatic inside a container. It has now been mounted.")


class TagSet(Widget):
    """
    Turns a dict of tags into a renderable widget.
    """
    DEFAULT_CSS = "TagSet { margin: 0 2 0 2; height: auto; border: white 100%; width: 50%; } Vertical { height: auto; border: white 100%; }"
    def __init__ (self, *args, **kw):
        super().__init__(*args, **kw)
        self.container = Vertical(id="tag-set")

    def compose(self):
        with self.container:
            yield TagSetStatic()

    def update(self):
        self.container.remove_children()
        self.container.mount(TagSetStatic())

class TagSetSelector(Widget):
    DEFAULT_CSS = """
    #filler { border: yellow 100%; height: 1fr; }
    #lss-selector { height: auto; }
    """

    def compose(self) -> ComposeResult:
        with Horizontal(id="lss-selector"):
            yield TagSet(id="tag-set-left", classes="tagset")
            yield TagSet(id = "tag-set-right", classes="tagset")
        yield Horizontal(id="filler")

def build_app() -> App:

    class SelTestApp(App):

        def compose(self):
            yield TagSetSelector(id="tag-set-selector")

        def on_click(self, e):
            self.panic(self.tree, self.css_tree)

    return SelTestApp()

app = build_app()

if __name__ == '__main__':
    app.run()
