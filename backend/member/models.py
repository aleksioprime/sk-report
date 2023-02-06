from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from django.contrib.auth.models import AbstractUser

class RoleUser(models.Model):
    """ Роли пользователей """
    name = models.CharField(max_length=16, verbose_name=_("Название роли"))
    codename = models.CharField(max_length=16, verbose_name=_("Кодовое имя"))
    class Meta:
        verbose_name = 'Роль пользователей'
        verbose_name_plural = 'Роли пользователей'
        ordering = ['name']
    def __str__(self):
        return '{}'.format(self.name)

class Department(models.Model):
    """ Учебные подразделения / Кафедры """
    name = models.CharField(max_length=255, verbose_name=_("Название кафедры"))
    class Meta:
        verbose_name = 'Кафедра'
        verbose_name_plural = 'Кафедры'
        ordering = ['name']
    def __str__(self):
        return '{}'.format(self.name)

class User(AbstractUser):
    """ Расширение модели пользователя """
    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        ('O', 'Не указан')
    )
    id_str = models.CharField(editable=False, unique=True, max_length=10)
    middle_name = models.CharField(max_length=32, verbose_name=_("Отчество"), null=True, blank=True)
    date_of_birth = models.DateField(max_length=10, verbose_name=_("Дата рождения"), null=True, blank=True)
    gender = models.CharField(max_length=1, verbose_name=_("Пол"), choices=GENDER_CHOICES, default='O', null=True, blank=True)
    photo = models.ImageField(upload_to="member_photos", blank=True, verbose_name=_("Фотография"), null=True)
    role = models.ManyToManyField('member.RoleUser', verbose_name=_("Роли пользователя"), blank=True, related_name="role_user")
    position = models.CharField(max_length=255, verbose_name=_("Должность"), blank=True, null=True)
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name']
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.id_str:                                
            self.id_str = "u" + str(self.id + (10 ** 5))
            self.save() 
    def get_full_name(self):
        full_name = "{} {} {}".format(self.last_name, self.first_name, self.middle_name)
        return full_name.strip()
    def get_short_name(self):
        if self.first_name:
            return "{} {}.".format(self.last_name, self.first_name[0])

class ProfileStudent(models.Model):
    """ Дополнительный профиль студента """
    user = models.OneToOneField('member.User', verbose_name=_("Пользователь"), related_name='student',
                                blank=True, null=True, on_delete=models.SET_NULL)
    short_name = models.CharField(max_length=32, verbose_name=_("Студент"), null=True, blank=True)
    id_dnevnik = models.CharField(verbose_name=_('ID системы Дневник.РУ'), max_length=40, blank=True, null=True)
    group = models.ForeignKey('assess.ClassGroup', verbose_name=_("Класс"), on_delete=models.SET_NULL,
                              null=True, blank=True, related_name="student")
    class Meta:
        verbose_name = 'Профиль студента'
        verbose_name_plural = 'Профили студентов'
        ordering = ['group', 'user']
    def __str__(self):
        return '{} - {}'.format(self.group, self.user)
    def save(self, *args, **kwargs):
        if not self.short_name:
            if self.user:
                self.short_name = "{} {}.".format(self.user.first_name, self.user.last_name[0])
        super(ProfileStudent, self).save(*args, **kwargs)

class ProfileTeacher(models.Model):
    """ Дополнительный профиль учителя """
    user = models.OneToOneField('member.User', verbose_name=_("Пользователь"), related_name='teacher',
                                blank=True, null=True, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=32, verbose_name=_("Учитель"), null=True, blank=True)
    id_dnevnik = models.CharField(verbose_name=_('ID системы Дневник.РУ'), max_length=40, blank=True, null=True)
    # departments = models.ManyToManyField('member.Department', verbose_name=_("Отдел"),
    #                                   blank=True, related_name="teacher")
    class Meta:
        verbose_name = 'Профиль учителя'
        verbose_name_plural = 'Профили учителей'
        ordering = ['user']
    def __str__(self):
        return '{}'.format(self.user)
    def save(self, *args, **kwargs):
        if not self.short_name:
            if self.user:
                if self.user.middle_name:
                    self.short_name = "{} {}. {}.".format(self.user.last_name, self.user.first_name[0], self.user.middle_name[0], )
                else:
                    self.short_name = "{} {}.".format(self.user.last_name, self.user.first_name[0])
        super(ProfileTeacher, self).save(*args, **kwargs)

class WorkLoad(models.Model):
    """ Преподавательская нагрузка """
    teacher = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Учитель"), on_delete=models.CASCADE,
                              null=True, blank=True, related_name="workload")
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.CASCADE,
                                      null=True, blank=True, related_name="workload")
    group = models.ForeignKey('assess.ClassGroup', verbose_name=_("Класс"), on_delete=models.CASCADE,
                              null=True, blank=True, related_name="workload")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Часы"), default=1)
    class Meta:
        verbose_name = 'Рабочая нагрузка'
        verbose_name_plural = 'Рабочие нагрузки'
        ordering = ['teacher']
    def __str__(self):
        return '{} ({} - {} ч.)'.format(self.teacher, self.subject, self.hours)
    