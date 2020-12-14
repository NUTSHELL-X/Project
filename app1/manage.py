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
from decimal import Decimal
import random as r


def indent1_create(request):
    error = ''
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
            if tea_cou_obj.price > stu_obj.account:
                error = '账户余额不足'
            else:
                type = 1
                status = 1
                create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                models.Indent.objects.create(s_id=s_id, tea_cou_id=t_c_pk, price=tea_cou_obj.price, status=status,
                                             # 这里突然报错，o(╥﹏╥)o,
                                             type_id=type,
                                             create_time=create_time)  # 问题出在触发器上,tea_cou的t_id有多个值,要用新表new的数据,o(╥﹏╥)o
                # new就不是一个表o(╥﹏╥)o
                models.Teach.objects.create(s_id=s_id, tea_cou_id=t_c_pk, status=status, create_time=create_time)
                return redirect('/my/')

        return render(request, 'indent_create.html', {'stu_obj': stu_obj, 'tea_cou_obj': tea_cou_obj, 'error': error})


def my_account(request):
    identity = request.session.get('identity')
    # 获取学生或师傅pk
    pk = request.session.get('pk')
    if identity == '师傅':
        # 从数据库查询
        tea_obj = models.Teacher.objects.filter(pk=pk).first()
        return render(request, 'tea_account.html', {'tea_obj': tea_obj})
    else:
        stu_obj = models.Student.objects.filter(pk=pk).first()
        return render(request, 'stu_account.html', {'stu_obj': stu_obj})


def talk(request):
    identity = request.session.get('identity')
    # 获取学生或师傅pk
    pk = request.session.get('pk')
    # 获取tea_cou（任教）编号
    tea_cou_id = request.GET.get('pk')
    tea_cou_obj = models.TeaCou.objects.filter(pk=tea_cou_id).first()
    if identity == '师傅':
        # 从数据库查询
        # 师傅在该任教所有的辅导
        all_teach = models.Teach.objects.filter(tea_cou_id=tea_cou_id)
        all_problem = models.Problem.objects.filter(tea_cou_id=tea_cou_id)
        return render(request, 'tea_talk.html',
                      {'all_teach': all_teach, 'tea_cou_obj': tea_cou_obj, 'all_problem': all_problem})
    else:  # 学生
        stu_obj = models.Student.objects.filter(pk=pk).first()
        all_problem = models.Problem.objects.filter(s_id=stu_obj.pk).filter(tea_cou_id=tea_cou_id)  # 需要有学生，任教双重过滤
        return render(request, 'stu_talk.html',
                      {'stu_obj': stu_obj, 'tea_cou_obj': tea_cou_obj, 'all_problem': all_problem})


def my_indent(request):
    identity = request.session.get('identity')
    # 获取学生或师傅pk
    pk = request.session.get('pk')
    if identity == '师傅':
        all_indent_obj = models.Indent.objects.filter(tea_cou__t=pk)  # 正向

        return render(request, 'tea_indent.html', {'all_indent_obj': all_indent_obj})
    else:
        all_indent_obj = models.Indent.objects.filter(s=pk)
        return render(request, 'stu_indent.html', {'all_indent_obj': all_indent_obj})


def my_info(request):
    identity = request.session.get('identity')
    # 获取学生或师傅pk
    pk = request.session.get('pk')
    if identity == '师傅':
        # 从数据库查询
        tea_obj = models.Teacher.objects.filter(pk=pk).first()
        return render(request, 'tea_info.html', {'tea_obj': tea_obj})
    else:
        stu_obj = models.Student.objects.filter(pk=pk).first()
        return render(request, 'stu_info.html', {'stu_obj': stu_obj})


# 师傅学生管理
def tea_my_student(request):
    # 师傅的主键
    pk = request.session.get('pk')
    all_teach = models.Teach.objects.filter(tea_cou__t=pk)
    return render(request, 'tea_my_student.html', {'all_teach': all_teach})


def stu_exam(request):
    return render(request, 'stu_exam.html')


def stu_add_problem(request):
    error = ''
    # 获取?后的任教id及学生id,post请求也行，只要action的url上带上就行
    tea_cou_id = request.GET.get('tea_cou_id')
    s_id = request.GET.get('s_id')
    # 从数据库中获取数据
    tea_cou_obj = models.TeaCou.objects.filter(pk=tea_cou_id).first()
    stu_obj = models.Student.objects.filter(pk=s_id).first()
    if request.method == 'POST':
        p_info = request.POST.get('p_info')
        if not p_info:
            error = '问题不能为空'
        else:
            create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            type = 1
            models.Problem.objects.create(s_id=s_id, tea_cou_id=tea_cou_id, type_id=type, p_info=p_info,
                                          create_time=create_time)  # 将问题写入数据库
            all_problem = models.Problem.objects.filter(s_id=s_id).filter(tea_cou_id=tea_cou_id)
            return render(request, 'stu_talk.html',
                          {'stu_obj': stu_obj, 'tea_cou_obj': tea_cou_obj, 'all_problem': all_problem})

    return render(request, 'stu_add_problem.html', {'tea_cou_obj': tea_cou_obj, 'stu_obj': stu_obj, 'error': error})


def tea_ans_problem(request):
    error = ''
    # 获取？的问题编号
    p_id = request.GET.get('p_id')
    pro_obj = models.Problem.objects.filter(pk=p_id).first()
    if request.method == 'POST':
        p_ans = request.POST.get('p_ans')
        if not p_ans:
            error = '回答不能为空'
        else:
            p_price = request.POST.get('p_price')
            ans_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            models.Problem.objects.filter(pk=p_id).update(p_ans=p_ans, p_price=p_price, ans_time=ans_time)
            # 回到学生管理
            pk = request.session.get('pk')
            all_teach = models.Teach.objects.filter(tea_cou__t=pk)
            return render(request, 'tea_my_student.html', {'all_teach': all_teach})

    return render(request, 'tea_ans_problem.html', {'pro_obj': pro_obj, 'error': error})


def stu_add_my_account(request):
    error = ''
    # 从session获取学生pk
    s_id = request.session.get('pk')
    stu_obj = models.Student.objects.filter(pk=s_id).first()
    if request.method == 'POST':
        add_account = request.POST.get('add_account')
        if not add_account:
            error = '请输入金额'
        else:
            add_account = Decimal(request.POST.get('add_account'))  # 这里获取的都默认是字符串
            # print(type(add_account))
            if add_account <= 0:
                error = '充值金额需要大于0'
            else:
                account = stu_obj.account + add_account
                models.Student.objects.filter(pk=s_id).update(account=account)
                # return render(request, 'stu_account.html', {'stu_obj': stu_obj})
                return redirect('/my_account/')        #这里用这种
    return render(request, 'stu_add_my_account.html', {'stu_obj': stu_obj, 'error': error})


def tea_trans_my_account(request):
    error = ''
    t_id = request.session.get('pk')
    tea_obj = models.Teacher.objects.filter(pk=t_id).first()
    if request.method == 'POST':
        trans_account = request.POST.get('trans_account')
        #判空要放在最前面
        if not trans_account:
            error = '请输入金额'
        else:
            trans_account = Decimal(trans_account)
            if trans_account > tea_obj.account:
                error = '提现超出账户余额'
            elif trans_account <= 0:
                error = '提现金额需要大于0'
            else:
                account = tea_obj.account - trans_account
                models.Teacher.objects.filter(pk=t_id).update(account=account)
                # return render(request, 'tea_account.html', {'tea_obj': tea_obj})
                return redirect('/my_account/')
    return render(request, 'tea_trans_my_account.html', {'tea_obj': tea_obj, 'error': error})
