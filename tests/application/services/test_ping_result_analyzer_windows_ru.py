import pytest

from application.services.ping_result_analyzer import analyze_ping_result
from domain.value_objects.ping_result_status import PingResultStatus


class TestPingResultAnalyzerWindowsRU:
    """
    Windows RU локализация.
    Проверяем, что разные системные сообщения
    НЕ схлопываются в один статус.
    """

    def test_windows_ru_unreachable(self):
        stdout = "Ответ от 150.102.95.250: Заданный узел недоступен."
        status = analyze_ping_result(stdout=stdout, exit_code=1)

        assert status == PingResultStatus.UNREACHABLE

    def test_windows_ru_timeout(self):
        stdout = "Превышен интервал ожидания для запроса."
        status = analyze_ping_result(stdout=stdout, exit_code=1)

        assert status == PingResultStatus.TIMEOUT

    def test_windows_ru_general_failure_is_error(self):
        stdout = "PING: сбой передачи. Общий сбой."
        status = analyze_ping_result(stdout=stdout, exit_code=1)

        assert status == PingResultStatus.ERROR

    def test_general_failure_has_priority_over_timeout_words(self):
        """
        Иногда 'сбой' может сопровождаться другими словами.
        Это НЕ timeout.
        """
        stdout = "PING: сбой передачи. Общий сбой. timeout"
        status = analyze_ping_result(stdout=stdout, exit_code=1)

        assert status == PingResultStatus.ERROR
