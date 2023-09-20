import asyncio
import pytest

from rich.text import Text
from textual.app import App


pytest_plugins = ('pytest_asyncio',)

from textual_tagset import TagSet, TagSetStatic, FilteredTagSetStatic

def ignore(i):
    pass


def build_app(ts_type, members=[], fmt="{v}"):

    class TestApp(App):

        def __init__(self):
            super().__init__()
            self.members = dict(enumerate(members))
            self.action_func = ignore
            self.fmt = fmt
            # assert ts_type == list
            self.component = ts_type(self.members, ignore, fmt)

        def compose(self):
            yield self.component

        def on_click(self, event):
            self.log(self.tree)

    return TestApp

@pytest.mark.asyncio
@pytest.mark.parametrize("ts_class", [TagSetStatic, FilteredTagSetStatic])
async def test_tagset_static_empty(ts_class):
    app = build_app(ts_type=ts_class, fmt="{v}")
    test_app = app()
    async with test_app.run_test() as pilot:
        ch = test_app.query_one(TagSetStatic)
        assert type(ch.render()) == Text
        assert ch.render().plain == ""


@pytest.mark.asyncio
@pytest.mark.parametrize("ts_class", [TagSetStatic, FilteredTagSetStatic])
async def test_tagset_static_nonempty(ts_class):
    app = build_app(ts_class, ["a", "b"], fmt="{v}")
    test_app = app()
    async with test_app.run_test() as pilot:
        ch = test_app.query_one(TagSetStatic)
        assert ch.render().plain == "a b"


@pytest.mark.asyncio
@pytest.mark.parametrize("ts_class", [TagSetStatic, FilteredTagSetStatic])
async def test_tagset_static_formatting(ts_class):
    app = build_app(ts_class, ["a", "b"], fmt="\\[{v} [@click='klick({i})']x[/]]")
    test_app = app()
    async with test_app.run_test() as pilot:
        ch = test_app.query_one(TagSetStatic)
        assert ch.render().plain == "[a x] [b x]"


@pytest.mark.asyncio
async def test_tagset_static_push_pop():
    app = build_app(TagSetStatic, [], fmt="[{i} {v}]")
    test_app = app()
    async with test_app.run_test() as pilot:
        static = test_app.component
        static.push(1, "a")
        assert static.render().plain == "[1 a]"
        static.push(2, "b")
        assert static.render().plain == "[1 a] [2 b]"
        static.pop(1)
        assert static.render().plain == "[2 b]"