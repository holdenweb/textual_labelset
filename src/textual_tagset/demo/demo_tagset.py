"""
demo_tagset.py: show off the features of textual_tagset.
"""
import codecs

from textual import on
from textual.app import App
from textual.containers import Vertical
from textual.validation import Integer
from textual.widgets import Input, Static
from textual_tagset import TagSet
from textual_tagset.demo.data import random_names

from .baseapp import BaseScreen

class TagSetScreen(BaseScreen):

    CSS = "TagSetScreen { background: rgba(0, 0, 0, 0.5); }"

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
        self.items =list( random_names(self.n))
        super().__init__(self.items)

    def demo_widget(self):
        return TagSet(self.items, action_func=None, link_fmt=self.link_fmt, item_fmt=self.item_fmt, sep=self.sep)

class SelTestApp(App):

    CSS = """
    Screen {
        layout: horizontal;
    }
    """
    CSS_PATH = "../tagset.tcss"
    def compose(self):
        self.name_count = Input(placeholder="How many names",
                    validators=[Integer(1, 4900)],
                    id="name-count")
        self.link_text = Input(value="{v}", placeholder="Enter link text format")
        self.item_format = Input(value="[!]", placeholder="Enter entry text format (! becomes link")
        self.separator = Input("\\n", placeholder="Enter separator")
        members = ["TagSet", "TagSetSelector", "FilteredTagSet", "FilteredTagSetSelector"]
        with Vertical():
            yield Static(
            "The link text becomes the selection hyperlink for an entry. "
            "The item format must contain a \"!\" to indicate where the "
            "link should appear. The separator is inserted between items."
            "For text entry the usual Python escape sequences are available."
            "\n\nHow many names:""")
            yield self.name_count
            yield Static("Link text:")
            yield self.link_text
            yield Static("Item format (link replaces !)")
            yield self.item_format
            yield Static("Item separator")
            yield self.separator
        self.type_selector = TagSet(members, action_func=None, item_fmt="{v}", link_fmt="[!]", key=None, sep="\n", id="type-choice")
        with Vertical(id="display"):
            yield Static("Select object type here")
            yield self.type_selector

    @on(Input.Submitted)
    def input_submitted(self, event):
        n = int(self.name_count.value)
        link_fmt = self.escape_managed(self.link_text.value)
        item_fmt = self.escape_managed(self.item_format.value)
        sep = self.escape_managed(self.separator.value)
        self.app.push_screen(TagSetScreen(n, link_fmt=link_fmt, item_fmt=item_fmt, sep=sep), self.finished_screen)

    def escape_managed(self, s):
        return codecs.escape_decode(bytes(s, "utf-8"))[0].decode("utf-8")

    def finished_screen(self, message):
        self.reset_inputs()

    def reset_inputs(self):
        self.name_count.focus()

app = SelTestApp()

if __name__ == '__main__':
    app.run()
