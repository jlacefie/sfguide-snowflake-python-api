import functools, time, re

from flask import jsonify, make_response


def phone_params_valid(phone):
    if re.search("^[0-9]{2}-[0-9]{3}-[0-9]{3}-[0-9]{4}$", phone):
        return True
    return False

def okey_params_valid(okey):
    if re.search("^\d+$", okey):
        return True
    return False

def api_response(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time        
        response = dict(result=result, time_ms=int(run_time*1000))
        value = make_response(jsonify(response))
        value.headers['Access-Control-Allow-Origin'] = '*'
        return value
    return f
