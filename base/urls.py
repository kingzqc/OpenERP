from django.conf.urls import url
from django.urls import path, re_path
from . import views

urlpatterns = [
    url(r'^make_bu_enable/$', views.make_bu_enable, name='bu_enable'),
    path('index/', views.index, name='index'), # 首页
    path('login/', views.base_login, name='login'), # 登录
    path('logout/', views.base_logout, name='logout'), # 退出
    path('register/', views.register, name='register'),  # 注册
    path('forgotpassword/', views.forgotpassword, name='forgot'),  # 忘记密码
    path(r'activeuser/', views.activeuser, name='active'),
    path(r'myprofile/', views.myprofile, name='myprofile'),
    path('resource/', views.resource, name='resource'),  # 讲师
    path('jobs/', views.jobs, name='jobs'),  # 课程
    path('about/', views.about, name='about'),  # 关于我们
    path('topicdetail/', views.topicdetail, name='topicdetail'),  # 关于topic page
    path(r'agenda/', views.agenda, name='agenda'),  # 日程
    path(r'editagenda/', views.editagenda, name='editagenda'),  # book日程
    path(r'bookagenda/', views.bookagenda, name='bookagenda'),  # book日程
    path(r'cancelagenda/', views.cancelagenda, name='cancelagenda'),  # cancel日程
    path('modify_pwd/',views.modify_pwd,name='modify_pwd'),
    re_path(r'agenda/', views.agenda, name='agenda'),  # 日程
    re_path(r'^activeuser/', views.activeuser, name='user_active'),  # 邮箱激活账号
    re_path(r'^myprofile/', views.myprofile, name='myprofile'),
]