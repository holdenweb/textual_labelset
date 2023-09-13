from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Rule
from textual.containers import Vertical, Horizontal, VerticalScroll
from rich.text import Text

from typing import Callable

def sort_key(x):
    k, v = x
    f, l = v.split(None, 1)
    return l, f


class TagSet(Static):
    """A set of labels that render as a static.

    Args:
        members: An iterable of string values.
        action_func: The action to be taken when a member's link is clicked.
        fmt: The format of a member in the TagSet's string representation.
        key: The key function used to sort the members.
    """
    DEFAULT_CSS = "TagSet { width: 30; height: auto; margin: 2; border: yellow 100%; }"

    def __init__(self,
                 members: list[str],
                 action_func: Callable[[int], None],
                 fmt: str, key=None,
                 *args,
                 **kw):
        super().__init__(*args, **kw)
        self.action_func = action_func
        def local_key(x):
            seq = reversed(x[1].split())
            return list(seq)
        self.fmt = fmt
        self.key = local_key if key is None else key
        self.members = dict(sorted(members.items(), key=self.key))

    def render(self):
        strings = [self.fmt.format(i=i, v=v) for (i, v) in self.members.items()]
        return Text.from_markup(" ".join(strings))

    def action_click(self, i: int):
        return self.action_func(i)


class TagSetSelector(Widget):
    """Select a set of labels from a closed vocabulary.

    Args:
        selected: An iterable of the currently selected labels.
        unselected: An iterable of the currently deselected labels.
    """
    DEFAULT_CSS = "TagSetDelector { border: yellow 100%; }"

    def __init__(self, selected: list[str], unselected: list[str], *args, **kw) -> None:
        super().__init__(*args, **kw)
        self.selected = dict(enumerate(selected))
        self.unselected = dict(enumerate(unselected, start=len(selected)))

    def compose(self) -> ComposeResult:
        with Horizontal(id="lss-selector"):
            yield self.selected_labels()
            yield self.unselected_labels()

    def update_view(self) -> None:
        v = self.query_one("#lss-selector")
        v.remove_children()
        v.mount(self.selected_labels())
        v.mount(self.unselected_labels())

    def unselected_labels(self) -> TagSet:
        return TagSet(
            members=self.unselected,
            action_func=self.select,
            fmt="\\[[@click='click({i})']{v}[/]]",
            classes="label-set selected-labels",
        )

    def selected_labels(self) -> TagSet:
        return TagSet(
            members=self.selected,
            action_func=self.deselect,
            fmt="\\[{v} [bold black on white][@click='click({i})']x[/][/bold black on white]]",
            classes="label-set unselected-labels",
        )

    def deselect(self, i: int) -> None:
        assert i in self.selected
        self.unselected[i] = self.selected[i]
        del self.selected[i]
        self.update_view()

    def select(self, i: int) -> None:
        assert i in self.unselected
        self.selected[i] = self.unselected[i]
        del self.unselected[i]
        self.update_view()

class WideTagSetSelector(TagSetSelector):
    """
    TagSetSelector with a custom layout.
    """
    def compose(self) -> ComposeResult:
        with VerticalScroll(id="lss-selector"):
            yield self.selected_labels()
            yield self.unselected_labels()


s = "Tom Dick Harry".split()
u = "Charlie Joe Quentin".split()

def build_app(s: list[str], u: list[str]) -> App:

    class SelTestApp(App):
        def compose(self):
            with VerticalScroll():
                yield TagSetSelector(s, u)
                yield Rule()
                yield WideTagSetSelector(s, u)

    return SelTestApp()

app = build_app(s, u)

if __name__ == '__main__':
    app.run()
