import asyncio
import pytest

pytest_plugins = ('pytest_asyncio',)

from textual_tagset.__main__ import build_app, SelTestApp, selected, deselected

@pytest.mark.asyncio
async def test_tagset_static():
    app = build_app([], [])
    test_app = app()
    async with test_app.run_test() as pilot:
        assert len(test_app.query_one("#lss-selector").children) == 2

