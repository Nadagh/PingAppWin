import pytest

import adresses
from Tools import ping_tools


def test_ping_to_int_no_arg_ok():
    assert ping_tools.ping_to_int("127.0.0.1") == 0


def test_ping_to_bool_no_arg_ok():
    assert ping_tools.ping_to_bool("127.0.0.1") is True


def test_ping_to_int_no_arg_error():
    assert ping_tools.ping_to_int("150.102.95.100") == 1


def test_ping_to_bool_no_arg_error():
    assert ping_tools.ping_to_bool("150.102.95.100") is False


@pytest.mark.parametrize("ip,num", adresses.ok_ip)
def test_ping_to_int_ok(ip, num):
    assert ping_tools.ping_to_int(ip, num) == 0


@pytest.mark.parametrize("ip,num", adresses.error_ip)
def test_ping_to_int_error(ip, num):
    assert ping_tools.ping_to_int(ip, num) == 1


@pytest.mark.parametrize("ip,num", adresses.ok_ip)
def test_ping_to_bool_ok(ip, num):
    assert ping_tools.ping_to_bool(ip, num) is True


@pytest.mark.parametrize("ip,num", adresses.error_ip)
def test_ping_to_bool_error(ip, num):
    assert ping_tools.ping_to_bool(ip, num) is False


def test_batch_ping_to_int_list_ok():
    assert ping_tools.batch_ping_to_int_list(adresses.ok_batch_ip) == adresses.ok_batch_ip_result_int_list


def test_batch_ping_to_bool_list_ok():
    assert ping_tools.batch_ping_to_bool_list(adresses.ok_batch_ip) == adresses.ok_batch_ip_result_bool_list


def test_batch_ping_to_int_list_error():
    assert ping_tools.batch_ping_to_int_list(adresses.error_batch_ip) == adresses.error_batch_ip_result_int_list


def test_batch_ping_to_bool_list_error():
    assert ping_tools.batch_ping_to_bool_list(adresses.error_batch_ip) == adresses.error_batch_ip_result_bool_list


def test_batch_ping_to_int_list():
    assert ping_tools.batch_ping_to_int_list(adresses.batch_ip) == adresses.batch_ip_result_int_list


def test_batch_ping_to_bool_list():
    assert ping_tools.batch_ping_to_bool_list(adresses.batch_ip) == adresses.batch_ip_result_bool_list


def test_batch_ping_to_int_dict_ok():
    assert ping_tools.batch_ping_to_int_dict(adresses.ok_batch_ip) == adresses.ok_batch_ip_result_int_dict


def test_batch_ping_to_bool_dict_ok():
    assert ping_tools.batch_ping_to_bool_dict(adresses.ok_batch_ip) == adresses.ok_batch_ip_result_bool_dict


def test_batch_ping_to_int_dict_error():
    assert ping_tools.batch_ping_to_int_dict(adresses.error_batch_ip) == adresses.error_batch_ip_result_int_dict


def test_batch_ping_to_bool_dict_error():
    assert ping_tools.batch_ping_to_bool_dict(adresses.error_batch_ip) == adresses.error_batch_ip_result_bool_dict


def test_batch_ping_to_int_dict():
    assert ping_tools.batch_ping_to_int_dict(adresses.batch_ip) == adresses.batch_ip_result_int_dict


def test_batch_ping_to_bool_dict():
    assert ping_tools.batch_ping_to_bool_dict(adresses.batch_ip) == adresses.batch_ip_result_bool_dict
