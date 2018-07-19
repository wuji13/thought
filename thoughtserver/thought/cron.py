# -*- coding:utf-8 -*-
from .models import Thought,WeightFactor
from django.core.exceptions import ObjectDoesNotExist


def setWeight():
    try:
        weightFactor = WeightFactor.objects.get(name='one')
        sup = weightFactor.sup
        dis = weightFactor.dis
        time = weightFactor.time
    except ObjectDoesNotExist:
        sup = 1
        dis = 1
        time = 1

    thoughtObjects = Thought.objects.all()
    for item in thoughtObjects:
        item.weight = item.duration*time + item.discussNum*dis + item.supportNum*sup +item.selfW
        item.save()