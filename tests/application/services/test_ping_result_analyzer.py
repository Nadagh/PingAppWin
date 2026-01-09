# tests/application/services/test_ping_result_analyzer.py

import pytest

from domain.value_objects.ping_result_status import PingResultStatus
from application.services.ping_result_analyzer import analyze_ping_result


class TestPingResultAnalyzer:
    """
    Application-level tests.

    analyze_ping_result(stdout, exit_code) → PingResultStatus
    """

    # ======================================================
    # SUCCESS — EN / RU / WINDOWS LOCALIZED
    # ======================================================

    def test_success_when_reply_received_en(self):
        stdout = """
        Reply from 8.8.8.8: bytes=32 time=20ms TTL=117
        Reply from 8.8.8.8: bytes=32 time=21ms TTL=117
        """
        status = analyze_ping_result(stdout=stdout, exit_code=0)
        assert status == PingResultStatus.SUCCESS


    def test_success_when_reply_received_ru(self):
        stdout = """
        Ответ от 8.8.8.8: число байт=32 время=20мс TTL=117
        Ответ от 8.8.8.8: число байт=32 время=21мс TTL=117
        """
        status = analyze_ping_result(stdout=stdout, exit_code=0)
        assert status == PingResultStatus.SUCCESS


    def test_localhost_ru_windows_time_less_than_one_ms(self):
        """
        Канонический случай Windows RU:
        время<1мс
        """
        stdout = "Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128"
        status = analyze_ping_result(stdout=stdout, exit_code=1)

        assert status == PingResultStatus.SUCCESS


    def test_localhost_multiple_replies_ru(self):
        stdout = """
        Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
        Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
        Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
        Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
        """
        status = analyze_ping_result(stdout=stdout, exit_code=0)

        assert status == PingResultStatus.SUCCESS


    def test_success_even_if_exit_code_non_zero_when_reply_present(self):
        stdout = "Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128"
        status = analyze_ping_result(stdout=stdout, exit_code=2)

        assert status == PingResultStatus.SUCCESS


    # ======================================================
    # UNREACHABLE — ROUTER RESPONDED
    # ======================================================

    @pytest.mark.parametrize(
        "stdout",
        [
            "Reply from 192.168.0.1: Destination host unreachable.",
            "Ответ от 150.102.95.250: Заданный узел недоступен.",
            "destination host unreachable",
            "узел недоступен",
        ],
    )
    def test_unreachable_when_router_reports_no_route(self, stdout):
        status = analyze_ping_result(stdout=stdout, exit_code=1)
        assert status == PingResultStatus.UNREACHABLE


    def test_unreachable_has_priority_over_reply(self):
        stdout = """
        Ответ от 192.168.0.1: Заданный узел недоступен.
        Ответ от 192.168.0.1: число байт=32 время=1мс TTL=64
        """
        status = analyze_ping_result(stdout=stdout, exit_code=1)
        assert status == PingResultStatus.UNREACHABLE


    # ======================================================
    # TIMEOUT
    # ======================================================

    @pytest.mark.parametrize(
        "stdout",
        [
            "Request timed out.",
            "Превышен интервал ожидания для запроса.",
            "timeout waiting for icmp_seq",
        ],
    )
    def test_timeout_detected(self, stdout):
        status = analyze_ping_result(stdout=stdout, exit_code=1)
        assert status == PingResultStatus.TIMEOUT


    def test_timeout_has_priority_over_statistics(self):
        stdout = """
        Превышен интервал ожидания для запроса.
        Статистика Ping:
            Пакетов: отправлено = 1, получено = 0, потеряно = 1
        """
        status = analyze_ping_result(stdout=stdout, exit_code=1)
        assert status == PingResultStatus.TIMEOUT


    # ======================================================
    # HOST NOT FOUND — DNS
    # ======================================================

    @pytest.mark.parametrize(
        "stdout",
        [
            "Ping request could not find host google123.",
            "Не удается найти указанный узел.",
            "could not find host",
        ],
    )
    def test_host_not_found(self, stdout):
        status = analyze_ping_result(stdout=stdout, exit_code=2)
        assert status == PingResultStatus.HOST_NOT_FOUND


    # ======================================================
    # INVALID ADDRESS
    # ======================================================

    @pytest.mark.parametrize(
        "stdout",
        [
            "Invalid IP address.",
            "Неверный IP адрес",
        ],
    )
    def test_invalid_address_detected(self, stdout):
        status = analyze_ping_result(stdout=stdout, exit_code=2)
        assert status == PingResultStatus.INVALID_ADDRESS


    def test_invalid_address_has_priority_over_host_not_found(self):
        stdout = "Неверный IP адрес. Не удается найти указанный узел."
        status = analyze_ping_result(stdout=stdout, exit_code=2)

        assert status == PingResultStatus.INVALID_ADDRESS


    # ======================================================
    # ERROR — FALLBACK
    # ======================================================

    def test_empty_stdout_is_error(self):
        status = analyze_ping_result(stdout="", exit_code=1)
        assert status == PingResultStatus.ERROR


    def test_whitespace_stdout_is_error(self):
        status = analyze_ping_result(stdout="   \n   ", exit_code=1)
        assert status == PingResultStatus.ERROR


    def test_none_exit_code_is_error(self):
        stdout = "Ответ от 8.8.8.8: число байт=32 время=10мс TTL=117"
        status = analyze_ping_result(stdout=stdout, exit_code=None)

        assert status == PingResultStatus.ERROR


    def test_garbage_output_is_error(self):
        stdout = "какой-то мусор без маркеров"
        status = analyze_ping_result(stdout=stdout, exit_code=0)

        assert status == PingResultStatus.ERROR
