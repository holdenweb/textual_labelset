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

    poetry env create 3.11

Then enter

    poetry install

To build pip-installable artefacts, run

    poetry build

This will create `dist/textual_tagset-X.Y.Z.tar.gz` and
`dist/textual_tagset-X.Y.Z-py3-none-any.whl`, either of
which can be installed with pip.

### Usage

A `TagSet` is a set of string tags.
You won't normally use them directly,
but you can create one by calling the `TagSet`
constructor with a dict of string values, each
of which has a unique integer key.
A more convenient API would clearly be helpful,
and will likely emerge shortly.

A `FilteredTagset` has the same interface as a
`TagSet` but provideses an `Input` to enter a filter
string value to limit the choices available in
the `TagSet` for ease of selection.

You create a `TagSetSelector` by providing two
dicts, one containing the selected labels and
the other containing the deselected labels.
Note that the keys must be nnumeric, and unique across
both dicts.

As you might expect there's also a `FilteredTagSetSelector`,
which uses `FilteredTagSet`s for the values.
The assumption here was that many more items would
remain unselected than _be_ selected,

The default representation  of a `FilteredtTagSetSelector` shows each tagset
as a variable-height area of selected values
next to a similar area of deselected values.

More documentation will follow on demand.
No demand, no more documentation :).

### Demonstrations and Code Samples

A simple demonstration of each of the classes is available
by using `make demo`. NOTE: **to submit the result of the
FilteredTagSet and the FilteredTagSetSelector you need to
press Enter!**

Development work will aim to increase usability:

1. Make sorting somewhat easier to configure (at present
   it uses a slightly bizarre algorithm to sort names correctly).
2. Make it easier to configure the formats used for the selected
   and deselected items.
3. Simplify the API.

