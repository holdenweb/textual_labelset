"""
demo.py: show off the features of textual_labelset.
"""
from textual.app import App
from textual_labelset import LabelSetSelector

selected = "Yes Oui Ja".split()
deselected = "No Non Nein".split()

lss = LabelSetSelector(selected, deselected)

class LabelSetApp(App):

    def compose(self):
        yield lss

app = LabelSetApp()

if __name__ == '__main__':
    app.run()

