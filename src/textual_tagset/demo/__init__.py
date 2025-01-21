"""
demo_tagset.py: show off the features of textual_tagset.
"""
import codecs

from textual import on
from textual.app import App
from textual.containers import VerticalScroll, Horizontal, Vertical, Grid
from textual.validation import Integer
from textual.widgets import Input, Static, Button
from .. import TagSet, FilteredTagSet, TagSetSelector, FilteredTagSetSelector

from .basescreen import BaseScreen

class ModalTagSet(BaseScreen):

    def demo_widget(self):
        return TagSet(self.items, link_fmt=self._link_fmt, item_fmt=self._item_fmt, sep=self._sep, id="demo-widget")

class ModalFilteredTagSet(BaseScreen):

    def demo_widget(self):
        return FilteredTagSet(self.items, link_fmt=self._link_fmt, item_fmt=self._item_fmt, sep=self._sep, id="demo-widget")

class ModalTagSetSelector(BaseScreen):

    def demo_widget(self):
        s = len(self.items) // 2
        return TagSetSelector(self.items[:s], self.items[s:], link_fmt=self._link_fmt, item_fmt=self._item_fmt, sep=self._sep, id="demo-widget")

class ModalFilteredTagSetSelector(BaseScreen):

    def demo_widget(self):
        s = len(self.items) // 2
        return FilteredTagSetSelector(self.items[:s], self.items[s:], link_fmt=self._link_fmt, item_fmt=self._item_fmt, sep=self._sep, id="demo-widget")

selector = {
    "TagSet": ModalTagSet,
    "TagSetSelector": ModalTagSetSelector,
    "FilteredTagSet": ModalFilteredTagSet,
    "FilteredTagSetSelector": ModalFilteredTagSetSelector,
}

class SelTestApp(App):

    CSS = """
    """
    CSS_PATH = "../tagset.tcss"

    def compose(self):

        self.name_count = Input(value="40", placeholder="How many names",
                    validators=[Integer(1, 4690)],
                    id="name-count")
        self.link_text = Input(value="{v}", placeholder="Enter link text format")
        self.item_format = Input(value="[!]", placeholder="Enter entry text format (! becomes link")
        self.separator = Input("\\n", placeholder="Enter separator")
        with Vertical():
            yield Static(
            "The link text becomes the selection hyperlink for an entry. "
            "The item format must contain a \"!\" to indicate where the "
            "link should appear. The separator is inserted between items. "
            "The usual Python escape sequences are available.\n"
            "For selectors, the entries are initially split evenly "
            "between the two TagSets.")
            with Horizontal(id="container"):
                with VerticalScroll(classes="top-level"):
                    with Grid(id="questions"):
                        yield Static("\nHow many names:")
                        yield self.name_count
                        yield Static("\nLink text:")
                        yield self.link_text
                        yield Static("Item format (link replaces!)")
                        yield self.item_format
                        yield Static("\nItem separator")
                        yield self.separator
                members = ["TagSet", "TagSetSelector", "FilteredTagSet", "FilteredTagSetSelector"]
                self.type_selector = TagSet(members, sep="\n", id="type-choice", key=lambda x: x, item_fmt="[bold]![/]", modal=False)
                with VerticalScroll(id="display", classes="top-level"):
                    yield Static("Click on required object type")
                    yield self.type_selector
                    yield Button("Quit")
            with VerticalScroll(id="message"):
                self.message_box = Static("", id="message-box")
                yield self.message_box

    @on(TagSet.Selected, "#type-choice")
    async def tagset_type_selected(self, event):
        n = int(self.name_count.value)
        link_fmt = self.decoded(self.link_text.value)
        item_fmt = self.decoded(self.item_format.value)
        sep = self.decoded(self.separator.value)
        screen_type = selector[event.selected]
        await self.app.push_screen(screen_type(n, link_fmt=link_fmt, item_fmt=item_fmt, sep=sep), self.finished_screen)
        self.app.query_one("#widget-container").focus()

    @on(TagSet.Selected, "#demo-widget")
    def demo_tagset_selected(self, event):
        self.set_message(f"{event.selected} selected")

    @on(TagSetSelector.Moved, "#demo-widget")
    def moved(self, e: TagSetSelector.Moved):
        self.set_message(f"{e.value} {e.operation}")


    def decoded(self, s):
        return codecs.escape_decode(bytes(s, "utf-8"))[0].decode("utf-8")

    def finished_screen(self, message):
        self.set_message(f"{message} selected")
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

def main():
    return app.run()

app = SelTestApp()

if __name__ == '__main__':
    main()
