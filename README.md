## textual_tagset

A utility to allow selection of choices, either singly or in groups.

To get a flavour of what the package can do, after installation run

    python -m textual_tagset.demo

This lets you play with the four object types the tagset package offers
choosing the number of items you want to work with.
See the **Demonstration** section below.

![The tagset demo utility](CC-SA-88x31.png)
### Dependency

Besides the usual Python ecosystem the sole requirement
is the [textual package](https://textualize.io/) itself.

For development you will need [the `poetry` command](https://python-poetry.org/docs/).
Installation is normally straightforward.

### Installation

`textual_tagset` is available on PyPI, which will be
by far the simplest installation. Simply create a virtual environment (while not strictly necessary
this is stringly advised) and with the environment activated issue the command

    pip install textual-tagset

I'm very interested in gathering comments. For development feel free to download a copy

    git clone git@github.com:holdenweb/textual-tagset.git

if you prefer to use HTTPS:

    git clone https://github.com/holdenweb/textual-tagset.git

In either case, change into the directory you just created.

    cd textual_tagset

We really do recommend you perform Python development work
inside a virtual environment.
To create a virtual environment with `textual_tagset` already installed,
first select your Python version.
Textual_tagset supports Python 3.9 onwards.

    poetry env use 3.11

Then enter

    poetry install

To build pip-installable artefacts, run

    poetry build

This will create `dist/textual_tagset-X.Y.Z.tar.gz` and
`dist/textual_tagset-X.Y.Z-py3-none-any.whl`, either of
which can be installed with pip.

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
selection. Clicking on a tag moves it from one set to the other.

As you might expect there's also a `FilteredTagSetSelector`,
which uses `FilteredTagSet`s for the values.
The filtered variants are especially useful when tags must
be selected from an intractably large set.
In the filtered versions, interaction is terminated by
pressing return.


### Python API

TagSet and FilteredTagSet have the same API, as do TagSetSelector and
FilteredTageSetSelector.

#### TagSet, FilteredTagSet
#### TagSetSelector, FilteredTagSetSelector

Documentation to be provided once API is stabilised.

### Further development

Development work will aim to increase usability:
User comments and issues are both warmly welcome.