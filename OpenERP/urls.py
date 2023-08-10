"""PSMProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
import base, doc
from base import views
from doc.views import SelectBaseCompetenceView
from django.conf.urls import url
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.base_login, name = 'login'),
    path('logout/', views.base_logout, name = 'logout'),
    path('register/', views.register, name = 'register'),
    path('resource/', views.resource, name = 'resource'),
    path('jobs/', views.jobs, name = 'jobs'),
    path('about/', views.about, name = 'about'),
    path('topicdetail/', views.topicdetail, name='topicdetail'),  # 关于single page
    path(r'agenda/', views.agenda, name='agenda'),  # 日程
    path(r'editagenda/', views.editagenda, name='editagenda'),  # 日程
    path(r'bookagenda/', views.bookagenda, name='bookagenda'),  # book日程
    path(r'cancelagenda/', views.cancelagenda, name='cancelagenda'),  # cancel日程
    re_path(r'^agenda/', views.agenda, name='agenda'),  # 日程
    re_path(r'^activeuser/<str:username>/',views.activeuser,name='user_active'),# 邮箱激活账号
    re_path(r'^myprofile/', views.myprofile, name='myprofile'),
    re_path(r'^editprofile/', views.editprofile, name='editprofile'),
    path('forgotpassword/',views.forgotpassword, name='forgot'), # 忘记密码
    path(r'activeuser/<str:username>/', views.activeuser, name='active'),
    path(r'myprofile/', views.myprofile, name='myprofile'),
    path(r'editprofile/', views.editprofile, name='editprofile'),
    path(r'select/resource_basecompetence/', SelectBaseCompetenceView.as_view(), name='resource_basecompetence'),
    path('modify_pwd/',views.modify_pwd,name='modify_pwd'),
    path('psm/', xadmin.site.urls),
    path('captcha/', include("captcha.urls")),
    path('base/', include("base.urls")),
    path('aboutpsm/', include("aboutpsm.urls")),
    path(r'resourcelist/', views.resource_list, name='resourcelist'),
    path(r'resourcedetailedit/', views.resource_detail_edit, name='resourcedetailedit'),
    re_path(r'resourcelist/', views.resource_list, name='resourcelist'),
    path(r'servicelist/', views.service_list, name='servicelist'),
    re_path(r'servicelist/', views.service_list, name='servicelist'),
    path(r'servicedetailedit/', views.service_detail_edit, name='servicedetailedit'),
    path(r'requestlist/', views.request_list, name='requestlist'),
    re_path(r'requestlist/', views.request_list, name='requestlist'),
    path(r'requestdetailedit/', views.request_detail_edit, name='requestdetailedit'),
    path(r'contactdetailedit/', views.contact_detail_edit, name='contactdetailedit'),
    path(r'customerdetailedit/', views.customer_detail_edit, name='customerdetailedit'),
    path(r'opportunitydetailedit/', views.opportunity_detail_edit, name='opportunitydetailedit'),
    path(r'resultlist/', views.result_list, name='resultlist'),
    re_path(r'resultlist/', views.result_list, name='resultlist'),
    path('viewfunnel/', views.view_funnel, name='viewfunnel'),
    path('love/', views.love, name='love'),
    path('lovepass/', views.lovepass, name='lovepass'),
    path('thumbup/', views.thumpup, name='thumbup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
