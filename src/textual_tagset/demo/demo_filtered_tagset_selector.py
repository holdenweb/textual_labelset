"""
demo_filtered_tagset_selector.py: demonstrate multi-seletion from a large set.
"""
from textual.app import App
from textual_tagset import FilteredTagSetSelector
from textual_tagset.demo.data import selected, deselected

from .baseapp import BaseApp

class SelTestApp(BaseApp):
    def demo_widget(self):
        return FilteredTagSetSelector(selected, deselected, select_hook=self.log_select, deselect_hook=self.log_deselect)

app = SelTestApp()

if __name__ == '__main__':
    app.run()
