"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views, search,manage


urlpatterns = [            #将{}改为[]，TypeError: 'set' object is not reversible
    #views.py
    path("admin/", admin.site.urls),
    path("login/", views.login),
    path("logout/", views.logout),
    path("course_list/", views.course_list),
    path("course_info/", views.course_info),
    path("teacher_list/", views.teacher_list),
    path("problem_list/", views.problem_list),
    path("my/", views.my),
    # path("teacher_my/", views.my),
    path("t_cou_add/", views.t_cou_add),
    path("team/", views.team),

    #search.py
    path("course_search/", search.course_search),
    #该师傅所教课程
    path("t_course_search/", search.t_course_search),
    path("teacher_search/", search.teacher_search),
    path("tag_search/", search.tag_search),
    path("teach_search/", search.teach_search),
    path("problem_search/", search.problem_search),

    #manage.py
    path("indent_create/", manage.indent1_create),
    path("my_account/", manage.my_account),
    path("stu_add_my_account/", manage.stu_add_my_account),
    path("tea_trans_my_account/", manage.tea_trans_my_account),
    path("talk/", manage.talk),
    path("stu_add_problem/", manage.stu_add_problem),
    path("tea_ans_problem/", manage.tea_ans_problem),
    path("my_indent/", manage.my_indent),
    path("my_info/", manage.my_info),
    path("tea_my_student/", manage.tea_my_student),
    path("stu_exam/", manage.stu_exam),


]
