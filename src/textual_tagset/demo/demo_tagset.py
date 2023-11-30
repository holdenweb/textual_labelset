"""
demo_tagset.py: show off the features of textual_tagset.
"""
from textual import on
from textual.app import App
from textual.containers import Vertical
from textual.validation import Integer
from textual.widgets import Input
from textual_tagset import TagSet
from textual_tagset.demo.data import random_names

from .baseapp import BaseScreen

class TagSetScreen(BaseScreen):

    def __init__(self, n):
        self.n = n
        self.items = dict(enumerate(random_names(self.n)))
        super().__init__(self.items)
    def demo_widget(self):
        return TagSet(self.items, action_func=self.log_item, key=None, sep="\n")

class SelTestApp(App):

    CSS = """
    Screen {
        layout: vertical;
    }
    """

    def compose(self):
        self.input = Input(placeholder="How many names",
                    validators=[Integer(1, 4900)],
                    id="name-count")
        yield self.input

    @on(Input.Submitted)
    def input_submitted(self, event):
        n = int(event.control.value)
        self.app.push_screen(TagSetScreen(n), self.finished_screen)

    def finished_screen(self, message):
        self.reset_inputs()

    def reset_inputs(self):
        self.input.clear()
        self.input.focus()

app = SelTestApp()

if __name__ == '__main__':
    app.run()
