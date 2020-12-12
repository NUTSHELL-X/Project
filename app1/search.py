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

#查询相应师傅的课程
def t_course_search(request):
    #获取？后的师傅主键
    pk = request.GET.get('pk')
    #查询数据库
    all_tea_cou = models.TeaCou.objects.filter(t=pk)   #名字要取一样的，不然渲染不出来
    all_tag = models.Tag.objects.all()

    return render(request,'course_list.html',{'all_tea_cou':all_tea_cou,'all_tag':all_tag})


def teacher_search(request):
    teacher_obj_top = models.Teacher.objects.filter(c_num__gt=0).order_by('-hot')[0:10]  # 取top10
    teacher_name = request.POST.get('teacher_name')
    # 在数据库中查询
    teacher_obj = models.Teacher.objects.filter(t_name__contains=teacher_name)
    return render(request,'teacher_list.html',{'teacher_obj_top':teacher_obj_top,'teacher_obj':teacher_obj})