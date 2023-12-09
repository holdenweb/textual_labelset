"""
demo_tagset.py: show off the features of textual_tagset.
"""
import codecs

from textual import on
from textual.app import App
from textual.containers import VerticalScroll, Horizontal
from textual.validation import Integer
from textual.widgets import Input, Static, Button
from textual_tagset import TagSet, FilteredTagSet, TagSetSelector, FilteredTagSetSelector

from .baseapp import BaseScreen

class TagSetScreen(BaseScreen):

    def demo_widget(self):
        return TagSet(self.items, link_fmt=self.link_fmt, item_fmt=self.item_fmt, sep=self.sep, id="demo-widget")

class FilteredTagSetScreen(BaseScreen):

    def demo_widget(self):
        return FilteredTagSet(self.items, link_fmt=self.link_fmt, item_fmt=self.item_fmt, sep=self.sep, id="demo-widget")

class TagSetSelectorScreen(BaseScreen):

    def demo_widget(self):
        s = len(self.items) // 2
        return TagSetSelector(self.items[:s], self.items[s:], id="demo-widget")

class FilteredTagSetSelectorScreen(BaseScreen):

    def demo_widget(self):
        s = len(self.items) // 2
        return FilteredTagSetSelector(self.items[:s], self.items[s:], id="demo-widget")

selector = {
    "TagSet": TagSetScreen,
    "TagSetSelector": TagSetSelectorScreen,
    "FilteredTagSet": FilteredTagSetScreen,
    "FilteredTagSetSelector": FilteredTagSetSelectorScreen,
}

class SelTestApp(App):

    CSS = """
    .top-level {
        border: white 75%;
        height: 1fr;
     }
    """
    CSS_PATH = "../tagset.tcss"

    def compose(self):

        self.name_count = Input(value="10", placeholder="How many names",
                    validators=[Integer(1, 4690)],
                    id="name-count")
        self.link_text = Input(value="{v}", placeholder="Enter link text format")
        self.item_format = Input(value="[!]", placeholder="Enter entry text format (! becomes link")
        self.separator = Input("\\n", placeholder="Enter separator")
        horiz = Horizontal(id="container")
        with horiz:
            with VerticalScroll(classes="top-level"):
                yield Static(
                "The link text becomes the selection hyperlink for an entry. "
                "The item format must contain a \"!\" to indicate where the "
                "link should appear. The separator is inserted between items."
                "The usual Python escape sequences are available.\n"
                "For selectors, the entries will initially be split evenly "
                "between the two TagSets."
                "\n\nHow many names:")
                yield self.name_count
                yield Static("Link text:")
                yield self.link_text
                yield Static("Item format (link replaces !)")
                yield self.item_format
                yield Static("Item separator")
                yield self.separator
            members = ["TagSet", "TagSetSelector", "FilteredTagSet", "FilteredTagSetSelector"]
            self.type_selector = TagSet(members, sep="\n", id="type-choice", key=lambda x: x, item_fmt="[bold]![/]")
            with VerticalScroll(id="display", classes="top-level"):
                yield Static("Select object type here")
                yield self.type_selector
                yield Button("Quit")
            self.message_box = Static("", id="message-box")
            yield self.message_box

    @on(TagSet.Selected, "#type-choice")
    def tagset_type_selected(self, event):
        n = int(self.name_count.value)
        link_fmt = self.esc_processed(self.link_text.value)
        item_fmt = self.esc_processed(self.item_format.value)
        sep = self.esc_processed(self.separator.value)
        screen_type = selector[event.selected]
        self.app.push_screen(screen_type(n, link_fmt=link_fmt, item_fmt=item_fmt, sep=sep), self.finished_screen)


    @on(TagSet.Selected, "#demo-widget")
    def demo_tagset_selected(self, event):
        self.set_message(f"{event.selected} selected")

    @on(TagSetSelector.Moved, "#demo-widget")
    def moved(self, e: TagSetSelector.Moved):
        self.set_message(f"{e.value} {e.operation}")

    def esc_processed(self, s):
        return codecs.escape_decode(bytes(s, "utf-8"))[0].decode("utf-8")

    def finished_screen(self, message):
        self.name_count.focus()

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

    def on_click(self, event):
        self.log(self.tree)
        #self.log(self.css_tree)

    @on(Button.Pressed)
    def button_pressed(self):
        self.exit()

app = SelTestApp()

if __name__ == '__main__':
    app.run()
