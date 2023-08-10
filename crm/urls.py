#
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^contact_confirm_detail/$', views.contact_confirm_detail, name='contact confirm detail'),
]