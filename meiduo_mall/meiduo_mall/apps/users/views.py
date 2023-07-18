from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateUserSerializer
from .models import User


class UserView(ModelViewSet):
    """用户注册"""
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    # def post(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
