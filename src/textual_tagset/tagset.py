from collections.abc import Iterable, Mapping

from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.events import Event, InputEvent, Message, Key
from textual.widget import Widget
from textual.widgets import Static, Rule, Input, ListView

from typing import Optional, Callable

class ClickableStatic(Static):

    class Clicked(Message):
        def __init__(self, w: Widget, i: int):
            super().__init__()
            self._control = w
            self.i = i
        @property
        def control(self):
            return _control

    def __init__(self, *args, action_func: Optional[Callable[[int], None]] = None, **kw):
        super().__init__(*args, **kw)

    def null_action(self, i):
        pass

    def action_click(self, i):
        self.post_message(self.Clicked(self, i))


class TagSet(Widget):

    """Allow selection of a single label from a given set.

    Parameters
    ----------
    members: Sequence | dict
        Either a sequence of tags, or a dictionary of tags,
        keyed by unique integers.

    item_fmt: Optional[str]:
        A string format determining how each link should appear.
        The links will replace an excalamation mark in this format.
        Defaults to "[!]", so links will appear in square brackets.
    link_fmt: Optional[str]:
        A string format determining what goes inside each link.
        Use {i} to include the key of a tag, {v} to include
        the tag value itself. Defaults to {v}, the tag value.
    sep: Optional[str]:
        A string used to separate the tags. Defaults to "\n".
    modal: bool:
        Detarmines whether the component or its modal version
        is being displayed.
    """
    def __init__(
        self,
        members: dict[int, str], /,
        item_fmt: Optional[str] = None,
        link_fmt: Optional[str] = None,
        key: Optional[Callable[[tuple[int, str]], list[str]]] = None,
        sep: str = " ",
        modal: bool = True,
        *args,
        **kw,
    ):
        super().__init__(*args, **kw)
        self._item_fmt = "[!]" if item_fmt is None else item_fmt
        self._link_fmt = "{v}" if link_fmt is None else link_fmt
        self._key = self._local_key if key is None else key
        self._sep = sep
        self._modal = modal
        if not isinstance(members, Mapping):
            members = dict(enumerate(members))
        self.members = dict(sorted(members.items(), key=self._key))
        self.static = ClickableStatic(Text(""), id="tagset-static")
        self._filter_string = ""
        self.can_focus = True
        self._key_value: str = ""

    class Selected(Message):
        def __init__(self, w: Widget, i: int, s: str):
            super().__init__()
            self._control = w
            self.index = i
            self.selected = s
        @property
        def control(self):
            return self._control

    def _local_key(self, x: tuple[int, str]) -> list[str]:
        seq = reversed(x[1].split())
        return list(seq)

    def _push(self, key, value):
        self.members[key] = value
        self.update()

    def _pop(self, key):
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
        for (i, v) in sorted(self.members.items(), key=self._key):
            if self._filter_string in v.lower():
                link = f"[@click='click({i})']{self._link_fmt}[/]".format(i=i, v=v)
                item = self._item_fmt.format(i=i, v=v)
                strings.append(item.replace("!", link))
        content = Text.from_markup(self._sep.join(strings))
        self.static.update(content)

    def action_click(self, i: int):
        self._key_value = self.members[i]
        self.post_message(self.Selected(self, i, self._key_value))

    def render(self):
        return self.static.render()

    def result(self):
        return self._key_value

    @on(ClickableStatic.Clicked)
    def tagset_selected(self, event: Selected):
        """
        When the TagSet is modal, the selected element is returned
        as the result of the modal screen. Otherwise the Selected
        message bubbles to the DOM parent of the TagSet.
        """
        self.app.log(self.tree)
        if self._modal:
            self.screen.dismiss(self.members[event.i])
        else:
            self.post_message(self.Selected(self, (i := event.i), self.members[i]))

class FilteredTagSet(TagSet):
    """Allow selection of a tag from a set"""
    def compose(self):
        with Vertical():
            yield Input(id="filter-string")
            yield self.static

    @on(Input.Changed)
    def input_changed(self, event: Input.Changed):
        self._filter_string = event.control.value.lower()
        self.update()

    @on(Input.Submitted)
    def input_submitted(self, event: Input.Submitted):
        pass

class SelectorBase(Widget):
    """
    Select a set of labels from a closed vocabulary.

    Args:
        selected: An iterable of the currently selected labels.
        unselected: An iterable of the currently deselected labels.
    """
    CSS_PATH = "tagset.tcss"
    tagset_type: type[TagSet] | type[FilteredTagSet]

    class Meta:
        abstract = True

    class Moved(Message):
        def __init__(self, w: Widget, i: int, v: str, op: str):
            super().__init__()
            self._control = w
            self.index = i
            self.value = v
            self.operation = op
        @property
        def control(self):
            return self._control


    def __init__(self, s_choices: list[str], u_choices: list[str], link_fmt="{v}", item_fmt="[!]", sep=" ", modal: bool = False,
                 *args, **kw) -> None:
        super().__init__(*args, **kw)
        self._sep = sep
        self.s_dict: dict[int, str] = dict(enumerate(s_choices))
        self.u_dict: dict[int, str] = dict(enumerate(u_choices, start=len(s_choices)))
        self._link_fmt = link_fmt
        self._item_fmt = item_fmt
        self.s_tags = self.tagset_type(self.s_dict, link_fmt=self._link_fmt, item_fmt=self._item_fmt, sep=self._sep, modal=False, id="selected-set")
        self.u_tags = self.tagset_type(self.u_dict, link_fmt=self._link_fmt, item_fmt=self._item_fmt, sep=self._sep, modal=False, id="unselected-set")
        self._modal = modal
        self.can_focus = True

    class Selected(Message):
        def __init__(self, w, values):
            super().__init__()
            self._control = w
            self.values = values
        @property
        def control(self):
            return self._control

    def compose(self) -> ComposeResult:
        with Horizontal(id="lss-selector"):
            yield self.s_tags
            yield self.u_tags

    def result(self):
        return list(self.s_dict.values())

    def update_view(self) -> None:
        self.s_tags.update(members=self.s_dict)
        self.u_tags.update(members=self.u_dict)

    @on(TagSet.Selected, "#selected-set")
    def deselect(self, e: TagSet.Selected) -> None:
        e.stop()
        i = e.index
        assert i in self.s_dict
        value = self.s_dict.pop(i)
        self.u_dict[i] = value
        self.update_view()
        self.post_message(self.Moved(self, e.index, e.selected, "deselected"))

    @on(TagSet.Selected, "#unselected-set")
    def select(self, e: TagSet.Selected, ) -> None:
        e.stop()
        i = e.index
        assert i in self.u_dict
        value = self.u_dict.pop(i)
        self.s_dict[i] = value
        self.update_view()
        self.post_message(self.Moved(self, e.index, e.selected, "selected"))

    @on(Input.Submitted)
    def input_submitted(self, e: Input.Submitted):
        if self._modal:
            self.screen.dismiss(self.s_dict.values())
        else:
            self.post_message(self.Selected(self, self.s_dict.values()))

class TagSetSelector(SelectorBase):

    tagset_type = TagSet


class FilteredTagSetSelector(TagSetSelector):
    """
    TagSetSelector with a custom layout.

    We subclass TagSetSelector rather than SelectorBase
    so messages can be checked as coing from the former
    class.
    """
    tagset_type = FilteredTagSet

