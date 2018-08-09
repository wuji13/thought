from django.conf.urls import url
from . import views,tests

urlpatterns = [
    url(r'^getopenid', views.Get_openid, name='getopenid'),
    url(r'^createuser', views.Create_user, name='createuser'),
    url(r'^write', views.Write, name='write'),
    url(r'^getthought', views.Get_thought, name='getthought'),
    url(r'^supportthought', views.Support_thought, name='supportthought'),
    url(r'^discussone', views.Discuss_one, name='discussone'),
    url(r'^getuserimg', views.Get_user_img, name='getuserimg'),
    url(r'^orsupport', views.Or_support, name='orsupport'),
    url(r'^getdiscussone', views.Get_discussone, name='getdiscussone'),
    url(r'^supportdisone', views.Support_disone, name='supportdisone'),
    url(r'^discusstwo', views.Discuss_two, name='discusstwo'),
    url(r'^getdiscusstwo', views.Get_discusstwo, name='getdiscusstwo'),
    url(r'^getmythought', views.Get_mythought, name='getmythought'),
    url(r'^getmydis', views.Get_mydis, name='getmydis'),
    url(r'^getmyreply', views.Get_myReply, name='getmyreply'),
    url(r'^test', tests.Create_user_test, name='test'),
    url(r'^getShow', tests.Get_show, name='getShow'),
]