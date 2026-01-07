from enum import Enum, auto


class ConsoleLineType(Enum):
    """
    Тип строки вывода консоли.

    Используется для классификации строк ping
    без привязки к UI или цветам.
    """

    INFO = auto()       # обычная информация
    SUCCESS = auto()    # успешный ответ (ttl, reply)
    WARNING = auto()    # предупреждения
    ERROR = auto()      # ошибки (timeout, invalid host)
    SYSTEM = auto()     # системные сообщения (запуск, режим)
