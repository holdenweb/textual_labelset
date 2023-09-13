"""
demo.py: show off the features of textual_tagset.
"""
from textual.app import App
from textual_tagset import TagSetSelector

selected = "Yes Oui Ja".split()
deselected = "No Non Nein".split()

lss = TagSetSelector(selected, deselected)

class TagSetApp(App):

    def compose(self):
        yield lss

app = TagSetApp()

if __name__ == '__main__':
    app.run()

