from flask import jsonify
import time

def make_resp(code=200, msg="success", data=None):
    """
    统一响应格式
    :param code: 状态码
    :param msg: 响应消息
    :param data: 响应数据
    :return: JSON 响应对象
    """
    response = {
        "code": code,
        "msg": msg,
        "data": data,
        "timestamp": int(time.time()),
    }
    return jsonify(response), code


