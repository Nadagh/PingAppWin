from application.services.ping_result_analyzer import analyze_ping_result
from domain.value_objects.ping_result_status import PingResultStatus


def test_windows_russian_ping_success_detected():
    stdout = """
Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128
Ответ от 127.0.0.1: число байт=32 время<1мс TTL=128

Статистика Ping для 127.0.0.1:
    Пакетов: отправлено = 2, получено = 2, потеряно = 0
    (0% потерь)
"""

    status = analyze_ping_result(stdout, exit_code=0)

    assert status == PingResultStatus.SUCCESS
