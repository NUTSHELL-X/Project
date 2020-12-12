from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from app1 import models


# Create your views here.

# 登录
def login(request):
    error1 = ''
    error2 = ''
    # 获取用户提交用户id和密码
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    # 在数据库中查询
    user_obj = models.Student.objects.filter(pk=user).first()
    if request.method == 'POST':
        if not user_obj:
            error1 = '未查询到用户名'
        elif pwd != user_obj.s_password:
            error2 = '密码错误'
        else:
            all_tag = models.Tag.objects.all()
            all_tea_cou = models.TeaCou.objects.all().order_by("-t_c_satisfaction")  # 加个-号就是降序

            return render(request,'course_list.html',{'user_obj':user_obj,"all_tea_cou": all_tea_cou, "all_tag": all_tag})

    return render(request, 'login.html',{'error1':error1,'error2':error2})


# 课程列表

def course_list(request: HttpRequest) -> HttpResponse:
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
    # 获取所有老师信息

    return render(request, "teacher_list.html")


# 问题列表
def problem_list(request: HttpRequest) -> HttpResponse:
    return render(request, "problem_list.html")


# 学生的我的
def student_my(request: HttpRequest) -> HttpResponse:
    return render(request, "student_my.html")


# 关于我们
def team(request: HttpRequest) -> HttpResponse:
    return render(request, "team.html")


def course_list2(request: HttpRequest) -> HttpResponse:
    # get
    # 获取所有的课程信息
    all_tea_cou = models.TeaCou.objects.all()

    return render(request, "course_list2.html", {"all_tea_cou": all_tea_cou})
