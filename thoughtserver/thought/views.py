from django.shortcuts import render
import requests
import json
import datetime,time
from datetime import timedelta
from django.http import HttpResponse
from .models import Developer,User,Thought,DiscussOne,DiscussTwo,SupportThought,SupportDisone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
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
            print(_wxid)
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('time'))
            _key = request.POST.get('key')
            _photoUrl = request.POST.get('photoUrl')
            print(_photoUrl)
            _name = request.POST.get('name')
            print(_name)
            if Verify(_ciphertext, _time,_key):
                u = User.objects.get(wxId=_wxid)
                if u:
                    u.name = _name
                    u.photoUrl = _photoUrl
                    u.save()
                    lis = {'data': '', 'errorCode': 102, 'flag': 'success', 'msg': 'user already exist '}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                else:
                    user = User(wxId=_wxid,photoUrl=_photoUrl,name=_name)
                    user.save()
                    lis = {'data': '', 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
                    print(type(lis))
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
    try:
        if request.method == 'POST':
            _wxid = request.POST.get('wxid')
            _content = request.POST.get('content')
            _thoughtId = request.POST.get('thoughtId')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('time'))
            _key = request.POST.get('key')
            if Verify(_ciphertext, _time,_key):
                user = User.objects.get(wxId = _wxid)
                thought = Thought.objects.get(pk=_thoughtId)
                dis_one = DiscussOne(thoughtId=thought,userId=user,content=_content,auther=user.name)
                dis_one.save()

                thought.discussNum = thought.discussNum + 1
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



#二级评论想法
def Discuss_two(request):
    try:
        if request.method == 'POST':
            _wxid = request.POST.get('wxid')
            _content = request.POST.get('content')
            _discussOneId = request.POST.get('thoughtOneId')
            _ciphertext = int(request.POST.get('ciphertext'))
            _time = int(request.POST.get('time'))
            _key = request.POST.get('key')
            if Verify(_ciphertext, _time,_key):
                user = User.objects.get(wxId = _wxid)
                discussOne = DiscussOne.objects.get(pk=_discussOneId)
                dis_two = DiscussOne(discussoneId=discussOne,userId=user,content=_content,auther=user.name)
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
            print('1',_thoughtId)
            if Verify(_ciphertext, _time,_key):
                print('12')
                user = User.objects.get(wxId = _wxid)
                print('13', user)
                thought = Thought.objects.get(id = _thoughtId)
                print('14',thought)
                supp = SupportThought.objects.filter(userId=user).filter(thoughtId=thought)
                print('2')
                if supp:
                    print('3')
                    supp.delete()
                    thought.supportNum=thought.supportNum - 1
                    thought.save()
                    lis = {'data': '', 'errorCode': 1000, 'flag': 'success', 'msg': 'has support'}
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                else:
                    print('4')
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
                    json_str = json.dumps(lis)
                    return HttpResponse(json_str)
                else:
                    suppDisone = SupportDisone(userId=user,discussoneId=_disone)
                    suppDisone.save()
                    _disone.supportNum = _disone.supportNum + 1
                    _disone.save()
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
                thought = Thought.objects.all().order_by('weight')
                paginator = Paginator(thought, 4)
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
                lis = {'data':data,'errorCode':100,'flag':'success','msg':'ok'}
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
    try:
        if request.method == 'GET':
            _page = request.GET.get('page')
            _thoughtId = request.GET.get('thoughtId')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')
            if Verify(_ciphertext, _time,_key):
                disone = DiscussOne.objects.filter(thoughtId = _thoughtId)
                paginator = Paginator(disone, 20)
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

#获取二级评论
def Get_discusstwo(request):
    try:
        if request.method == 'GET':
            _page = request.GET.get('page')
            _discussoneId = request.GET.get('discussoneId')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')
            if Verify(_ciphertext, _time,_key):
                distwo = DiscussTwo.objects.filter(discussoneId = _discussoneId)
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
    try:
        if request.method == 'GET':
            _wxid = request.GET.get('wxid')
            _page = request.GET.get('page')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')
            if Verify(_ciphertext, _time,_key):
                user = User.objects.get(wxId = _wxid)
                thought = Thought.objects.filter(userId=user)
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
                data = {'contacts':contacts}
                lis = {'data': data, 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
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
    try:
        if request.method == 'GET':
            _wxid = request.GET.get('wxid')
            _page = request.GET.get('page')
            _ciphertext = int(request.GET.get('ciphertext'))
            _time = int(request.GET.get('time'))
            _key = request.GET.get('key')
            if Verify(_ciphertext, _time,_key):
                user = User.objects.get(wxId = _wxid)
                discussone = DiscussOne.objects.filter(userId=user)
                paginator = Paginator(discussone, 20)
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
                data = {'contacts':contacts}
                lis = {'data': data, 'errorCode': 100, 'flag': 'success', 'msg': 'ok'}
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