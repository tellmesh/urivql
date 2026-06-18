from __future__ import annotations

from uri_control.edge.runtime import Runtime

import urivql


def test_ui_detect_mock():
    rt = Runtime()
    urivql.register(rt)
    res = rt.call(
        "vql://local/ui/latest/query/detect",
        {"target": "OK", "boxes": [{"text": "OK", "x": 1, "y": 2, "w": 10, "h": 10}]},
        {"params": {"host": "local"}},
    )
    assert res["ok"]
    assert res["result"]["count"] == 1


def test_ui_compare_changed():
    rt = Runtime()
    urivql.register(rt)
    res = rt.call(
        "vql://local/ui/latest/query/compare",
        {"before": {"a": 1}, "after": {"a": 2}},
        {"params": {"host": "local"}},
    )
    assert res["ok"]
    assert res["result"]["changed"] is True
