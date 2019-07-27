"""SmartCare URL Configuration

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
from django.contrib import admin
from smartsite import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.index),
    path('index.html', views.index),
    path('admin/', admin.site.urls),
    path('alarms.html', views.alarm_statics),
    re_path(r'mme_report_HZMME\d+BNK.html', views.unit_statics),
    re_path(r'alarms_report_HZMME\d+BNK.html', views.alarm_statics),
    re_path(r'alarmhist_report_HZMME\d+BNK.html', views.alarmhist_stat)
]
