import sys

from textual.app import App

class BaseApp(App):
    CSS_PATH = "../tagset.tcss"
    def on_button_pressed(self, e):
        sys.exit()
    def on_click(self, event):
        self.log(self.tree)
        self.log(self.css_tree)
    def set_message(self, m):
        self.query_one("#message-box").update(m)

