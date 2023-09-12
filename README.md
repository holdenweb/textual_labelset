## textual-labelset

A utility to allow easy maintenance of labels/tags
from a controlled vocabulary.

### Installation

We always recommend Python development work is performed
inside a virtual environment.
To install, activate your virtual environment and enter

    pip install textual_labelset

### Usage

A LabelSet is a fixed vocabulary
in which some or all of the values may be selected.
You create one by calling the LabelSet
constructor with two sequences,
one of selected values and the other of
deselected values.

LabelSets are presented internally as dictionaries
in which each label has a unique key.

The default representation shows each labelset
as a variable-height area of selected values
next to a similar area of deselected values.
The following code gives a simple example.
If you have both textual and textual_labelset installed
you can run it with the command

    textual run textual_labelset.demo

Here's the code

```python
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
```
### Development

This code is under construction.
Development work will aim to increase usability:

1. Make sorting somewhat easier to configure.
2. Make it easier to change the appearance of the selected
   and deselected items.

