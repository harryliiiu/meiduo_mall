from rest_framework import serializers
from .models import User
import re
from django_redis import get_redis_connection


class CreateUserSerializer(serializers.ModelSerializer):
    # 序列化器的所有字段: ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 需要校验的字段: ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 模型中已存在的字段: ['id', 'username', 'password', 'mobile']

    # 需要序列化的字段: ['id', 'username', 'mobile', 'token']
    # 需要反序列化的字段: ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow', 'email']
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {  # 自定义校验出错后的错误信息提示
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, value):
        """单独校验手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号有误')
        return value

    def validate_allow(self, value):
        if value != 'true':
            raise serializers.ValidationError('请同意协议')
        return value

    def validate(self, attrs):
        """校验两个密码是否相同"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两个密码不一致')

        # 校验验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        # redis 中以字符串存储
        if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('验证码错误')
        return attrs

    def create(self, validated_data):
        # 把不需要存储的字段从字典中移除
        del validated_data['password2']
        del validated_data['allow']
        del validated_data['sms_code']

        # 把密码先取出去
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password) # 把密码加密后再赋值给user的password属性
        user.save()
        return user