from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Rule
from textual.containers import Vertical, Horizontal, VerticalScroll
from rich.text import Text

from typing import Callable

DEFAULT_SELECTED_FORMAT = "\\[{v} [@click='klick({i})']x[/]]"
DEFAULT_UNSELECTED_FORMAT = "\\[[@click='klick({i})']{v}[/]]"


class TagSetStatic(Static):
    """A set of labels that render as a static.

    Args:
        members: A dictionary of tags, keyed by unique integers
        action_func: The action to be taken when a member's link is clicked.
        fmt: The format of a member in the TagSet's string representation.
        key: The key function used to sort the members.
    """
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

    def push(self, key, value):
        assert key not in self.members
        self.members[key] = value

    def pop(self, key):
        assert key in self.members
        return self.members.pop(key)

    def update(self, members):
        print("")
        strings = [self.fmt.format(i=i, v=v) for (i, v) in self.members.items()]
        super().update(" ".join(strings))

    def action_klick(self, i: int):
        print("CLICKED ON", i)
        return self.action_func(i)

    def render(self):
        return Text.from_markup(" ".join(self.fmt.format(i=i, v=v) for (i, v) in self.members.items()))


class TagSet(Widget):
    """
    Turns a dict of tags into a renderable widget.
    """

    def __init__(self,
                 members: dict[int, str],
                 action_func: Callable[[int], None],
                 fmt: str, key=None,
                 *args,
                 **kw
    ):
        super().__init__(*args, **kw)
        print("TAG SET INITIALISE")
        self.container = Vertical(id="tag-set")
        self.static = TagSetStatic(members=members, action_func=action_func, fmt=fmt)

    def compose(self):
        with self.container:
            yield self.static


class TagSetSelector(Widget):
    """
    Select a set of labels from a closed vocabulary.

    Args:
        selected: An iterable of the currently selected labels.
        unselected: An iterable of the currently deselected labels.
    """
    CSS_PATH = "tagset.tcss"

    def __init__(self, selected_labels: list[str], unselected_labels: list[str], *args, **kw) -> None:
        super().__init__(*args, **kw)
        self.selected: dict[int, str] = dict(enumerate(selected_labels))
        self.unselected: dict[int, str] = dict(enumerate(unselected_labels, start=len(selected_labels)))

    def compose(self) -> ComposeResult:
        with Horizontal(id="lss-selector"):
            yield TagSet(self.selected, self.deselect, fmt=DEFAULT_SELECTED_FORMAT)
            yield TagSet(self.unselected, self.select, fmt=DEFAULT_UNSELECTED_FORMAT)

    def update_view(self) -> None:
        v = self.query_one("#lss-selector")
        v.remove_children()
        v.mount(self.selected_tags())
        v.mount(self.unselected_tags())

    def unselected_tags(self) -> TagSet:
        return TagSet(
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
        self.unselected.push(i, value)
        self.update_view()

    def select(self, i: int) -> None:
        assert i in self.unselected
        value = self.unselected.pop(i)
        self.selected.push(i, value)
        self.update_view()


class FilteredTagSetSelector(TagSetSelector):
    """
    TagSetSelector with a custom layout.
    """
    def compose(self) -> ComposeResult:
        with Vertical(id="lss-selector"):
            yield TagSet(self.selected, self.deselect, fmt=DEFAULT_SELECTED_FORMAT)
            yield TagSet(self.unselected, self.select, fmt=DEFAULT_UNSELECTED_FORMAT)

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
        self.component = TagSetStatic(members, ignore, fmt)

    def compose(self):
        with Horizontal():
            yield self.component

    def on_click(self, event):
        self.log(self.tree)

app = TestApp()

if __name__ == '__main__':
    app.run()