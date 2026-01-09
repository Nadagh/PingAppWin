from enum import Enum, auto


class PingResultStatus(Enum):
    """
    Канонический результат ping.

    Domain-level enum.
    Не зависит от stdout, локализации, UI или цветов.
    Описывает ФАКТИЧЕСКОЕ состояние сетевой доступности.
    """

    # --- Технические состояния ---
    PENDING = auto()            # Проверка в процессе
    ERROR = auto()              # Внутренняя ошибка / общий сбой

    # --- Валидация ---
    MISSING_ADDRESS = auto()    # IP / host не указан
    INVALID_ADDRESS = auto()    # Неверный IP / host

    # --- Сетевые результаты ---
    SUCCESS = auto()            # Хост стабильно отвечает
    TIMEOUT = auto()            # Нет ответа в пределах таймаута
    UNREACHABLE = auto()        # Ответил роутер: хост недоступен
    HOST_NOT_FOUND = auto()     # DNS не смог разрешить имя

    # --- Агрегированные состояния ---
    UNSTABLE = auto()           # Ответы есть, но присутствуют потери / таймауты
