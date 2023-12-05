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

from .baseapp import BaseScreen

class TagSetScreen(BaseScreen):

    def demo_widget(self):
        self.widget = TagSet(self.items, link_fmt=self.link_fmt, item_fmt=self.item_fmt, sep=self.sep, id="demo-widget")
        return self.widget

    #@on(TagSet.Selected, "#demo-widget")
    #def tagset_selected(self, event):
        #self.log(event.control)
        #self.set_message(event.selected)


class SelTestApp(App):

    CSS = """
    Screen {
        layout: horizontal;
    }
    Vertical {
        border: solid white 75%;
        margin: 2 2 2 2;
    }
    """
    CSS_PATH = "../tagset.tcss"
    def compose(self):
        self.name_count = Input(value="20", placeholder="How many names",
                    validators=[Integer(1, 4900)],
                    id="name-count")
        self.link_text = Input(value="{v}", placeholder="Enter link text format")
        self.item_format = Input(value="[!]", placeholder="Enter entry text format (! becomes link")
        self.separator = Input("\\n", placeholder="Enter separator")
        with Vertical():
            yield Static(
            "The link text becomes the selection hyperlink for an entry. "
            "The item format must contain a \"!\" to indicate where the "
            "link should appear. The separator is inserted between items."
            "The usual Python escape sequences are available."
            "\n\nHow many names:""")
            yield self.name_count
            yield Static("Link text:")
            yield self.link_text
            yield Static("Item format (link replaces !)")
            yield self.item_format
            yield Static("Item separator")
            yield self.separator
        members = ["TagSet", "TagSetSelector", "FilteredTagSet", "FilteredTagSetSelector"]
        self.type_selector = TagSet(members, sep="\n", id="type-choice")
        with Vertical(id="display"):
            yield Static("Select object type here")
            yield self.type_selector
        self.message_box = Static(":eyes: WATCH THIS SPACE :eyes:", id="message-box")
        yield self.message_box

    @on(TagSet.Selected, "#demo-widget")
    def demo_tagset_selected(self, event):
        self.set_message(f"{event.selected} selected")

    @on(TagSet.Selected, "#type-choice")
    def tagset_type_selected(self, event):
        n = int(self.name_count.value)
        link_fmt = self.esc_processed(self.link_text.value)
        item_fmt = self.esc_processed(self.item_format.value)
        sep = self.esc_processed(self.separator.value)
        self.app.push_screen(TagSetScreen(n, link_fmt=link_fmt, item_fmt=item_fmt, sep=sep), self.finished_screen)

    def esc_processed(self, s):
        return codecs.escape_decode(bytes(s, "utf-8"))[0].decode("utf-8")

    def finished_screen(self, message):
        self.name_count.focus()

    def set_message(self, m):
        self.message_box.update(m)
    def log_item(self, i):
        self.set_message(self.items[i])
    def log_select(self, i, v):
        self.set_message(f"{v} selected")
    def log_deselect(self, i, v):
        self.set_message(f"{v} deselected")
    def demo_widget(self):
        raise NotImplementedError
    def on_click(self, event):
        self.log(self.tree)
        self.log(self.css_tree)

app = SelTestApp()

if __name__ == '__main__':
    app.run()
