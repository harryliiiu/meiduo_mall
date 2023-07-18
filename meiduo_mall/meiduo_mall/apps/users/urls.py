from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
urlpatterns = []

router.register(r'^users', views.UserView, basename='users')

urlpatterns += router.urls
