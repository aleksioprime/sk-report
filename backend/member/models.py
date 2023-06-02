from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    """ Учебные подразделения / Кафедры """
    name = models.CharField(max_length=255, verbose_name=_("Название кафедры"))
    photo = models.ImageField(upload_to="department_pictures", blank=True, verbose_name=_("Фотография"), null=True)
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
    middle_name = models.CharField(max_length=32, verbose_name=_("Отчество"), null=True, blank=True)
    date_of_birth = models.DateField(max_length=10, verbose_name=_("Дата рождения"), null=True, blank=True)
    gender = models.CharField(max_length=1, verbose_name=_("Пол"), choices=GENDER_CHOICES, default='O', null=True, blank=True)
    photo = models.ImageField(upload_to="member_photos", blank=True, verbose_name=_("Фотография"), null=True)
    access_token_dnevnik = models.CharField(max_length=255, verbose_name=_("Токен для подключения к Дневник.РУ"), null=True, blank=True)
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name', 'is_active']
    def get_full_name(self):
        if not self.middle_name:
            full_name = f"{self.last_name} {self.first_name}"
        else:
            full_name = f"{self.last_name} {self.first_name} {self.middle_name}"
        return full_name.strip()
    def get_short_name(self):
        if self.first_name and self.middle_name:
            return f"{self.last_name} {self.first_name[0]}. {self.middle_name[0]}."
        elif self.first_name:
            return f"{self.last_name} {self.first_name[0]}."
        else:
            return f"{self.last_name} {self.first_name}"
    def __str__(self):
        return '{} {}'.format(self.last_name, self.first_name)

class ProfileStudent(models.Model):
    """ Дополнительный профиль студента """
    user = models.OneToOneField('member.User', verbose_name=_("Пользователь"), related_name='student', null=True, on_delete=models.CASCADE)
    id_dnevnik = models.CharField(verbose_name=_('ID системы Дневник.РУ'), max_length=40, blank=True, null=True)
    # group = models.ForeignKey('assess.ClassGroup', verbose_name=_("Класс"), on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    class Meta:
        verbose_name = 'Профиль студента'
        verbose_name_plural = 'Профили студентов'
        ordering = ['user']
    def __str__(self):
        return '{}'.format(self.user)

class ProfileTeacher(models.Model):
    """ Дополнительный профиль учителя """
    user = models.OneToOneField('member.User', verbose_name=_("Пользователь"), related_name='teacher', null=True, on_delete=models.CASCADE)
    id_dnevnik = models.CharField(verbose_name=_('ID системы Дневник.РУ'), max_length=40, blank=True, null=True)
    position = models.CharField(max_length=255, verbose_name=_("Должность"), blank=True, null=True)
    admin = models.BooleanField(verbose_name=_("Администрация"), null=True, default=False)
    class Meta:
        verbose_name = 'Профиль учителя'
        verbose_name_plural = 'Профили учителей'
        ordering = ['user']
    def __str__(self):
        return '{}'.format(self.user)

    