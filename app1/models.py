from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    c_name = models.CharField(max_length=30)
    c_tag = models.ForeignKey('Tag', models.DO_NOTHING)
    c_info = models.TextField(blank=True, null=True)
    c_hot = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'course'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Indent(models.Model):
    indent_id = models.AutoField(primary_key=True)
    s = models.ForeignKey('Student', models.DO_NOTHING)
    tea_cou = models.ForeignKey('TeaCou', models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'indent'


class Problem(models.Model):
    problem_id = models.AutoField(primary_key=True)
    p_info = models.TextField()
    p_ans = models.TextField(blank=True, null=True)
    c_id = models.IntegerField()
    p_price = models.FloatField()
    create_time = models.DateTimeField(blank=True, null=True)
    t_id = models.CharField(max_length=11)
    s_id = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'problem'


class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=11)
    s_name = models.CharField(max_length=30)
    s_password = models.CharField(max_length=30)
    sex = models.CharField(max_length=2, blank=True, null=True)
    grade = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=30)
    tel = models.CharField(max_length=11, blank=True, null=True)
    account = models.PositiveIntegerField()
    info = models.TextField(blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    last_login_time = models.DateTimeField(blank=True, null=True)
    identity = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'


class Tag(models.Model):
    tag_id = models.IntegerField(primary_key=True)
    tag_name = models.CharField(max_length=30)
    creat_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tag'


class TeaCou(models.Model):
    tea_cou_id = models.AutoField(primary_key=True)
    t = models.ForeignKey('Teacher', models.DO_NOTHING)
    c = models.ForeignKey(Course, models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    t_c_hot = models.IntegerField(blank=True, null=True)
    t_c_satisfaction = models.IntegerField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    sum_student = models.IntegerField(blank=True, null=True)
    creat_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tea_cou'


class Teach(models.Model):
    teach_id = models.AutoField(primary_key=True)
    s = models.ForeignKey(Student, models.DO_NOTHING)
    tea_cou = models.ForeignKey(TeaCou, models.DO_NOTHING, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    create_time = models.DateTimeField(blank=True, null=True)
    finish_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teach'


class Teacher(models.Model):
    teacher_id = models.CharField(primary_key=True, max_length=11)
    t_name = models.CharField(max_length=30)
    t_password = models.CharField(max_length=30)
    sex = models.CharField(max_length=2, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    tel = models.CharField(max_length=11, blank=True, null=True)
    account = models.PositiveIntegerField()
    info = models.TextField(blank=True, null=True)
    c_num = models.IntegerField()
    stu_num = models.IntegerField(blank=True, null=True)
    hot = models.IntegerField(blank=True, null=True)
    satisfaction = models.IntegerField(blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    last_login_time = models.DateTimeField(blank=True, null=True)
    identity = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacher'
