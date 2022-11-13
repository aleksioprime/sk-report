from django.db import models
from django.utils.translation import ugettext_lazy as _

class StudyYear(models.Model):
    """ Учебные года """
    name = models.CharField(max_length=32, verbose_name=_("Учебный год"))
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    class Meta:
        verbose_name = 'Учебный год'
        verbose_name_plural = 'Учебные года'
        ordering = ['date_start']
    def __str__(self):
        return "{}".format(self.name)

class ClassGroup(models.Model):
    """ Учебные классы """
    study_year = models.ForeignKey('assess.StudyYear', verbose_name=_("Учебный год"), on_delete=models.CASCADE, 
                                   null=True, blank=True, related_name="classgroup")
    class_year = models.PositiveSmallIntegerField(verbose_name=_("Год обучения"), default=1)
    letter = models.CharField(max_length=1, verbose_name=_("Литера класса"), null=True, blank=True)
    id_dnevnik = models.CharField(max_length=255, verbose_name=_('ID системы Дневник.РУ'), blank=True, null=True)
    class Meta:
        verbose_name = 'Учебный класс'
        verbose_name_plural = 'Учебные классы'
        ordering = ['class_year', 'letter']
    def __str__(self):
        return "{}{} класс".format(self.class_year, self.letter)
