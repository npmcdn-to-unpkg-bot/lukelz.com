from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'^api/reminders', views.ReminderViewSet)
router.register(r'^api/tasks', views.TaskViewSet)
router.register(r'^api/events', views.EventViewSet)
router.register(r'^api/calendars', views.CalendarViewSet)

urlpatterns = [
    url(r'$', views.calendar, name="calendar"),
]

urlpatterns += router.urls

