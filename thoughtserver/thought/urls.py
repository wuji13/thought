from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^getopenid', views.Get_openid, name='getopenid'),
    url(r'^createuser', views.Create_user, name='createuser'),
    url(r'^write', views.Write, name='write'),
    url(r'^getthought', views.Get_thought, name='getthought'),
    url(r'^supportthought', views.Support_thought, name='supportthought'),
]