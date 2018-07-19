# -*- coding:utf-8 -*-

"""thoughtserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from apscheduler.schedulers.background import BackgroundScheduler
from thought.cron import setWeight


#定时器
scheduler = BackgroundScheduler()
set_weight = setWeight

scheduler.add_job(set_weight, 'cron', hour =4 )  # 凌晨4点执行

try:
    scheduler.start()  # 这里的调度任务是独立的一个线程
except(KeyboardInterrupt, SystemExit):
    scheduler.shutdown()




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/',include('thought.urls')),
]
