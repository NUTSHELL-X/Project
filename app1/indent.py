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


def indent_create(request):
    indetity = request.session.get('indetity')
    t_c_pk = request.GET.get('pk')  # 授课主键
    if indetity == '师傅':
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
            models.Indent.objects.create(s_id=s_id, tea_cou_id=t_c_pk, price=tea_cou_obj.price, status=status,
                                         type=type,create_time=create_time)
            return redirect('/my/')

        return render(request, 'indent_create.html', {'stu_obj': stu_obj, 'tea_cou_obj': tea_cou_obj})
