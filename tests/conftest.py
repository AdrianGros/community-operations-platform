from __future__ import annotations

import os
from pathlib import Path

import pytest

from app.bootstrap import create_app_context

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("XDG_RUNTIME_DIR", "/tmp")


@pytest.fixture()
def app_context(tmp_path: Path):
    context, conn = create_app_context(base_dir=tmp_path)
    try:
        yield context
    finally:
        conn.close()
