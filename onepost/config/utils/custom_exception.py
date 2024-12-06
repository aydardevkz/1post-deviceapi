import redis
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status

#  redis Sentinel 连接

def get_message_detail(message):
    if isinstance(message, dict):
        return message
    elif isinstance(message, list):
        return message[0]
    else:
        return message



def custom_exception_handler(exc, context):
    # 获取默认的 DRF 异常处理响应
    response = exception_handler(exc, context)

    # 检查是否是 APIException
    if isinstance(exc, APIException):
        # 如果异常处理响应不为空
        if response is not None:
            custom_response_data = {
                'status_code': response.status_code,
                'message':  get_message_detail(exc.detail),
                'message_code': exc.get_codes()  # 获取异常代码
            }
            return Response(custom_response_data, status=response.status_code)

    # 如果异常不是 APIException，返回默认的处理结果
    return response

