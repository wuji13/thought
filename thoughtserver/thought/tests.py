# -*- coding:utf-8 -*-
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
import json
from django.http import HttpResponse
from .models import Developer,User,Thought,DiscussTwo,SupportThought,SupportDisone,DiscussOne
from .views import Verify
# Create your tests here.


def Create_user_test(request):
    print('Create_user')
    try:
        if request.method == 'POST':
            _wxid = request.POST.get('wxid')
            _photoUrl = request.POST.get('photoUrl')
            _name = request.POST.get('name')
            print('数据', _wxid, _photoUrl, _name)
            try:
                u = User.objects.get(wxId=_wxid)
                u.name = _name
                u.photoUrl = _photoUrl
                u.save()
                lis = {'data': '', 'errorCode': 102, 'flag': 'success', 'msg': 'user already exist '}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            except ObjectDoesNotExist:
                print('meiren',_wxid,_photoUrl,_name)

                user = User(wxId=_wxid, photoUrl=_photoUrl, name=_name)
                user.save()
                lis = {'data': '', 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                json_str = json.dumps(lis)
                print(lis)
                return HttpResponse(json_str)

        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        json_str = json.dumps(lis)
        return HttpResponse(json_str)
