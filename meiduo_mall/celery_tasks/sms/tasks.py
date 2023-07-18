# 编写异步任务代码
from celery_tasks.sms import constants
from celery_tasks.sms.yuntongxun.sms import CCP
from celery_tasks.main import celery_app


@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """发送短信的异步celery任务
    mobile :手机号
    sms_code:验证码
    """
    CCP().send_template_sms(mobile, [sms_code, constants.SEND_CODE_REDIS_EXPIRES // 60], 1)