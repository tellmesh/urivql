# UriPack: urivql

Self-contained Markpact — definitions, full source, run config. Unpack & run: `urisys markpact run urivql/urivql.markpact.md --as service` (writes `.markpact/`).

```yaml markpact:pack
apiVersion: urisys.io/v1
kind: UriPack
metadata:
  id: urivql-pack
  version: 1.0.0
  language: python
description: Visual query language — UI detect/compare for urisys-node.
schemes:
- vql
capabilities:
- id: vql.ui.detect
  uri: vql://{host}/ui/latest/query/detect
  kind: query
  operation: vql.ui.detect
  handler: python://urivql.handlers:ui_detect
  side_effects: false
  approval: not_required
- id: vql.ui.compare
  uri: vql://{host}/ui/latest/query/compare
  kind: query
  operation: vql.ui.compare
  handler: python://urivql.handlers:ui_compare
  side_effects: false
  approval: not_required
policy:
  default: deny_mutations_without_approval
runtime:
  default_environment: mock
  supports:
  - mock
  - local
  - docker
```

```yaml markpact:run
modes:
- pack
- service
- flow
- interface
- adapter
default: service
scheme: vql
service:
  port: 8790
  wire: POST /uri/call
flow:
  ids: []
adapter:
  wire: POST /uri/call
  events: GET /events
```

```python markpact:module path=urivql/__init__.py
from __future__ import annotations

from importlib.resources import files

from .routes import register

__all__ = ["register", "manifest_path"]


def manifest_path():
    return files(__package__).joinpath("manifest.yaml")
```

```python markpact:module path=urivql/handlers.py
from __future__ import annotations

from typing import Any


def ui_detect(payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    target = str(payload.get("target") or payload.get("text") or payload.get("selector") or "")
    boxes = (context.get("state", {}).get("latest_ocr") or {}).get("boxes") or payload.get("boxes") or []
    matches = []
    for box in boxes:
        text = str(box.get("text") or "")
        if not target or target.lower() in text.lower():
            matches.append(box)
    return {
        "target": target,
        "matches": matches[:20],
        "count": len(matches),
        "source": "urivql-mock",
    }


def ui_compare(payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    before = payload.get("before") or context.get("state", {}).get("screen_before")
    after = payload.get("after") or context.get("state", {}).get("screen_after")
    expect = payload.get("expect") or {}
    changed = before != after if before is not None and after is not None else bool(expect.get("changed", True))
    ok = changed if expect.get("changed") is None else (changed == bool(expect.get("changed")))
    return {
        "ok": ok,
        "changed": changed,
        "expect": expect,
        "source": "urivql-mock",
    }
```

```python markpact:module path=urivql/routes.py
from __future__ import annotations

from importlib.resources import files

from uri_control.edge.manifest import register_manifest_file


def register(runtime):
    register_manifest_file(runtime, files(__package__).joinpath("manifest.yaml"))
```

```markdown markpact:docs
# urivql

urivql:// URI capability pack for urisys-node.

Licensed under Apache-2.0.
```

