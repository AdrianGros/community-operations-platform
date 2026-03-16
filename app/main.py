from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

from PySide6 import QtWidgets

from app.bootstrap import BootstrapError, create_app_context
from app.presentation.main_window import MainWindow

log = logging.getLogger(__name__)


def main() -> int:
    runtime_cache = Path(__file__).resolve().parent.parent / "var" / "cache"
    runtime_cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("XDG_CACHE_HOME", str(runtime_cache))
    qt_app = QtWidgets.QApplication(sys.argv)
    qt_app.setApplicationName("Governance-Demo-App")
    qt_app.setOrganizationName("CommunityOperationsPlatform")
    try:
        app_context, conn = create_app_context()
    except BootstrapError as exc:
        log.exception("Application startup failed")
        QtWidgets.QMessageBox.critical(
            None,
            "Governance-Demo-App",
            f"Start fehlgeschlagen.\n\n{exc}\n\nPruefe die lokale Logdatei im Ordner var fuer Details.",
        )
        return 1
    window = MainWindow(app_context)
    window.show()
    try:
        return qt_app.exec()
    finally:
        conn.close()
        log.info("Application shutdown complete")


if __name__ == "__main__":
    raise SystemExit(main())
