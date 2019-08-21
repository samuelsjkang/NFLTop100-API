from django.urls import path, include
from rest_framework.routers import DefaultRouter
from top100 import views

router = DefaultRouter()
router.register('players', views.PlayerViewSet)
router.register('teams', views.TeamViewSet)
router.register('positions', views.PositionViewSet)
app_name = 'top100'

urlpatterns = [
    path('', include(router.urls))
]
