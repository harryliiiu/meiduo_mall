from random import randint
from rest_framework.views import APIView
from django_redis import get_redis_connection
from meiduo_mall.libs.yuntongxun.sms import CCP
from rest_framework.response import Response
from rest_framework import status
import logging
from . import constants

logger = logging.getLogger('django')


class SMSCodeView(APIView):
    """短信验证码"""

    def get(self, request, mobile):
        # 1.生成验证码
        sms_code = '%04d' % randint(0, 999)
        logger.info(sms_code)
        # 2.创建Redis连接对象
        redis_conn = get_redis_connection('verify_codes')

        # 判断60秒内是否发送过短信
        send_flag = pl.get('send_flag_ %s' % mobile)

        # 创建Redis管道
        pl = redis_conn.pipeline()
        if send_flag:
            return Response({'message': '手机频繁发送短信验证码'}, status=status.HTTP_400_BAD_REQUEST)
        # 3.把验证码存到数据库、
        pl.setex('sms_%s' % mobile, constants.SEND_CODE_REDIS_EXPIRES, sms_code)
        # 存储一个标识表示60秒内已经发过短信
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 执行管道
        pl.execute()
        # 4.利用容联云发送短信验证码、
        flag = CCP().send_template_sms(mobile, [sms_code, constants.SEND_CODE_REDIS_EXPIRES // 60], 1)
        # 5.响应
        if flag == 0:
            return Response({'message': 'ok'})
        return Response({'message': '接收短信失败，请重试。'})

