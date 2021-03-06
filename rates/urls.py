from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/rates', views.RateView)

urlpatterns = [
    path('', views.home, name="home"),
    path('', include(router.urls)),
]
