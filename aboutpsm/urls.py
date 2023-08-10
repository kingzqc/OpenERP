from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^load_appoints/$', views.load_appoints, name='load_appoints'),
    url(r'^load_opportunitys/$', views.load_opportunitys, name='load_opportunitys'),
]