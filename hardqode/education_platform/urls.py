from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'lessons', views.LessonViewSet, basename='lesson')
router.register(r'groups', views.GroupViewSet)
router.register(r'product-stats', views.ProductStatsViewSet)

app_name = 'education_platform'
urlpatterns = [
    path('', include(router.urls)),
]
