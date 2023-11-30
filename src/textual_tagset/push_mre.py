from textual.app import App, Screen
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Button, Static


class BaseScreen(Screen):

    class Done(Message):
        ...

    def compose(self):
        yield Static("Click it! You know you want to!")
        yield Button("Click to Quit")
        yield Static(":eyes: WATCH THIS SPACE :eyes:", id="message-box")

    @on(Button.Pressed)
    def finish(self, e):
        self.app.post_message(self.Done())
        self.dismiss("Finished!")


class SelTestApp(App):

    CSS = """
    Screen {
        layout: vertical;
    }
    """

    def compose(self):
        yield Button("Click to Fail ...")

    def on_button_pressed(self, event):
        self.push_screen(BaseScreen())


app = SelTestApp()

if __name__ == '__main__':
    app.run()