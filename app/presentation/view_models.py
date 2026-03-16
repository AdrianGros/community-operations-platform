from __future__ import annotations

from typing import Any

from PySide6 import QtCore
from PySide6.QtGui import QColor


class CaseTableModel(QtCore.QAbstractTableModel):
    HEADERS = ("Title", "Risk", "Finding", "Measure", "Owner", "Updated")

    def __init__(self) -> None:
        super().__init__()
        self._items: list[dict[str, Any]] = []

    def update_items(self, items: list[dict[str, Any]]) -> None:
        self.beginResetModel()
        self._items = items
        self.endResetModel()

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._items)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.HEADERS)

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None
        item = self._items[index.row()]
        keys = ("title", "risk_level", "finding_status", "measure_status", "measure_owner_name", "updated_at")
        if role == QtCore.Qt.DisplayRole:
            key = keys[index.column()]
            return item.get(key, "-")
        if role == QtCore.Qt.ForegroundRole:
            key = keys[index.column()]
            value = str(item.get(key, ""))
            if key == "risk_level":
                return {
                    "High": QColor("#9f2d2d"),
                    "Medium": QColor("#9a5a00"),
                    "Low": QColor("#25683c"),
                }.get(value)
            if key == "finding_status":
                return {
                    "Identified": QColor("#8a4b00"),
                    "In Progress": QColor("#1f5f99"),
                    "Mitigated": QColor("#25683c"),
                    "Accepted": QColor("#7b4bb3"),
                    "Closed": QColor("#5d7185"),
                }.get(value)
            if key == "measure_status":
                return {
                    "Planned": QColor("#8a4b00"),
                    "In Progress": QColor("#1f5f99"),
                    "Completed": QColor("#25683c"),
                    "Accepted": QColor("#7b4bb3"),
                }.get(value)
        if role == QtCore.Qt.FontRole:
            key = keys[index.column()]
            if key in {"risk_level", "finding_status", "measure_status"}:
                font = super().data(index, role)
                if font is None:
                    from PySide6.QtGui import QFont
                    font = QFont()
                font.setBold(True)
                return font
        if role == QtCore.Qt.TextAlignmentRole:
            key = keys[index.column()]
            if key in {"risk_level", "finding_status", "measure_status", "updated_at"}:
                return int(QtCore.Qt.AlignCenter)
        if role == QtCore.Qt.UserRole:
            return item
        return None

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole) -> Any:
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.HEADERS[section]
        return super().headerData(section, orientation, role)


class AuditTableModel(QtCore.QAbstractTableModel):
    HEADERS = ("Time", "Severity", "Actor", "Action", "Entity")

    def __init__(self) -> None:
        super().__init__()
        self._items: list[dict[str, Any]] = []

    def update_items(self, items: list[dict[str, Any]]) -> None:
        self.beginResetModel()
        self._items = items
        self.endResetModel()

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._items)

    def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.HEADERS)

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None
        item = self._items[index.row()]
        keys = ("occurred_at", "severity", "actor_name", "action", "entity_label")
        if role == QtCore.Qt.DisplayRole:
            key = keys[index.column()]
            return item.get(key, "-")
        if role == QtCore.Qt.ForegroundRole and keys[index.column()] == "severity":
            return {
                "INFO": QColor("#1f5f99"),
                "WARNING": QColor("#9a5a00"),
                "ERROR": QColor("#9f2d2d"),
            }.get(str(item.get("severity", "")).upper())
        if role == QtCore.Qt.FontRole and keys[index.column()] == "severity":
            from PySide6.QtGui import QFont
            font = QFont()
            font.setBold(True)
            return font
        if role == QtCore.Qt.UserRole:
            return item
        return None

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole) -> Any:
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.HEADERS[section]
        return super().headerData(section, orientation, role)
