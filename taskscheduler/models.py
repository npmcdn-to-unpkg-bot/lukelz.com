from django.db import models

# Pretty much a reminder, except I do not want inheritance
class SchedulableItem(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True) # Not required

    # Location of event in longitude and lattitude
    lon = models.FloatField(default= 41.829616, blank=True) # Not required
    lat = models.FloatField(default=-71.401486, blank=True) # Not required

    priority = models.IntegerField()

    scheduled = False

    def __str__(self):
        return self.title

class Reminder(SchedulableItem):
    deadline = models.DateTimeField()

# Tasks are longer and should have an ETC. 
class Task(SchedulableItem):
    # Estimated time to completion in seconds (a time interval object)
    deadline = models.DateTimeField()
    etc = models.DurationField()

# Events are scheduled on a calendar and can be rescheduled.
class Event(SchedulableItem):
    start = models.DateTimeField()
    end = models.DateTimeField()

    calendar = models.ForeignKey('Calendar', on_delete=models.CASCADE)

    scheduled = True

# Calendars hold lists of event objects. Reminders and tasks are scheduled onto calendars.
class Calendar(models.Model):
    calendar_name = models.CharField(max_length=50)
    source_name = models.CharField(max_length=50)
    user_email = models.EmailField()

    def __str__(self):
        return self.calendar_name