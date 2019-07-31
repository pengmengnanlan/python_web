"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

import pymysql
from django.conf.urls import url
from django.urls import path
from django.urls import include, re_path
from django.contrib import admin 
from . import view, Api

db = pymysql.connect(host='localhost', user='root',
                     password='123456', db='download_info', charset='utf8')

urlpatterns = [re_path(r'^$', view.login, name='index'),
               re_path(r'^login/$', view.login, name='login'),
               re_path(r'^logout/$', view.logout, name='logout'),
               re_path(r'^admin_user/$', view.admin_user, {'page':'admin_user.html'}, name='admin_user'),
               re_path(r'^admin_group/$', view.admin_group, {'page':'admin_group.html'}, name='admin_group'),
               re_path(r'^administrator/$', view.administrator, {'page':'administrator.html'}, name='administrator'),
               re_path(r'^extract_file.html/$', view.extract_file,name='extract_file'),
               re_path(r'^check_file.html/$', view.check_file,name='check_file'),]
               

