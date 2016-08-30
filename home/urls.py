from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^resume$', views.resume, name='resume'),
    url(r'^projects$', views.projects, name='projects'),
]