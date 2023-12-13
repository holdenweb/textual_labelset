## textual_tagset

A utility to allow selection of choices, either singly or in groups.

### Dependency

Besides the usual Python ecosystem the sole requirement
is the [textual package](https://textualize.io/) itself.
For development you will need [the `poetry` command](https://python-poetry.org/docs/).
Installation is normally straightforward.

### Installation

`textual_tagset` isn't currently available on PyPI, but will be.
At present I'm interested in gathering comments.
For the moment, please follow these instructions.

    git clone git@github.com:holdenweb/textual_tagset.git

if you prefer to use HTTPS:

    git clone https://github.com/holdenweb/textual_tagset.git

In either case, change into the directory you just created.

    cd textual_tagset

We recommend you perform Python development work
inside a virtual environment.
To create a virtual environment with `textual_tagset` already installed,
first select your Python version.
Textual_tagset supports Python 3.8 onwards.

    poetry env use 3.11

Then enter

    poetry install

To build pip-installable artefacts, run

    poetry build

This will create `dist/textual_tagset-X.Y.Z.tar.gz` and
`dist/textual_tagset-X.Y.Z-py3-none-any.whl`, either of
which can be installed with pip.

### Demonstration

A simple demonstration of the modal version of each of the
classes is available by using

    make demo

#### NOTES:

  **To submit the result of the FilteredTagSet and the
  FilteredTagSetSelector you need to press Enter!**

  **The make command requires poetry. If you haven't installed it,
  try**

    textual run textual_tagset.demo

### Usage

A `TagSet` is a set of string tags.
Clicking on a particular tag causes a `TagSet.Selected`
Message to be raised. This has an```index` attribute that
contains the numerical index of the selected element, and
a `selected` attribute containing the selected tag.

A `FilteredTagset` has the same interface as a
`TagSet` but provides an `Input` to enter a filter
string value to limit the choices visible in
the `TagSet` for ease of selection. Pressing the
Enter key the component raises a `TagSetSelector.Selected`
signal whose `values` attribute holds the tags from the
selected set.

The `TagSetSelector` lets you maintain two TagSets, one showing the
the selected tags and the other showing other tags available for
selection. Clicking on a tag moves it from it's present location
to the other set.

As you might expect there's also a `FilteredTagSetSelector`,
which uses `FilteredTagSet`s for the values.
The assumption here was that many more items would
remain unselected than _be_ selected,


### Python API

TagSet and FilteredTagSet have the same API, as do TagSetSelector and
FilteredTageSetSelector.

#### TagSet, FilteredTagSet
#### TagSetSelector, FilteredTagSetSelector

Documentation to be provided once API is stabilised.

### Further development

Development work will aim to increase usability:
User comments and issues are both warmly welcome.