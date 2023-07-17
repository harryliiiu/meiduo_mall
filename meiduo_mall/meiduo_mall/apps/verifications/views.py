from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


class SMSCodeView(APIView):
    """短信验证码"""
    def get_code(self, request, mobile):
        # 1.生成验证码
        # 2.创建Redis连接对象
        # 3.把验证码存到数据库
        # 4.利用容联云发送短信验证码
        # 5.响应

        pass
