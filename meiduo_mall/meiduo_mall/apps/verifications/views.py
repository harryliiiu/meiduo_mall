from random import randint
from rest_framework.views import APIView
from django.shortcuts import render
from django_redis import get_redis_connection
from meiduo_mall.libs.yuntongxun.sms import CCP
from rest_framework.response import Response
import logging

logger = logging.getLogger('django')


class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 1.生成验证码
        sms_code = '%04d' % randint(0, 999)
        logger.info(sms_code)
        # 2.创建Redis连接对象
        redis_conn = get_redis_connection('verify_codes')
        # 3.把验证码存到数据库、
        redis_conn.setex('sms_%s' % mobile, 300, sms_code)
        # 4.利用容联云发送短信验证码、
        CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # 5.响应
        return Response({'message': 'ok'})
        pass

    def post(self, request):
        return Response(123)