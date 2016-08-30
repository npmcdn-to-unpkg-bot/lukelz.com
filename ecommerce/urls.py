from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<item_id>[0-9]+)/$', views.detail, name='detail'),
]