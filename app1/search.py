"""
@Time    : 2020/12/7 20:09
@Author  : wyp
@File    : search.py
@Software: win10  python3.7
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from app1 import models

# 搜索模块


def course_search(request: HttpRequest) -> HttpResponse:
    all_tag = models.Tag.objects.all()
    course_name = request.POST.get("course_name")
    # 在数据库中查询
    # cou_obj = models.Course.objects.filter(c_name__contains=course_name)     #set
    # cou_obj = models.Course.objects.filter(c_name__contains=course_name).first()   #查一个课程
    # all_tea_cou = cou_obj.teacou_set.all()            #set没有teacou_set属性
    # print(type(cou_obj))
    # for cou in cou_obj:   #正确查询到了
    #     print(cou.c_name)
    all_tea_cou = models.TeaCou.objects.filter(c__c_name__contains=course_name)  # 正向模糊查询的到set,通过外键加__，连接到对应类，获得属性
    return render(request, "course_list.html", {"all_tea_cou": all_tea_cou, "all_tag": all_tag})
