from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from app1 import models
import random as r
# 认证模块
from django.contrib import auth

# 对应数据库
from django.contrib.auth.models import User


# Create your views here.

# 登录
def login(request):
    # models.Student.objects.all().update(identity='学生')  #就是更新一下数据
    # models.Teacher.objects.all().update(identity='师傅')
    error1 = ''
    error2 = ''
    # post请求
    if request.method == 'POST':
        # 获取用户提交用户id和密码
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user[0] == 's':
            # 在数据库学生表中查询
            user_obj = models.Student.objects.filter(pk=user).first()
            if not user_obj:
                error1 = '未查询到用户名'
            elif pwd != user_obj.s_password:
                error2 = '密码错误'
            else:
                all_tag = models.Tag.objects.all()
                all_tea_cou = models.TeaCou.objects.all().order_by("-t_c_satisfaction")  # 加个-号就是降序
                # 设置session
                request.session['is_login'] = True
                request.session['pk'] = user_obj.pk
                request.session['identity'] = user_obj.identity
                request.session['user'] = user_obj.s_name
                # request.session['user_obj'] = user_obj         #不能传对象

                return render(request, 'course_list.html',
                              {'user_obj': user_obj, "all_tea_cou": all_tea_cou,
                               "all_tag": all_tag})
        elif user[0] == 't':
            # 在数据库师傅表中查询
            user_obj = models.Teacher.objects.filter(pk=user).first()
            if not user_obj:
                error1 = '未查询到用户名'
            elif pwd != user_obj.t_password:
                error2 = '密码错误'
            else:
                all_tag = models.Tag.objects.all()
                all_tea_cou = models.TeaCou.objects.all().order_by("-t_c_satisfaction")  # 加个-号就是降序
                request.session['is_login'] = True
                request.session['pk'] = user_obj.pk
                request.session['identity'] = user_obj.identity
                request.session['user'] = user_obj.t_name
                # request.session['user_obj'] = user_obj

                return render(request, 'course_list.html',
                              {'user_obj': user_obj, "all_tea_cou": all_tea_cou,
                               "all_tag": all_tag})
    return render(request, 'login.html', {'error1': error1, 'error2': error2})


# 登出
def logout(request):
    # del request.session["is_login"] # 删除session_data里的一组键值对
    request.session.flush()  # 删除一条记录包括(session_key session_data expire_date)三个字段
    return redirect('/login/')


# 课程列表

def course_list(request: HttpRequest) -> HttpResponse:
    # 登录后才能访问
    status = request.session.get('is_login')
    if not status:
        return redirect('/login/')
    all_tea_cou = []
    all_tag = models.Tag.objects.all()
    if request.method == "GET":
        # get
        # 获取所有的课程信息
        all_tea_cou = models.TeaCou.objects.all().order_by("-t_c_satisfaction")  # 加个-号就是降序
        return render(request, "course_list.html", {"all_tea_cou": all_tea_cou, "all_tag": all_tag})

    # 此部分以移交至search.py
    # else:
    #     # post
    #     # 获取用户提交的课程名
    #     course_name = request.POST.get('course_name')
    #     # 在数据库中查询
    #     # cou_obj = models.Course.objects.filter(c_name__contains=course_name)     #set
    #     # cou_obj = models.Course.objects.filter(c_name__contains=course_name).first()   #查一个课程
    #     # all_tea_cou = cou_obj.teacou_set.all()            #set没有teacou_set属性
    #     #print(type(cou_obj))
    #     # for cou in cou_obj:   #正确查询到了
    #     #     print(cou.c_name)
    #     all_tea_cou = models.TeaCou.objects.filter(c__c_name__contains=course_name)     #正向模糊查询的到set,通过外键加__，连接到对应类，获得属性
    #     return render(request, 'course_list.html', {'all_tea_cou': all_tea_cou, 'all_tag': all_tag})


# 课程详情
def course_info(request: HttpRequest) -> HttpResponse:
    status = request.session.get('is_login')
    if not status:
        return redirect('/login/')
    # 获取url ？后面的参数
    pk = request.GET.get("pk")
    tea_cou = models.TeaCou.objects.get(pk=pk)
    course = models.Course.objects.get(pk=tea_cou.c.course_id)
    if request.method == "GET":
        # get 返回一个页面 页面包含课程信息及操作
        return render(request, "course_info.html", {"tea_cou": tea_cou, "course": course})

    return render(request, "course_info.html")


# 师傅列表
def teacher_list(request: HttpRequest) -> HttpResponse:
    status = request.session.get('is_login')
    if not status:
        return redirect('/login/')
    # 获取所有老师信息
    teacher_obj_top = models.Teacher.objects.filter(c_num__gt=0).order_by('-hot')[0:10]  # 取top10
    teacher_obj = models.Teacher.objects.filter(c_num__gt=0).order_by('-hot')
    return render(request, "teacher_list.html", {'teacher_obj': teacher_obj, 'teacher_obj_top': teacher_obj_top})


# 问题列表
def problem_list(request: HttpRequest) -> HttpResponse:
    status = request.session.get('is_login')
    if not status:
        return redirect('/login/')
    return render(request, "problem_list.html")


# 学生的or师傅的 我的
def my(request: HttpRequest) -> HttpResponse:
    status = request.session.get('is_login')
    if not status:
        return redirect('/login/')
    identity = request.session.get('identity')
    #学生或师傅的主键
    pk = request.session.get('pk')
    #print(pk)
    if identity == '师傅':
        all_tea_cou = models.TeaCou.objects.filter(t=pk)
        return render(request, "teacher_my.html", {'all_tea_cou': all_tea_cou})
    else:   #学生
        all_teach = models.Teach.objects.filter(s_id=pk)
        return render(request, "student_my.html",{'all_teach':all_teach})


# 关于我们
def team(request: HttpRequest) -> HttpResponse:
    return render(request, "team.html")


# 添加授课
def t_cou_add(request):
    error = ''
    # 提交form表单时，post请求
    if request.method == 'POST':
        # 获取师傅pk
        pk = request.session.get('pk')
        cou_id = request.POST.get('cou_id')
        info = request.POST.get('info')
        price = request.POST.get('price')
        t_c_hot = r.randint(30, 75)
        t_c_satisfaction = r.randint(30, 75)
        status = 1   #可选状态
        sum_student = 0
        # 将数据插入数据库
        models.TeaCou.objects.create(t_id=pk, c_id=cou_id, info=info, price=price,t_c_hot=t_c_hot,
                                     t_c_satisfaction=t_c_satisfaction, status=status, sum_student=sum_student)
        return redirect('/my/')
    all_courses = models.Course.objects.all()

    return render(request, 't_cou_add.html', {'all_courses': all_courses})
