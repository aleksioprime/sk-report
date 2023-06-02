from django.db import models
from django.utils.translation import ugettext_lazy as _


GRADES = { 1: [3, 5, 7], 2: [6, 10, 14], 3: [8, 14, 20], 4: [11, 19, 28] }

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
                                   null=True, blank=True, related_name="group")
    # class_year = models.PositiveSmallIntegerField(verbose_name=_("Год обучения"), default=1)
    class_year = models.ForeignKey('curriculum.ClassYear', verbose_name=_("Год обучения"),
                                      on_delete=models.SET_NULL, null=True, related_name="group")
    letter = models.CharField(max_length=1, verbose_name=_("Литера класса"), null=True, blank=True)
    id_dnevnik = models.CharField(max_length=255, verbose_name=_('ID системы Дневник.РУ'), blank=True, null=True)
    students = models.ManyToManyField('member.ProfileStudent', verbose_name=_("Студенты"), blank=True, related_name="groups")
    mentor = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Наставник"), related_name='groups', null=True, blank=True, on_delete=models.SET_NULL)
    psychologist = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Психолог"), related_name='psycho_groups', null=True, blank=True, on_delete=models.SET_NULL)
    class Meta:
        verbose_name = 'Учебный класс'
        verbose_name_plural = 'Учебные классы'
        ordering = ['class_year', 'letter']
    @property
    def count(self):
        return self.students.count
    @property
    def group_name(self):
        return f"{self.class_year.year_rus}{self.letter}"
    def __str__(self):
        return "{}{} класс".format(self.class_year, self.letter)
    
class WorkLoad(models.Model):
    """ Преподавательская нагрузка """
    study_year = models.ForeignKey('assess.StudyYear', verbose_name=_("Учебный год"), 
                                   on_delete=models.CASCADE,
                                   null=True, blank=True, related_name="workload")
    teacher = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Учитель"), on_delete=models.CASCADE,
                              null=True, blank=True, related_name="workload")
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.CASCADE,
                                      null=True, blank=True, related_name="workload")
    # group = models.ForeignKey('assess.ClassGroup', verbose_name=_("Класс"), on_delete=models.CASCADE,
    #                           null=True, blank=True, related_name="workload")
    groups = models.ManyToManyField('assess.ClassGroup', verbose_name=_("Классы"), blank=True, related_name="workload")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Часы"), default=1)
    class Meta:
        verbose_name = 'Рабочая нагрузка'
        verbose_name_plural = 'Рабочие нагрузки'
        ordering = ['study_year', 'subject', 'groups__class_year', 'teacher']
    def __str__(self):
        return '{} ({} - {} ч.)'.format(self.teacher, self.subject, self.hours)

class StudyPeriod(models.Model):
    """ Учебные периоды в году """
    PERIOD_TYPE = [
        ('trimester', 'триместр'),
        ('halfyear', 'полугодие'),
    ]
    study_year = models.ForeignKey('assess.StudyYear', verbose_name=_("Учебный год"), on_delete=models.SET_NULL, \
        null=True, blank=True, related_name="period")
    number = models.PositiveSmallIntegerField(verbose_name=_("Номер периода"), default=1)
    type = models.CharField(max_length=16, choices=PERIOD_TYPE, verbose_name=_("Тип периода"))
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    id_dnevnik = models.CharField(max_length=255, verbose_name=_('ID системы Дневник.РУ'), blank=True, null=True)
    class_year = models.ManyToManyField('curriculum.ClassYear', verbose_name=_("Год обучения"), blank=True, related_name="period")
    @property
    def days(self):
        days = abs((self.date_end - self.date_start).days)
        return "{} дней".format(days)
    class Meta:
        verbose_name = 'Учебный период'
        verbose_name_plural = 'Учебные периоды'
        ordering = ['study_year', 'type', 'number']
    def __str__(self):
        return "{} | {} {}".format(self.study_year, self.number, self.get_type_display())

class SummativeWork(models.Model):
    """ Итоговые работы: основная информация """
    title = models.CharField(max_length=255, verbose_name=_("Название итоговой работы"))
    unit = models.ForeignKey('curriculum.UnitPlannerMYP', verbose_name=_("Юнит"), on_delete=models.SET_NULL,
                                null=True, related_name="sumwork")
    period = models.ForeignKey('assess.StudyPeriod', verbose_name=_("Период обучения"), on_delete=models.SET_NULL,
                               null=True, related_name="sumwork")
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Учебный предмет"), on_delete=models.SET_NULL,
                                null=True, blank=False, related_name="sumwork")
    teacher = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Учитель"), on_delete=models.SET_NULL,
                                null=True, related_name="sumwork")
    groups = models.ManyToManyField('assess.ClassGroup', verbose_name=_("Классы"), through='assess.WorkGroupDate',
                                          blank=True, related_name="sumwork")
    criteria = models.ManyToManyField('curriculum.Criterion', verbose_name=_("Критерии оценки"),
                                      blank=True, related_name="sumwork")
    class Meta:
        verbose_name = 'ИР: Основаная информация'
        verbose_name_plural = 'ИР: Основная информация'
        ordering = ['period', 'subject', 'title']
    def __str__(self):
        return '{}: {}'.format(self.subject, self.title)
    
class WorkGroupDate(models.Model):
    """ Даты итоговых работ """
    work = models.ForeignKey('assess.SummativeWork', verbose_name=_("Итоговая работа"), on_delete=models.CASCADE, null=True, related_name="workgroup")
    group = models.ForeignKey('assess.ClassGroup', verbose_name=_("Класс"), on_delete=models.CASCADE, blank=True, related_name="workgroup")
    date = models.DateField(verbose_name=_("Дата проведения"))
    lesson = models.PositiveSmallIntegerField(verbose_name=_("Номер урока"), default=1)
    students = models.ManyToManyField('member.ProfileStudent', verbose_name=_("Оценки студентов"), through='assess.WorkAssessment', blank=True, related_name="workgroup")
    class Meta:
        verbose_name = 'ИР: Классы'
        verbose_name_plural = 'ИР: Классы'
        ordering = ['work', 'group', 'date']
    def __str__(self):
        return '{} - {} ({})'.format(self.work, self.group, self.date)
    
class WorkAssessment(models.Model):
    """ Журналы оценок по итоговым работам """
    work_date = models.ForeignKey('assess.WorkGroupDate', verbose_name=_("Дата итоговой работы"), on_delete=models.CASCADE, null=True, related_name="workassess")
    student = models.ForeignKey('member.ProfileStudent', verbose_name=_("Студент"), on_delete=models.SET_NULL, null=True, related_name="workassess")
    criteria_marks = models.ManyToManyField('curriculum.Criterion', through='assess.WorkCriteriaMark', blank=True, related_name="workassess")
    grade = models.SmallIntegerField(verbose_name=_("Оценка"), default=0)
    class Meta:
        verbose_name = 'ИР: Журналы'
        verbose_name_plural = 'ИР: Журналы'
        ordering = ['work_date', 'student']
    def __str__(self):
        return '{} - {}'.format(self.work_date, self.student)

class WorkCriteriaMark(models.Model):
    """ Выбор критериев в журнале итоговых работ для выставление баллов студенту"""
    work_assess = models.ForeignKey('assess.WorkAssessment', verbose_name=_("Позиция оценки в юните"), on_delete=models.CASCADE,
                                null=True, related_name="work_criteria_mark")
    criterion = models.ForeignKey('curriculum.Criterion', verbose_name=_("Критерий оценки"), on_delete=models.SET_NULL,
                             null=True, related_name="work_criteria_mark")
    mark = models.SmallIntegerField(verbose_name=_("Оценка по критерию"), default=0)
    class Meta:
        verbose_name = 'ИР: Оценки по критериям'
        verbose_name_plural = 'ИР: Оценки по критериям'
        ordering = ['work_assess', 'criterion']
    def __str__(self):
        return '{}: {} ({})'.format(self.work_assess, self.criterion, self.mark)
    
class PeriodAssessment(models.Model):
    """ Журналы оценок за учебный период """
    student = models.ForeignKey('member.ProfileStudent', verbose_name=_("Студент"), on_delete=models.SET_NULL, null=True, related_name="periodassess")
    period = models.ForeignKey('assess.StudyPeriod', verbose_name=_("Период"), on_delete=models.SET_NULL, null=True, related_name="periodassess")
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.SET_NULL, null=True, related_name="periodassess")
    year = models.ForeignKey('curriculum.ClassYear', verbose_name=_("Год обучения"), on_delete=models.SET_NULL, null=True, related_name="periodassess")
    criterion_a = models.SmallIntegerField(verbose_name=_("Оценка по критерию A"), default=None, null=True, blank=True)
    criterion_b = models.SmallIntegerField(verbose_name=_("Оценка по критерию B"), default=None, null=True, blank=True)
    criterion_c = models.SmallIntegerField(verbose_name=_("Оценка по критерию C"), default=None, null=True, blank=True)
    criterion_d = models.SmallIntegerField(verbose_name=_("Оценка по критерию D"), default=None, null=True, blank=True)
    summ_grade = models.SmallIntegerField(verbose_name=_("Оценка за итоговые работы"), default=None, null=True, blank=True)
    form_grade = models.DecimalField(verbose_name=_("Оценка за текущие работы"), max_digits=3, decimal_places=2, default=None, null=True, blank=True)
    final_grade = models.SmallIntegerField(verbose_name=_("Итоговая оценка"), default=None, blank=True, null=True)
    class Meta:
        verbose_name = 'Итоговые оценки за период'
        verbose_name_plural = 'Итоговые оценки за период'
        ordering = ['period', 'student']
    def __str__(self):
        return '{} - {}'.format(self.period, self.student)
    @property
    def summ_criterion(self):
        return sum([x for x in [self.criterion_a, self.criterion_b, self.criterion_c, self.criterion_d] if isinstance(x, int)])
        # return self.criterion_a + self.criterion_b + self.criterion_c + self.criterion_d
    @property
    def count_criterion(self):
        return len([x for x in [self.criterion_a, self.criterion_b, self.criterion_c, self.criterion_d] if  x is not None])
    @property
    def prediction_criterion(self):
        if self.criterion_count not in GRADES:
            return "N/A"
        if self.summ_criterion >= GRADES[self.count_criterion][2]:
            return 5
        elif self.summ_criterion < GRADES[self.count_criterion][2] and self.summ_criterion >= GRADES[self.count_criterion][1]:
            return 4
        elif self.summ_criterion < GRADES[self.count_criterion][1] and self.summ_criterion >= GRADES[self.count_criterion][0]:
            return 3
        elif self.summ_criterion < GRADES[self.count_criterion][0] and self.summ_criterion > 0:
            return 2
        else:
            return '-'

class ReportPeriod(models.Model):
    """ Периоды для заполнения репортов в году """
    study_year = models.ForeignKey('assess.StudyYear', verbose_name=_("Учебный год"), on_delete=models.SET_NULL, \
        null=True, blank=True, related_name="report_period")
    number = models.PositiveSmallIntegerField(verbose_name=_("Номер периода"), default=1)
    name = models.CharField(max_length=255, verbose_name=_("Название периода"), default=None, null=True)
    assessment_periods = models.ManyToManyField('assess.StudyPeriod', verbose_name=_("Оценочные периоды"), blank=True, related_name="report_period")
    date_start = models.DateField(verbose_name=_("Дата начала"))
    date_end = models.DateField(verbose_name=_("Дата окончания"))
    @property
    def days(self):
        days = abs((self.date_end - self.date_start).days)
        return "{} дней".format(days)
    class Meta:
        verbose_name = 'Период репортов'
        verbose_name_plural = 'Периоды репортов'
        ordering = ['study_year', 'number']
    def __str__(self):
        return "{} период ({})".format(self.number, self.study_year)
    
class ReportTeacher(models.Model):
    """ Репорты учителя """
    student = models.ForeignKey('member.ProfileStudent', verbose_name=_("Студент"), on_delete=models.SET_NULL, null=True, related_name="teacher_reports")
    period = models.ForeignKey('assess.ReportPeriod', verbose_name=_("Период репорта"), on_delete=models.SET_NULL, null=True, related_name="teacher_reports")
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.SET_NULL, null=True, related_name="teacher_reports")
    year = models.ForeignKey('curriculum.ClassYear', verbose_name=_("Год обучения"), on_delete=models.SET_NULL, null=True, related_name="teacher_reports")
    text = models.TextField(verbose_name=_("Текст репорта"), null=True, blank=True)
    events = models.ManyToManyField('assess.EventParticipation', verbose_name=_("Участие в мероприятиях"), blank=True, related_name="teacher_reports")
    author = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Автор репорта"), on_delete=models.SET_NULL, null=True, related_name="teacher_reports")
    achievements = models.ManyToManyField('assess.ReportAchievements', verbose_name=_("Уровни достижений"), blank=True, related_name="teacher_reports")
    criterion_a = models.SmallIntegerField(verbose_name=_("Оценка по критерию A"), default=None, null=True, blank=True)
    criterion_b = models.SmallIntegerField(verbose_name=_("Оценка по критерию B"), default=None, null=True, blank=True)
    criterion_c = models.SmallIntegerField(verbose_name=_("Оценка по критерию C"), default=None, null=True, blank=True)
    criterion_d = models.SmallIntegerField(verbose_name=_("Оценка по критерию D"), default=None, null=True, blank=True)
    criteria = models.ManyToManyField('curriculum.Criterion', verbose_name=_("Критерии "), through='assess.ReportCriteria', blank=True, related_name="teacher_reports")
    final_grade = models.SmallIntegerField(verbose_name=_("Итоговая оценка по шкале 1-5"), default=None, null=True, blank=True)
    final_grade_ib = models.SmallIntegerField(verbose_name=_("Итоговая оценка по шкале 1-7"), default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Дата и время создания"))
    updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Дата и время редактирования"))
    class Meta:
        verbose_name = 'Репорт учителя'
        verbose_name_plural = 'Репорты учителя'
        ordering = ['period', 'subject__name_rus', 'author']
    def __str__(self):
        return '{} - {}'.format(self.period, self.student)
    @property
    def criterion_summ(self):
        return sum([item.report_criteria.filter(report_teacher=self.id).first().mark for item in self.criteria.all()])
        # return sum([x for x in [self.criterion_a, self.criterion_b, self.criterion_c, self.criterion_d] if isinstance(x, int)])
        # return self.criterion_a + self.criterion_b + self.criterion_c + self.criterion_d
    @property
    def criterion_count(self):
        return len(self.criteria.all())
        # return len([x for x in [self.criterion_a, self.criterion_b, self.criterion_c, self.criterion_d] if x is not None])
    @property
    def criterion_rus(self):
        if self.criterion_count not in GRADES:
            return "N/A"
        if self.criterion_summ >= GRADES[self.criterion_count][2]:
            return 5
        elif self.criterion_summ < GRADES[self.criterion_count][2] and self.criterion_summ >= GRADES[self.criterion_count][1]:
            return 4
        elif self.criterion_summ < GRADES[self.criterion_count][1] and self.criterion_summ >= GRADES[self.criterion_count][0]:
            return 3
        elif self.criterion_summ < GRADES[self.criterion_count][0] and self.criterion_summ > 0:
            return 2
        else:
            return '-'

class ReportAchievements(models.Model):
    """ Выбор уровней достижений и их предметных целей в репортах"""
    objective = models.ForeignKey('curriculum.Objective', verbose_name=_("Предметная цель"), on_delete=models.CASCADE, null=True, related_name="report_achievements")
    achievement = models.ForeignKey('curriculum.AchievementLevel', verbose_name=_("Уровень достижений"), on_delete=models.CASCADE, blank=True, null=True, related_name="report_achievements")
    class Meta:
        verbose_name = 'Репорты: уровнень достижений'
        verbose_name_plural = 'Репорты: уровни достижений'
        ordering = ['objective']
    def __str__(self):
        return '{}: {}'.format(self.objective, self.achievement)

class ReportCriteria(models.Model):
    """ Выбор критериев и выставление баллов в репортах """
    report_teacher = models.ForeignKey('assess.ReportTeacher', verbose_name=_("Репорт учителя"), on_delete=models.CASCADE, null=True, related_name="report_criteria")
    criterion = models.ForeignKey('curriculum.Criterion', verbose_name=_("Критерий оценки"), on_delete=models.SET_NULL, null=True, related_name="report_criteria")
    mark = models.SmallIntegerField(verbose_name=_("Балл по критерию"), default=None, null=True)
    class Meta:
        verbose_name = 'Репорты: баллы за критерии'
        verbose_name_plural = 'Репорты: баллы за критерии'
        ordering = ['report_teacher__student', 'criterion']
    def __str__(self):
        return '{}: {} ({})'.format(self.report_teacher, self.criterion, self.mark)

class ReportMentor(models.Model):
    """ Репорты наставника """
    student = models.ForeignKey('member.ProfileStudent', verbose_name=_("Студент"), on_delete=models.SET_NULL, null=True, related_name="mentor_reports")
    period = models.ForeignKey('assess.ReportPeriod', verbose_name=_("Период репорта"), on_delete=models.SET_NULL, null=True, related_name="mentor_reports")
    year = models.ForeignKey('curriculum.ClassYear', verbose_name=_("Год обучения"), on_delete=models.SET_NULL, null=True, related_name="mentor_reports")
    events = models.ManyToManyField('assess.EventParticipation', verbose_name=_("Участие в мероприятиях"), blank=True, related_name="mentor_reports")
    text = models.TextField(verbose_name=_("Текст репорта"), null=True, blank=True)
    author = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Автор репорта"), on_delete=models.SET_NULL, null=True, related_name="mentor_reports")
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Дата и время создания"))
    updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Дата и время редактирования"))
    class Meta:
        verbose_name = 'Репорт наставника'
        verbose_name_plural = 'Репорты наставника'
        ordering = ['period', 'student']
    def __str__(self):
        return '{} - {}'.format(self.period, self.student)

class ReportPsychologist(models.Model):
    """ Репорты психолога """
    student = models.ForeignKey('member.ProfileStudent', verbose_name=_("Студент"), on_delete=models.SET_NULL, null=True, related_name="psycho_reports")
    period = models.ForeignKey('assess.ReportPeriod', verbose_name=_("Период репорта"), on_delete=models.SET_NULL, null=True, related_name="psycho_reports")
    year = models.ForeignKey('curriculum.ClassYear', verbose_name=_("Год обучения"), on_delete=models.SET_NULL, null=True, related_name="psycho_reports")
    text = models.TextField(verbose_name=_("Текст репорта"), null=True, blank=True)
    events = models.ManyToManyField('assess.EventParticipation', verbose_name=_("Участие в мероприятиях"), blank=True, related_name="psycho_reports")
    author = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Автор репорта"), on_delete=models.SET_NULL, null=True, related_name="psycho_reports")
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Дата и время создания"))
    updated = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Дата и время редактирования"))
    class Meta:
        verbose_name = 'Репорт психолога'
        verbose_name_plural = 'Репорты психолога'
        ordering = ['period', 'student']
    def __str__(self):
        return '{} - {}'.format(self.period, self.student)

class EventType(models.Model):
    """ Типы мероприятий """
    name = models.CharField(max_length=255, verbose_name=_("Название типа"))
    description = models.TextField(verbose_name=_("Описание типа"), null=True, blank=True)
    class Meta:
        verbose_name = 'Тип мероприятий'
        verbose_name_plural = 'Типы мероприятий'
        ordering = ['name']
    def __str__(self):
        return '{}'.format(self.name)

class EventParticipation(models.Model):
    """ Участие в мероприятиях """
    LEVEL_CHOICES = [
        ('1', '1 уровень'),
        ('2', '2 уровень'),
        ('3', '3 уровень'),
        ('0', 'Без уровня'),
    ]
    title = models.CharField(max_length=255, verbose_name=_("Название мероприятия"))
    level =  models.CharField(max_length=16, choices=LEVEL_CHOICES, verbose_name=_("Уровень мероприятий"), default='0')
    type = models.ForeignKey('assess.EventType', verbose_name=_("Тип мероприятия"), on_delete=models.SET_NULL, blank=True, null=True, related_name="events")
    result = models.TextField(verbose_name=_("Описание результатов"), null=True, blank=True)
    comment = models.TextField(verbose_name=_("Комментарии"), null=True, blank=True)
    class Meta:
        verbose_name = 'Участие в мероприятиях'
        verbose_name_plural = 'Участия в мероприятиях'
        ordering = ['type']
    def __str__(self):
        return '{} {}'.format(self.type, self.title)
