ok_ip = [
        ("127.0.0.1", 1),
        ("127.0.0.2", 10),
        ("127.0.0.3", 102),
        ("127.0.0.4", 0)
        ]

error_ip = [
        ("150.102.95.100", 1),
        ("150.102.95.158", 3)
        ]

ok_batch_ip = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]
ok_batch_ip_result_int_list = [0, 0, 0, 0]
ok_batch_ip_result_bool_list = [True, True, True, True]
ok_batch_ip_result_int_dict = dict(zip(ok_batch_ip, ok_batch_ip_result_int_list))
ok_batch_ip_result_bool_dict = dict(zip(ok_batch_ip, ok_batch_ip_result_bool_list))

error_batch_ip = ["150.102.95.100", "150.102.95.158"]
error_batch_ip_result_int_list = [1, 1]
error_batch_ip_result_bool_list = [False, False]
error_batch_ip_result_int_dict = dict(zip(error_batch_ip, error_batch_ip_result_int_list))
error_batch_ip_result_bool_dict = dict(zip(error_batch_ip, error_batch_ip_result_bool_list))

batch_ip = ["127.0.0.1", "150.102.95.100", "150.102.95.158", "127.0.0.4"]
batch_ip_result_int_list = [0, 1, 1, 0]
batch_ip_result_bool_list = [True, False, False, True]
batch_ip_result_int_dict = dict(zip(batch_ip, batch_ip_result_int_list))
batch_ip_result_bool_dict = dict(zip(batch_ip, batch_ip_result_bool_list))
