"""
demo_tagset_selector.py: demonstrate the basic features of textual_tagset.
"""
from textual.app import App
from textual_tagset import TagSetSelector
from textual_tagset.demo.data import selected, deselected

from .baseapp import BaseApp

class SelTestApp(BaseApp):
    def demo_widget(self):
        return TagSetSelector(selected, deselected, sep=" ", select_hook=self.log_select, deselect_hook=self.log_deselect)

app = SelTestApp()

if __name__ == '__main__':
    app.run()
