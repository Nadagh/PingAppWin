import pytest

from application.services.ping_result_analyzer import analyze_ping_result
from domain.value_objects.ping_result_status import PingResultStatus


class TestPingResultAnalyzerUnstable:
    """
    Нестабильные соединения:
    есть ответы, но присутствуют ошибки / таймауты.
    """

    def test_unstable_when_unreachable_and_reply_mixed(self):
        stdout = """
        Ответ от 150.102.95.250: Заданный узел недоступен.
        Ответ от 150.102.95.250: число байт=32 время<1мс TTL=128
        Ответ от 150.102.95.250: число байт=32 время<1мс TTL=128
        Ответ от 150.102.95.250: число байт=32 время<1мс TTL=128
        Ответ от 150.102.95.250: Заданный узел недоступен.
        Ответ от 150.102.95.250: Заданный узел недоступен.
        """

        status = analyze_ping_result(stdout=stdout, exit_code=1)

        assert status == PingResultStatus.UNSTABLE


    def test_unstable_when_timeout_and_reply_mixed(self):
        stdout = """
        Превышен интервал ожидания для запроса.
        Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
        Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
        Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
        Превышен интервал ожидания для запроса.
        Превышен интервал ожидания для запроса.
        """

        status = analyze_ping_result(stdout=stdout, exit_code=1)

        assert status == PingResultStatus.UNSTABLE


    def test_unstable_when_general_failure_and_reply_mixed(self):
        stdout = """
        PING: сбой передачи. Общий сбой.
        Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
        Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
        """

        status = analyze_ping_result(stdout=stdout, exit_code=1)

        assert status == PingResultStatus.UNSTABLE


    def test_success_when_only_replies(self):
        stdout = """
        Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
        Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
        """

        status = analyze_ping_result(stdout=stdout, exit_code=0)

        assert status == PingResultStatus.SUCCESS


    def test_unreachable_when_only_unreachable(self):
        stdout = """
        Ответ от 150.102.95.250: Заданный узел недоступен.
        Ответ от 150.102.95.250: Заданный узел недоступен.
        """

        status = analyze_ping_result(stdout=stdout, exit_code=1)

        assert status == PingResultStatus.UNREACHABLE


    def test_timeout_when_only_timeouts(self):
        stdout = """
        Превышен интервал ожидания для запроса.
        Превышен интервал ожидания для запроса.
        """

        status = analyze_ping_result(stdout=stdout, exit_code=1)

        assert status == PingResultStatus.TIMEOUT
