from collections.abc import Iterable, Mapping

from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.events import Event, InputEvent, Message
from textual.widget import Widget
from textual.widgets import Static, Rule, Input

from typing import Optional, Callable

class ClickableStatic(Static):

    def __init__(self, *args, action_func: Optional[Callable[[int], None]] = None, **kw):
        super().__init__(*args, **kw)
        self.action_func = action_func if action_func is not None else self.null_action

    def null_action(self, i):
        pass

    def action_click(self, i):
        return self.action_func(i)


class TagSet(Widget):

    """A set of labels that render as a static.

    Args:
        members: Either a sequence of tags, or a dictionary of tags,
        keyed by unique integers.

        action_func: The action to be taken when a member's link is clicked.
        fmt: The format of a member in the TagSet's string representation.
        key: The key function used to sort the members.
    """
    class Selected(Message):
        def __init__(self, w: Widget, i: int, s: str):
            super().__init__()
            self._control = w
            self.index = i
            self.selected = s
        @property
        def control(self):
            return self._control

    def local_key(self, x: tuple[int, str]):
        seq = reversed(x[1].split())
        return list(seq)

    def __init__(
        self,
        members: dict[int, str], /,
        item_fmt: str | None = None,
        link_fmt: str | None = None,
        key: Optional[Callable[[int], None]] | None = None,
        sep: str = " ",
        *args,
        **kw,
    ):
        super().__init__(*args, **kw)
        self.item_fmt = "[!]" if item_fmt is None else item_fmt
        self.link_fmt = "{v}" if link_fmt is None else link_fmt
        self.key = self.local_key if key is None else key
        self.sep = sep
        if not isinstance(members, Mapping):
            members = dict(enumerate(members))
        self.members = dict(sorted(members.items(), key=self.key))
        self.static = ClickableStatic(Text(""), action_func=self.action_click, id="tagset-static")
        self.filter_string = ""

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
        strings = []
        for (i, v) in sorted(self.members.items(), key=self.key):
            if self.filter_string in v.lower():
                link = f"[@click='click({i})']{self.link_fmt}[/]".format(i=i, v=v)
                item = self.item_fmt.format(i=i, v=v)
                strings.append(item.replace("!", link))
        content = Text.from_markup(self.sep.join(strings))
        self.static.update(content)

    def action_click(self, i: int):
        self.post_message(self.Selected(self, i, self.members[i]))

    def render(self):
        return self.static.render()


class FilteredTagSet(TagSet):

    def compose(self):
        with Vertical():
            yield Input(id="filter-string")
            yield self.static

    @on(Input.Changed)
    def input_changed(self, event: Input.Changed):
        self.filter_string = event.control.value.lower()
        self.update()

class TagSetSelector(Widget):
    """
    Select a set of labels from a closed vocabulary.

    Args:
        selected: An iterable of the currently selected labels.
        unselected: An iterable of the currently deselected labels.
    """
    CSS_PATH = "tagset.tcss"

    tagset_type = TagSet

    class Moved(Message):
        def __init__(self, w, i, v, op):
            super().__init__()
            self._control = w
            self.index = i
            self.value = v
            self.operation = op
        @property
        def control(self):
            return self._control

    def __init__(self, s_tags: list[str], u_tags: list[str], sep=" ", *args, **kw) -> None:
        super().__init__(*args, **kw)
        self.sep = sep
        self.s_dict: dict[int, str] = dict(enumerate(s_tags))
        self.u_dict: dict[int, str] = dict(enumerate(u_tags, start=len(s_tags)))
        self.s_tags = self.tagset_type(self.s_dict, id="selected-set", sep=self.sep)
        self.u_tags = self.tagset_type(self.u_dict, id="unselected-set", sep=self.sep)

    def compose(self) -> ComposeResult:
        with Horizontal(id="lss-selector"):
            yield self.s_tags
            yield self.u_tags

    def update_view(self) -> None:
        self.s_tags.update(members=self.s_dict)
        self.u_tags.update(members=self.u_dict)

    @on(TagSet.Selected, "#selected-set")
    def deselect(self, e: TagSet.Selected) -> None:
        self.app.log("Triggered deselect")
        i = e.index
        self.app.log(self.s_dict)
        self.app.log(f"Index: {i}")
        self.app.log(f"Value: {e.selected}")
        assert i in self.s_dict
        value = self.s_dict.pop(i)
        self.u_dict[i] = value
        self.update_view()
        self.post_message(TagSetSelector.Moved(self, e.index, e.selected, "deselected"))

    @on(TagSet.Selected, "#unselected-set")
    def select(self, e: TagSet.Selected, ) -> None:
        self.app.log("Triggered select")
        i = e.index
        self.app.log(self.u_dict)
        self.app.log(f"Index: {i}")
        self.app.log(f"Value: {e.selected}")
        assert i in self.u_dict
        value = self.u_dict.pop(i)
        self.s_dict[i] = value
        self.update_view()
        self.post_message(TagSetSelector.Moved(self, e.index, e.selected, "selected"))



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
        self.component = TagSet(members)
        TagSet(members)

    def compose(self):
        with Horizontal():
            yield self.component

    def on_click(self, event):
        self.log(self.tree)
        self.log(self.css_tree)

app = TestApp()

if __name__ == '__main__':
    app.run()