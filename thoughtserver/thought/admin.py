# -*- coding:utf-8 -*-

from django.contrib import admin
from thought.models import User,Thought,DiscussTwo,DiscussOne,SupportDisone,SupportThought,Developer,WeightFactor
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name','wxId','createTime','time')

class ThoughtAdmin(admin.ModelAdmin):
    list_display = ('id','auther','createTime','content')

    search_fields = ('aither','id','content')

class DiscussTwoAdmin(admin.ModelAdmin):
    list_display = ('id', 'auther', 'createTime')

class DiscussOneAdmin(admin.ModelAdmin):
    list_display = ('id', 'auther', 'createTime')

class SupportDisoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'createTime')

class SupportThoughtAdmin(admin.ModelAdmin):
    list_display = ('id', 'createTime')

class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class WeightFactorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(User,UserAdmin)
admin.site.register(Thought,ThoughtAdmin)
admin.site.register(DiscussTwo,DiscussTwoAdmin)
admin.site.register(DiscussOne,DiscussOneAdmin)
admin.site.register(SupportDisone,SupportDisoneAdmin)
admin.site.register(SupportThought,SupportThoughtAdmin)
admin.site.register(Developer,DeveloperAdmin)
admin.site.register(WeightFactor,WeightFactorAdmin)
