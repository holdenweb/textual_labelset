"""
demo_filtered_tagset.py: show selection from a large set.
"""
from textual.app import App
from textual_tagset import FilteredTagSet
from textual_tagset.demo.data import selected, deselected

from .baseapp import BaseApp

class SelTestApp(BaseApp):
    def demo_widget(self):
        self.items = dict(enumerate(selected))
        return FilteredTagSet(self.items, action_func=self.log_item, sep=" | ")

app = SelTestApp()

if __name__ == '__main__':
    app.run()
