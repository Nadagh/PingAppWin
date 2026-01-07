from PySide6.QtGui import QTextCharFormat, QColor

from application.services import ConsoleLineType


def map_console_line(line_type: ConsoleLineType) -> QTextCharFormat:
    fmt = QTextCharFormat()

    if line_type == ConsoleLineType.SUCCESS:
        fmt.setForeground(QColor("#00ff00"))  # зелёный

    elif line_type == ConsoleLineType.ERROR:
        fmt.setForeground(QColor("#f44747"))  # красный

    elif line_type == ConsoleLineType.WARNING:
        fmt.setForeground(QColor("#ffcc00"))  # жёлтый

    elif line_type == ConsoleLineType.SYSTEM:
        fmt.setForeground(QColor("#569cd6"))  # синий

    else:  # INFO
        fmt.setForeground(QColor("#d4d4d4"))  # стандарт

    return fmt
