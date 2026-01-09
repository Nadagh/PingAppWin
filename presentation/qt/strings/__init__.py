"""
UI string constants for presentation layer.

Назначение:
- Убрать магические строки из Qt-кода
- Централизовать UI-тексты
- Подготовить слой presentation к локализации

Ограничения:
- Используется ТОЛЬКО в presentation
- НЕ импортируется в application / domain
"""

# Common


from .common import (
    APP_TITLE,
    BTN_START,
    BTN_STOP,
    BTN_CLEAR,
    CHECKBOX_INFINITE,
    LABEL_STATUS,
    LABEL_ADDRESS,
    LABEL_COUNT,
    )

# Console tab
from .console_tab import (
    CONSOLE_TAB_TITLE,
    BTN_CLEAR_OUTPUT,
    PLACEHOLDER_NO_OUTPUT,
    )

# Ping tab
from .ping_tab import (
    PING_TAB_TITLE,
    BTN_ADD_ROW,
    BTN_REMOVE_ROW,
    STATUS_PENDING,
    STATUS_IDLE,
    )

# Scan tab
from .scan_tab import (
    SCAN_TAB_TITLE,
    BTN_SCAN_START,
    SCAN_INPUT_PLACEHOLDER,
    BTN_SCAN_STOP,
    BTN_ADAPTERS,
    LABEL_PROGRESS_INITIAL,
    TABLE_SUCCESS_TITLE,
    TABLE_FAIL_TITLE,
    LABEL_MAX_PARALLEL,
    )

# Tables
from .table_headers import (
    PING_TABLE_HEADERS,
    )


__all__ = [
        # common
        "APP_TITLE",
        "BTN_START",
        "BTN_STOP",
        "BTN_CLEAR",
        "CHECKBOX_INFINITE",
        "LABEL_STATUS",
        "LABEL_ADDRESS",
        "LABEL_COUNT",

        # ping tab
        "PING_TAB_TITLE",
        "BTN_ADD_ROW",
        "BTN_REMOVE_ROW",
        "STATUS_PENDING",
        "STATUS_IDLE",

        # console tab
        "CONSOLE_TAB_TITLE",
        "BTN_CLEAR_OUTPUT",
        "PLACEHOLDER_NO_OUTPUT",

        # scan tab
        "SCAN_TAB_TITLE",
        "SCAN_INPUT_PLACEHOLDER",
        "BTN_SCAN_START",
        "BTN_SCAN_STOP",
        "BTN_ADAPTERS",
        "LABEL_PROGRESS_INITIAL",
        "TABLE_SUCCESS_TITLE",
        "TABLE_FAIL_TITLE",
        "LABEL_MAX_PARALLEL",

        # tables
        "PING_TABLE_HEADERS",
        ]
