# -*- coding:utf-8 -*-


from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
import requests
import json
import datetime,time
from datetime import timedelta
from django.http import HttpResponse
from .models import Developer,User,Thought,DiscussTwo,SupportThought,SupportDisone,DiscussOne
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from itertools import chain
# Create your views here.


#一个简单的认证函数,通过时间和秘钥加密和解密，这是一个解密的过程
def Verify(ciphertext,ti,key):
    t = time.time()*1000
    if ti - t > -10000:
        _developer = Developer.objects.get(key=key)
        sum = 0
        for i in _developer.secret:
            num = ord(i)
            sum = sum + num
        if sum + ti == ciphertext :
            return True
        else:
            return False
    else:
        return False

def Get_openid(request):
    print('Get_openid')
    try:
        if request.method == 'GET':
            code = request.GET.get('code')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')

            if Verify(_ciphertext, _time,_key):
                r = requests.get(
                    'https://api.weixin.qq.com/sns/jscode2session?appid=wx86e64720c0387b9f&secret=7965220b0c99aeb7132b293cc6122c4d&js_code=' + code + '&grant_type=authorization_code')
                code = json.loads(r.text)
                lis = {'data': code, 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        json_str = json.dumps(lis)
        return HttpResponse(json_str)

# 创建用户id_wx
def Create_user(request):
    print('Create_user')
    try:
        if request.method == 'POST':
            _wxid = request.POST.get('wxid')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('time'))
            _key = request.POST.get('key')
            _photoUrl = request.POST.get('photoUrl')
            _name = request.POST.get('name')
            if Verify(_ciphertext, _time,_key):
                try:
                    u = User.objects.get(wxId=_wxid)
                    u.name = _name
                    u.photoUrl = _photoUrl
                    u.save()
                    lis = {'data': '', 'errorCode': 102, 'flag': 'success', 'msg': 'user already exist '}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                except ObjectDoesNotExist:
                    print('meiren')
                    user = User(wxId=_wxid, photoUrl=_photoUrl, name=_name)
                    user.save()
                    lis = {'data': '', 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        json_str = json.dumps(lis)
        return HttpResponse(json_str)


#发表想法
def Write(request):
    print('Write')
    try:
        if request.method == 'POST':
            _wxid = request.POST.get('wxid')
            _content = request.POST.get('content')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('time'))
            _key = request.POST.get('key')
            print(_wxid,_content)
            user = User.objects.get(wxId=_wxid)
            if Verify(_ciphertext, _time,_key):
                if Thought.objects.filter(content=_content).filter(userId=user):
                    print(Thought.objects.filter(content=_content).filter(userId=user))
                    lis = {'data': '', 'errorCode': 102, 'flag': 'success', 'msg': 'thought already exist '}
                    json_str = json.dumps(lis)

                    return HttpResponse(json_str)
                else:
                    _duration = round(time.time())
                    thought = Thought(userId = user,content=_content,duration=_duration,auther=user.name)
                    thought.save()
                    lis = {'data': '', 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        json_str = json.dumps(lis)
        return HttpResponse(json_str)

#一级评论想法
def Discuss_one(request):
    print('Discuss_one')
    try:
        if request.method == 'POST':
            _wxid = request.POST.get('wxid')
            _content = request.POST.get('content')
            _thoughtId = request.POST.get('thoughtId')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('time'))
            _key = request.POST.get('key')
            if Verify(_ciphertext, _time,_key):
                print(_content,_thoughtId)
                user = User.objects.get(wxId = _wxid)
                thought = Thought.objects.get(pk=_thoughtId)
                print(user.name, thought)
                dis_one = DiscussOne(thoughtId=thought,userId=user,content=_content,auther=user.name)
                print(' _thoughtId')
                dis_one.save()
                thought.discussNum = thought.discussNum + 1
                thought.save()
                lis = {'data': '', 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                print(lis)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        json_str = json.dumps(lis)
        return HttpResponse(json_str)



#二级评论想法
def Discuss_two(request):
    print("Discuss_two")
    try:
        if request.method == 'POST':
            _wxid = request.POST.get('wxid')
            _content = request.POST.get('content')
            _discussOneId = request.POST.get('disOneId')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('time'))
            _key = request.POST.get('key')
            if Verify(_ciphertext, _time,_key):
                user = User.objects.get(wxId = _wxid)
                discussOne = DiscussOne.objects.get(pk=_discussOneId)

                dis_two = DiscussTwo(discussoneId=discussOne,userId=user,content=_content,auther=user.name)

                dis_two.save()
                discussOne.discussNum = discussOne.discussNum + 1
                discussOne.save()
                lis = {'data': '', 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        json_str = json.dumps(lis)
        return HttpResponse(json_str)



#一级点赞/取消点赞
def Support_thought(request):
    print('Support_thought')
    try:
        if request.method == 'POST':
            _wxid = request.POST.get('wxid')
            _thoughtId = request.POST.get('thoughtId')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('time'))
            _key = request.POST.get('key')
            if Verify(_ciphertext, _time,_key):
                user = User.objects.get(wxId = _wxid)
                thought = Thought.objects.get(id = _thoughtId)
                supp = SupportThought.objects.filter(userId=user).filter(thoughtId=thought)

                if supp:

                    supp.delete()
                    thought.supportNum=thought.supportNum - 1
                    thought.save()
                    lis = {'data': '', 'errorCode': 1000, 'flag': 'success', 'msg': 'has support'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                else:

                    suppThought = SupportThought(userId=user,thoughtId=thought)
                    suppThought.save()
                    thought.supportNum = thought.supportNum + 1
                    thought.save()
                    lis = {'data': '', 'errorCode': 1001, 'flag': 'success', 'msg': 'cancel support'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)

            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        json_str = json.dumps(lis)
        return HttpResponse(json_str)


#二级点赞/取消点赞
def Support_disone(request):
    print("Support_disone")
    try:
        if request.method == 'POST':
            _wxid = request.POST.get('wxid')
            _disoneId = request.POST.get('disoneId')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('time'))
            _key = request.POST.get('key')
            if Verify(_ciphertext, _time,_key):
                user = User.objects.get(wxId = _wxid)
                _disone= DiscussOne.objects.get(pk=_disoneId)
                suppdis = SupportDisone.objects.filter(userId=user,discussoneId=_disone)
                if suppdis:
                    suppdis.delete()
                    _disone.supportNum=_disone.supportNum - 1
                    _disone.save()
                    lis = {'data': '', 'errorCode': 1000, 'flag': 'success', 'msg': 'has support'}
                else:
                    suppDisone = SupportDisone(userId=user,discussoneId=_disone)
                    suppDisone.save()
                    _disone.supportNum = _disone.supportNum + 1
                    _disone.save()
                    lis = {'data': '', 'errorCode': 1001, 'flag': 'success', 'msg': 'cancel support'}

            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}

        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}

    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
    print(lis)
    json_str = json.dumps(lis)
    return HttpResponse(json_str)

#获取思想
def Get_thought(request):
    print('Get_thought')
    try:
        if request.method == 'GET':
            _page = request.GET.get('page')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')
            if Verify(_ciphertext, _time,_key):
                print(_page,'woca')
                thought = Thought.objects.all().order_by('weight')
                print(thought, 'wo32a')
                paginator = Paginator(thought, 20)
                try:
                    contacts = paginator.page(_page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    lis = {'data': '', 'errorCode': 200, 'flag': 'success', 'msg': 'the first page'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    lis = {'data': '', 'errorCode': 201, 'flag': 'success', 'msg': 'the last page'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                data = serializers.serialize('json', contacts.object_list)
                lis = {'data':json.loads(data),'errorCode':100,'flag':'success','msg':'ok'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        json_str = json.dumps(lis)
        return HttpResponse(json_str)

#获取一级评论
def Get_discussone(request):
    print('Get_discussone')
    try:
        if request.method == 'GET':
            _wxid = request.GET.get('wxid')
            _page = request.GET.get('page')
            _thoughtId = request.GET.get('thoughtId')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')
            if Verify(_ciphertext, _time,_key):
                user = User.objects.get(wxId=_wxid)
                disone = DiscussOne.objects.filter(thoughtId = _thoughtId).order_by('createTime')
                paginator = Paginator(disone, 20)
                print(disone)
                try:
                    contacts = paginator.page(_page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    lis = {'data': '', 'errorCode': 200, 'flag': 'success', 'msg': 'the first page'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    lis = {'data': '', 'errorCode': 201, 'flag': 'success', 'msg': 'the last page'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                data = serializers.serialize('json', contacts.object_list)
                sup = Get_disonesup(user,contacts.object_list)
                datas={'data':data,'sup':sup}
                lis = {'data': datas, 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                print(lis)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        json_str = json.dumps(lis)
        return HttpResponse(json_str)


#获取一级评论是否点赞
def Get_disonesup(user,disone):
    sup=[]
    for i in disone:
        c = SupportDisone.objects.filter(discussoneId=i).filter(userId=user)
        if c :
            sup.append(True)
        else:
            sup.append(False)
    return sup



#获取二级评论
def Get_discusstwo(request):
    print('Get_discusstwo')
    try:
        if request.method == 'GET':
            _page = request.GET.get('page')
            _discussoneId = request.GET.get('disOneId')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')
            print(_page)
            if Verify(_ciphertext, _time,_key):
                distwo = DiscussTwo.objects.filter(discussoneId = _discussoneId).order_by('createTime')
                print(distwo)
                paginator = Paginator(distwo, 20)
                try:
                    contacts = paginator.page(_page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    lis = {'data': '', 'errorCode': 200, 'flag': 'success', 'msg': 'the first page'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    lis = {'data': '', 'errorCode': 201, 'flag': 'success', 'msg': 'the last page'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                data = serializers.serialize('json', contacts.object_list)
                lis = {'data': data, 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                print(lis)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        json_str = json.dumps(lis)
        return HttpResponse(json_str)


#获取我的发表
def Get_mythought(request):
    print('Get_mythought')
    try:
        if request.method == 'GET':
            _wxid = request.GET.get('wxid')
            _page = request.GET.get('page')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')
            print(_wxid,_page)
            if Verify(_ciphertext, _time,_key):
                user = User.objects.get(wxId = _wxid)
                thought = Thought.objects.filter(userId=user).order_by('createTime')
                print('hzegegfjk', thought)
                paginator = Paginator(thought, 20)
                try:
                    contacts = paginator.page(_page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    lis = {'data': '', 'errorCode': 200, 'flag': 'success', 'msg': 'the first page'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    lis = {'data': '', 'errorCode': 201, 'flag': 'success', 'msg': 'the last page'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                data = serializers.serialize('json', contacts.object_list)
                lis = {'data': data, 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                print('hzegegfjklasjdfakl',lis)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        json_str = json.dumps(lis)
        return HttpResponse(json_str)

#获取我的评论
def Get_mydis(request):
    print("Get_mydis")
    try:
        if request.method == 'GET':
            _wxid = request.GET.get('wxid')
            _page = request.GET.get('page')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')
            print(_wxid,_page)
            if Verify(_ciphertext, _time,_key):
                user = User.objects.get(wxId = _wxid)
                discussone = DiscussOne.objects.filter(userId=user).order_by('createTime')
                paginator = Paginator(discussone, 20)
                print(paginator)
                try:
                    contacts = paginator.page(_page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    lis = {'data': '', 'errorCode': 200, 'flag': 'success', 'msg': 'the first page'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    lis = {'data': '', 'errorCode': 201, 'flag': 'success', 'msg': 'the last page'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                data = serializers.serialize('json', contacts.object_list)
                theme = []
                for i in contacts.object_list:
                    theme.append(i.thoughtId.content)
                datas={'dis':data,'theme':theme}
                lis = {'data': datas, 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}

    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
    print(lis)
    json_str = json.dumps(lis)
    return HttpResponse(json_str)

#获取我回复的看法
def Get_myReply(request):
    print("Get_myReply")
    try:
        if request.method == 'GET':
            _wxid = request.GET.get('wxid')
            _page = request.GET.get('page')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')
            print(_wxid,_page)
            if Verify(_ciphertext, _time,_key):
                user = User.objects.get(wxId = _wxid)
                discusstwo = DiscussTwo.objects.filter(userId=user).order_by('createTime')
                paginator = Paginator(discusstwo, 20)
                print(paginator)
                try:
                    contacts = paginator.page(_page)

                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.

                    lis = {'data': '', 'errorCode': 200, 'flag': 'success', 'msg': 'the first page'}
                    print(lis)
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    lis = {'data': '', 'errorCode': 201, 'flag': 'success', 'msg': 'the last page'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                data = serializers.serialize('json', contacts.object_list)
                theme = []
                thought = []
                for i in contacts.object_list:
                    theme.append(i.discussoneId.content)
                    thought.append(i.discussoneId.thoughtId.content)
                datas={'dis':data,'theme':theme,'thought':thought}
                lis = {'data': datas, 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                print(lis)
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}

    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
    print(lis)
    json_str = json.dumps(lis)
    return HttpResponse(json_str)

#获取头像，内容和作者信息
def Get_user_img(request):
    print('Get_user_img')
    try:
        if request.method == 'GET':
            _id = request.GET.get('id')
            _type = request.GET.get('ty')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')

            if Verify(_ciphertext, _time, _key):

                if _type=='thought':
                    thought = Thought.objects.get(pk=_id)
                    photoUrl = thought.userId.photoUrl
                    content = thought.content
                    auther = thought.auther
                    da = thought.createTime
                    date = str(da)
                    data = {'photoUrl': photoUrl, 'content': content, 'auther': auther,'date':date}
                elif _type=='discussone':
                    discussone = DiscussOne.objects.get(pk=_id)
                    photoUrl = discussone.userId.photoUrl
                    content = discussone.content
                    auther = discussone.auther
                    da = discussone.createTime
                    date = str(da)
                    data={'photoUrl':photoUrl,'content':content,'auther':auther,'date':date}
                lis = {'data': data, 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}
                print('0202',lis)
                json_str = json.dumps(lis)
                return HttpResponse(json_str)
        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}
            print('0303',lis)
            json_str = json.dumps(lis)
            return HttpResponse(json_str)
    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
        print('0404',lis)
        json_str = json.dumps(lis)
        return HttpResponse(json_str)

#获取是否点赞
def Or_support(request):
    print('Or_support')
    try:
        if request.method == 'GET':
            _wxid = request.GET.get('wxid')
            _selectId = request.GET.get('selectId')
            _type = request.GET.get('ty')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')
            print(_wxid,_selectId,_type)
            if Verify(_ciphertext, _time, _key):
                user = User.objects.get(wxId = _wxid)
                if _type=='thought':
                    thought = Thought.objects.get(pk=_selectId)
                    print(user, thought)
                    selected = SupportThought.objects.filter(userId=user).filter(thoughtId=thought)
                elif _type=='discussone':
                    discussone = DiscussOne.objects.get(pk=_selectId)
                    selected = SupportDisone.objects.filter(userId=user).filter(discussoneId=discussone)

                if selected:

                    lis = {'data': True, 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}

                else:
                    lis = {'data': False, 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}

            else:
                lis = {'data': '', 'errorCode': 101, 'flag': 'fail', 'msg': 'Verify is error'}

        else:
            lis = {'data': '', 'errorCode': 103, 'flag': 'fail', 'msg': 'request method error'}

    except:
        lis = {'data': '', 'errorCode': 104, 'flag': 'fail', 'msg': 'system is error'}
    json_str = json.dumps(lis)
    return HttpResponse(json_str)