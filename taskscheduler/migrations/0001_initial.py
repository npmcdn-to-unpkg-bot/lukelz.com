# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 22:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar_name', models.CharField(max_length=50)),
                ('source_name', models.CharField(max_length=50)),
                ('user_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='SchedulableItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=150)),
                ('lon', models.FloatField(blank=True, default=41.829616)),
                ('lat', models.FloatField(blank=True, default=-71.401486)),
                ('priority', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('schedulableitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='taskscheduler.SchedulableItem')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskscheduler.Calendar')),
            ],
            bases=('taskscheduler.schedulableitem',),
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('schedulableitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='taskscheduler.SchedulableItem')),
                ('deadline', models.DateTimeField()),
            ],
            bases=('taskscheduler.schedulableitem',),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('schedulableitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='taskscheduler.SchedulableItem')),
                ('deadline', models.DateTimeField()),
                ('etc', models.DurationField()),
            ],
            bases=('taskscheduler.schedulableitem',),
        ),
    ]
