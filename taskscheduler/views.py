from django.shortcuts import render

from rest_framework import viewsets

from .serializers import ReminderSerializer, TaskSerializer, EventSerializer, CalendarSerializer
from .models import Reminder, Task, Event, Calendar

# Create your views here.
def calendar(request):
    return render(request, 'taskscheduler/calendar.html')

class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer