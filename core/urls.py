from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CourseViewSet, TimetableViewSet, SessionViewSet,
    start_session
)

# Create router and register viewsets
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('courses', CourseViewSet, basename='course')
router.register('timetables', TimetableViewSet, basename='timetable')
router.register('sessions', SessionViewSet, basename='session')

# Export urlpatterns
urlpatterns = router.urls + [
    path('start-session/', start_session, name='start-session'),
]

