from __future__ import annotations

from importlib.resources import as_file

from uri_control import CapabilityRegistry

import urivql


def test_manifest_loads():
    with as_file(urivql.manifest_path()) as path:
        registry = CapabilityRegistry.from_manifest_files([path])
    assert registry.manifests[0].scheme == "vql"
    assert len(registry.routes) == 2
