from __future__ import annotations

from typing import Any

from PySide6 import QtCore


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
        if role == QtCore.Qt.DisplayRole:
            key = ("title", "risk_level", "finding_status", "measure_status", "measure_owner_name", "updated_at")[index.column()]
            return item.get(key, "-")
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
        if role == QtCore.Qt.DisplayRole:
            key = ("occurred_at", "severity", "actor_name", "action", "entity_label")[index.column()]
            return item.get(key, "-")
        if role == QtCore.Qt.UserRole:
            return item
        return None

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole) -> Any:
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.HEADERS[section]
        return super().headerData(section, orientation, role)
