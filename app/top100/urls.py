from django.urls import path, include
from rest_framework.routers import DefaultRouter
from top100 import views

router = DefaultRouter()
router.register('players', views.PlayerViewSet)
app_name = 'top100'

urlpatterns = [
    path('', include(router.urls))
]
