from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Label, Rule, Input
from textual.containers import Vertical, Horizontal, VerticalScroll
from rich.text import Text

from typing import Callable

DEFAULT_SELECTED_FORMAT = "\\[{v} [@click='klick({i})']x[/]]"
DEFAULT_UNSELECTED_FORMAT = "\\[[@click='klick({i})']{v}[/]]"


class TagSet(Widget):

    """A set of labels that render as a static.

    Args:
        members: A dictionary of tags, keyed by unique integers
        action_func: The action to be taken when a member's link is clicked.
        fmt: The format of a member in the TagSet's string representation.
        key: The key function used to sort the members.
    """
    filter_string = ""

    def __init__(
        self,
        members: dict[int, str],
        action_func: Callable[[int], None],
        fmt: str,
        key: Callable[..., object] | None = None,
        *args,
        **kw,
    ):
        def local_key(x: tuple[int, str]):
            seq = reversed(x[1].split())
            return list(seq)

        super().__init__(*args, **kw)
        self.action_func = action_func
        self.key = local_key if key is None else key
        self.fmt = fmt
        self.members = dict(sorted(members.items(), key=self.key))
        self.static = Label(Text(""), id="tagset-static")

    def push(self, key, value):
        assert key not in self.members
        self.members[key] = value

    def pop(self, key):
        assert key in self.members
        return self.members.pop(key)

    def compose(self):
        with Vertical():
            yield self.static

    def on_mount(self):
        self.update()

    def update(self):
        strings = [self.fmt.format(i=i, v=v) for (i, v) in self.members.items() if self.filter_string in v.lower()]
        content = Text.from_markup(" ".join(strings))
        self.static.update(content)

    def action_klick(self, i: int):
        print("CLICKED ON", i)
        return self.action_func(i)

    def render(self):
        return Text.from_markup(" ".join(self.fmt.format(i=i, v=v) for (i, v) in self.members.items() if self.filter_string in v))



class FilteredTagSet(TagSet):

    def compose(self):
        with Vertical():
            yield Input(id="filter-string")
            yield self.static

    def on_input_changed(self, event):
        #
        # Probable issue here:
        # We replace the static when the input changes, but we
        # also want to update it when an element is removed or added
        # rather than creating a whole new TagSetStatic.
        #
        self.filter_string = event.input.value.lower()
        super().update()
        #self.static.remove()
        #self.static = TagSetStatic(members={k: v for (k, v) in self.members.items() if value in v.lower()},
                                   #action_func=self.action_func,
                                   #fmt=self.fmt)
        #self.container.mount(self.static)

class TagSetSelector(Widget):
    """
    Select a set of labels from a closed vocabulary.

    Args:
        selected: An iterable of the currently selected labels.
        unselected: An iterable of the currently deselected labels.
    """
    CSS_PATH = "tagset.tcss"

    tagset_type = TagSet

    def __init__(self, selected_labels: list[str], unselected_labels: list[str], *args, **kw) -> None:
        super().__init__(*args, **kw)
        self.selected: dict[int, str] = dict(enumerate(selected_labels))
        self.unselected: dict[int, str] = dict(enumerate(unselected_labels, start=len(selected_labels)))

    def compose(self) -> ComposeResult:
        with Horizontal(id="lss-selector"):
            yield TagSet(self.selected, self.deselect, fmt=DEFAULT_SELECTED_FORMAT, id="selected-set")
            yield self.tagset_type(self.unselected, self.select, fmt=DEFAULT_UNSELECTED_FORMAT, id="unselected-set")

    def update_view(self) -> None:
        v = self.query_one("#lss-selector")
        #
        # Multiple issues here.
        # 1. Since only the unselected tags can change there's
        #    no need to rebuild the whole container.
        # 2. Creating a new unselected FilteredTagSet destroys
        #    the continuity of the filtering input.
        #
        self.query_one("#selected_set").update(self.selected)
        self.query_one("#uselected-set").update(seld.unselected)

    def unselected_tags(self) -> TagSet:
        return self.tagset_type(
            members=self.unselected,
            action_func=self.select,
            fmt=DEFAULT_UNSELECTED_FORMAT,
            classes="label-set selected-labels",
        )

    def selected_tags(self) -> TagSet:
        return TagSet(
            members=self.selected,
            action_func=self.deselect,
            fmt=DEFAULT_SELECTED_FORMAT
        )

    def deselect(self, i: int) -> None:
        assert i in self.selected
        value = self.selected.pop(i)
        self.unselected[i] = value
        self.update_view()

    def select(self, i: int) -> None:
        assert i in self.unselected
        value = self.unselected.pop(i)
        self.selected[i] = value
        self.update_view()


class FilteredTagSetSelector(TagSetSelector):
    """
    TagSetSelector with a custom layout.
    """
    tagset_type = FilteredTagSet

    def compose(self) -> ComposeResult:
        with Vertical(id="lss-selector"):
            yield TagSet(self.selected, self.deselect, fmt=DEFAULT_SELECTED_FORMAT)
            yield FilteredTagSet(self.unselected, self.select, fmt=DEFAULT_UNSELECTED_FORMAT)

s = "Tom Dick Harry".split()
u = "Charlie Joe Quentin".split()

fmt = "{v}"


def ignore(i):
    pass


class TestApp(App):

    CSS_PATH = "tagset.tcss"

    def __init__(self):
        super().__init__()
        members = dict(enumerate(s))
        self.component = FilteredTagSet(members, ignore, fmt)

    def compose(self):
        with Horizontal():
            yield self.component

    def on_click(self, event):
        self.log(self.tree)

app = TestApp()

if __name__ == '__main__':
    app.run()