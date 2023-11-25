"""
demo_tagset.py: show off the features of textual_tagset.
"""
from textual.app import App
from textual_tagset import TagSet
from textual_tagset.demo.data import selected

from .baseapp import BaseApp

class SelTestApp(BaseApp):
    def demo_widget(self):
        self.items = dict(enumerate(selected))
        return TagSet(self.items, action_func=self.log_item, key=None, sep="\n")

app = SelTestApp()

if __name__ == '__main__':
    app.run()
