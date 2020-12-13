#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Time    : 2020/12/12 21:27
@Author  : wyp
@File    : indent.py
@Software: win10  python3.7
'''
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from app1 import models
from datetime import datetime
import random as r


def indent1_create(request):
    identity = request.session.get('identity')
    t_c_pk = request.GET.get('pk')  # 授课主键
    if identity == '师傅':
        tea_cou = models.TeaCou.objects.get(pk=t_c_pk)
        course = models.Course.objects.get(pk=tea_cou.c.course_id)
        return render(request, 'course_info.html', {'tea_cou': tea_cou, 'course': course, 'error': '师傅无法拜师'})
    else:
        # get
        s_id = request.session.get('pk')  # 学生编号
        # 从数据库查询数据
        stu_obj = models.Student.objects.filter(pk=s_id).first()
        tea_cou_obj = models.TeaCou.objects.filter(pk=t_c_pk).first()  # 要.first取出来，要不然是一个集合QuerySet
        # post请求
        if request.method == 'POST':
            type = 1
            status = 1
            create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # print(s_id)
            # print(t_c_pk)
            # print(tea_cou_obj.price)
            # print(status)
            # print(type)
            # print(create_time)
            models.Indent.objects.create(s_id=s_id, tea_cou_id=t_c_pk, price=tea_cou_obj.price, status=status,  #这里突然报错，o(╥﹏╥)o,
                                         type=type,create_time=create_time)                            #问题出在触发器上,tea_cou的t_id有多个值,要用新表new的数据,o(╥﹏╥)o
                                                                                                        #new就不是一个表o(╥﹏╥)o
            models.Teach.objects.create(s_id=s_id, tea_cou_id=t_c_pk,status=status,create_time=create_time)
            return redirect('/my/')

        return render(request, 'indent_create.html', {'stu_obj': stu_obj, 'tea_cou_obj': tea_cou_obj})


def my_account(request):
    identity = request.session.get('identity')
    #获取学生或师傅pk
    pk = request.session.get('pk')
    if identity == '师傅':
        #从数据库查询
        tea_obj = models.Teacher.objects.filter(pk=pk).first()
        return render(request,'tea_account.html',{'tea_obj':tea_obj})
    else:
        stu_obj = models.Student.objects.filter(pk=pk).first()
        return render(request,'stu_account.html',{'stu_obj':stu_obj})


def talk(request):

    return render(request,'')


def my_indent(request):

    return None


def my_info(request):

    return None


def tea_my_student(request):

    return None


def stu_exam(request):
    
    return None