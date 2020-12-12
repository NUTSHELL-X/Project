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
from app1 import views, search,indent


urlpatterns = [            #将{}改为[]，TypeError: 'set' object is not reversible
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

    path("course_search/", search.course_search),
    #该师傅所教课程
    path("t_course_search/", search.t_course_search),
    path("teacher_search/", search.teacher_search),

    path("indent_create/", indent.indent_create),


]
