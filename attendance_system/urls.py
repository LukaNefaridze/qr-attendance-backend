from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import UserViewSet, CourseViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('courses', CourseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
