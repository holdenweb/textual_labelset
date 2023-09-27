from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Rule, Input
from textual.containers import Vertical, Horizontal, VerticalScroll
from rich.text import Text

from typing import Callable

DEFAULT_SELECTED_FORMAT = "\\[{v} [@click='klick({i})']x[/]]"
DEFAULT_UNSELECTED_FORMAT = "\\[[@click='klick({i})']{v}[/]]"


class ClickableStatic(Static):

    def __init__(self, *args, action_func: Callable[[int], None] | None = None, **kw):
        super().__init__(*args, **kw)
        self.action_func = action_func

    def action_klick(self, i):
        return self.action_func(i)


class TagSet(Widget):

    """A set of labels that render as a static.

    Args:
        members: A dictionary of tags, keyed by unique integers
        action_func: The action to be taken when a member's link is clicked.
        fmt: The format of a member in the TagSet's string representation.
        key: The key function used to sort the members.
    """
    filter_string = ""

    def local_key(self, x: tuple[int, str]):
        seq = reversed(x[1].split())
        return list(seq)

    def __init__(
        self,
        members: dict[int, str],
        action_func: Callable[[int], None] = None,
        fmt: str = "{v}",
        key: Callable[..., object] | None = None,
        *args,
        **kw,
    ):
        super().__init__(*args, **kw)
        self.action_func = (lambda i: None) if action_func is None else action_func
        self.key = self.local_key if key is None else key
        self.fmt = fmt
        self.members = dict(sorted(members.items(), key=self.key))
        self.static = ClickableStatic(Text(""), action_func=self.action_klick, id="tagset-static")

    def push(self, key, value):
        assert key not in self.members
        self.members[key] = value
        self.update()

    def pop(self, key):
        assert key in self.members
        v = self.members.pop(key)
        self.update()
        return v

    def compose(self):
        with Vertical():
            yield self.static

    def on_mount(self):
        self.update()

    def update(self, members=None):
        if members is not None:
            self.members = members
        strings = [
            self.fmt.format(i=i, v=v)
            for (i, v) in sorted(self.members.items(), key=self.key)
            if self.filter_string in v.lower()
        ]
        content = Text.from_markup(" ".join(strings))
        self.static.update(content)

    def action_klick(self, i: int):
        print("CLICKED ON", i)
        return self.action_func(i)

    def render(self):
        return self.static.render()


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

class TagSetSelector(Widget):
    """
    Select a set of labels from a closed vocabulary.

    Args:
        selected: An iterable of the currently selected labels.
        unselected: An iterable of the currently deselected labels.
    """
    CSS_PATH = "tagset.tcss"

    tagset_type = TagSet

    def __init__(self, s_tags: list[str], u_tags: list[str], *args, **kw) -> None:
        super().__init__(*args, **kw)
        self.s_dict: dict[int, str] = dict(enumerate(s_tags))
        self.u_dict: dict[int, str] = dict(enumerate(u_tags, start=len(s_tags)))
        self.s_tags = TagSet(self.s_dict, fmt=DEFAULT_SELECTED_FORMAT, action_func=self.deselect, id="selected-set")
        self.u_tags = self.tagset_type(self.u_dict, fmt=DEFAULT_UNSELECTED_FORMAT, action_func=self.select, id="unselected-set")

    def compose(self) -> ComposeResult:
        with Horizontal(id="lss-selector"):
            yield self.s_tags
            yield self.u_tags

    def update_view(self) -> None:
        self.s_tags.update(members=self.s_dict)
        self.u_tags.update(members=self.u_dict)

    def deselect(self, i: int) -> None:
        assert i in self.s_dict
        value = self.s_dict.pop(i)
        self.u_dict[i] = value
        self.update_view()

    def select(self, i: int) -> None:
        assert i in self.u_dict
        value = self.u_dict.pop(i)
        self.s_dict[i] = value
        self.update_view()


class FilteredTagSetSelector(TagSetSelector):
    """
    TagSetSelector with a custom layout.
    """
    tagset_type = FilteredTagSet

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