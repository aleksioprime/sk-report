from django.db import models
from django.utils.translation import gettext as _

class SubjectGroupIB(models.Model):
    """ Предметные группы IB """
    PROGRAM_TYPE = [
        ('PYP', 'Primary Years Programme'),
        ('MYP', 'Middle Years Programme'),
        ('DP', 'Diploma Programme'),
        ('FGOS', 'ФГОС'),
    ]
    name_eng = models.CharField(max_length=128, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=128, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    picture = models.ImageField(upload_to='subjectgroup_pic', blank=True, verbose_name=_("Картинка"), null=True)
    program = models.CharField(choices=PROGRAM_TYPE, default='FGOS', max_length=4)
    class Meta:
        verbose_name = 'Предметная группа IB'
        verbose_name_plural = 'Предметные группы IB'
        ordering = ['program', 'id']
    def __str__(self):
        return "{} - {}".format(self.name_eng, self.program)

class ClassYear(models.Model):
    """ Года обучения / учебная параллель """
    PROGRAM_TYPE = [
        ('PYP', 'Primary Years Programme'),
        ('MYP', 'Middle Years Programme'),
        ('DP', 'Diploma Programme'),
        ('FGOS', 'ФГОС'),
    ]
    year_rus = models.PositiveIntegerField(verbose_name=_("Год обучения в РФ"), blank=False)
    year_ib = models.CharField(max_length=12, verbose_name=_("Год обучения в IB"), null=True, blank=True)
    program = models.CharField(choices=PROGRAM_TYPE, default='FGOS', max_length=4)
    class Meta:
        verbose_name = 'Год обучения'
        verbose_name_plural = 'Года обучения'
    def __str__(self):
        if self.year_ib is not None:
            return "{} {} ({} класс)".format(self.program, self.year_ib, self.year_rus)
        else:
            return "{} класс ({})".format(self.year_rus, self.program)

class SubjectGroupFGOS(models.Model):
    """ Предметная группа ФГОС """
    LEVEL_CHOICES = [
        ('noo', 'Начальная школа'),
        ('ooo', 'Средняя школа'),
        ('soo', 'Старшая школа'),
        ('dpsoo', 'DP в старшей школе')
    ]
    TYPE_CHOICES = [
        ('area', 'Предметная область'),
        ('direction', 'Направление'),
    ]
    name_rus = models.CharField(max_length=128, verbose_name=_("Название на рус. языке"))
    type_group = models.CharField(choices=TYPE_CHOICES, max_length=9, default='area', verbose_name=_("Тип группы"))
    level = models.CharField(choices=LEVEL_CHOICES, default='ooo', max_length=5, verbose_name=_("Уровень образования"))
    class Meta:
        verbose_name = 'Предметная группа ФГОС'
        verbose_name_plural = 'Предметные группы ФГОС'
        ordering = ['level', 'type_group', 'name_rus']
    def __str__(self):
        return "{} ({})".format(self.name_rus, self.level)

class Subject(models.Model):
    """ Учебные дисциплины """
    TYPE_CHOICES = [
        ('base', 'Обязательная часть'),
        ('extra', 'Внеурочная деятельность'),
    ]
    name_rus = models.CharField(max_length=128, verbose_name=_("Название на рус. языке"))
    name_eng = models.CharField(max_length=128, verbose_name=_("Название на англ. языке"), null=True, blank=True)
    group_ib = models.ForeignKey('curriculum.SubjectGroupIB', verbose_name=_("Предметная группа в IB"), 
                                 on_delete=models.SET_NULL, null=True, blank=True, related_name="subject")
    group_fgos = models.ForeignKey('curriculum.SubjectGroupFGOS', verbose_name=_("Предметная область в РФ"), 
                                 on_delete=models.SET_NULL, null=True, blank=True, related_name="subject")
    type_subject = models.CharField(choices=TYPE_CHOICES, max_length=5, default='base', verbose_name=_("Тип предмета"))
    id_dnevnik = models.CharField(verbose_name=_('ID системы Дневник.РУ'), max_length=40, blank=True, null=True)
    department = models.ForeignKey('member.Department', verbose_name=_("Учебное подразделение"), 
                                 on_delete=models.SET_NULL, null=True, blank=True, related_name="subject")
    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['group_ib', 'name_eng']
    def __str__(self):
        return "{} ({})".format(self.name_rus, self.group_fgos.get_level_display())

class AcademicPlan(models.Model):
    """ Учебный план """
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"),
                                      on_delete=models.CASCADE,
                                      null=True, blank=True, related_name="plan")
    class_year = models.ForeignKey('curriculum.ClassYear', verbose_name=_("Год обучения"),
                                        on_delete=models.CASCADE,
                                        null=True, blank=True, related_name="plan")
    study_year = models.ForeignKey('assess.StudyYear', verbose_name=_("Учебный год"), 
                                   on_delete=models.CASCADE,
                                   null=True, blank=True, related_name="plan")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Кол-во часов"), default=1)
    class Meta:
        verbose_name = 'Учебный план'
        verbose_name_plural = 'Учебные планы'
        ordering = ['subject', 'class_year']
    def __str__(self):
        return "{} ({})".format(self.subject, self.class_year)

class Criterion(models.Model):
    """ Критерии оценивания """
    CRITERION_LETTER = [
        ('A', 'Критерий A'),
        ('B', 'Критерий B'),
        ('C', 'Критерий C'),
        ('D', 'Критерий D'),
    ]
    letter = models.CharField(choices=CRITERION_LETTER, max_length=1)
    name_eng = models.CharField(max_length=255, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    description_eng = models.TextField(verbose_name=_("Описание на англ. языке"), null=True, blank=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    subject_group = models.ForeignKey('curriculum.SubjectGroupIB', verbose_name=_("Предметная группа"), on_delete=models.SET_NULL, \
        null=True, blank=False, related_name="criterion")
    class Meta:
        verbose_name = 'Критерий оценивания'
        verbose_name_plural = 'Критерии оценивания'
        ordering = ['subject_group', 'letter']
    def __str__(self):
        return "{} | {}".format(self.letter, self.subject_group)
    
    
class Strand(models.Model):
    """ Стрэнды - аспекты образовательных достижений """
    STRAND_LETTER = [
        (1, 'i'),
        (2, 'ii'),
        (3, 'iii'),
        (4, 'iv'),
        (5, 'v'),
    ]
    number = models.PositiveIntegerField(verbose_name=_("Абсолютный номер"), default=1)
    letter = models.PositiveIntegerField(choices=STRAND_LETTER, verbose_name=_("Метка в критерии"), default=1)
    name_eng = models.CharField(max_length=255, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    criterion = models.ForeignKey('curriculum.Criterion', verbose_name=_("Критерий"), on_delete=models.SET_NULL, \
        null=True, blank=False, related_name="strand")
    class Meta:
        verbose_name = 'Стрэнд'
        verbose_name_plural = 'Стрэнды'
        ordering = ['criterion', 'number', 'letter']
    def __str__(self):
        return "{} ({}). {}... | {}".format(self.number, self.get_letter_display(), self.name_eng[:15], self.criterion)
    
    
class Level(models.Model):
    """ Образовательный уровень """
    name_eng = models.CharField(max_length=255, verbose_name=_("Название на англ. языке"), null=True, blank=False)
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    subject_groups = models.ManyToManyField('curriculum.SubjectGroupIB',
                                                  verbose_name=_("Предметные группы"), blank=True,
                                                  related_name="level")
    class Meta:
        verbose_name = 'Образовательный уровень'
        verbose_name_plural = 'Образовательные уровни'
        ordering = ['name_eng']
    def __str__(self):
        return "{}".format(self.name_eng)

class Objective(models.Model):
    """ Образовательные цели """
    level = models.ForeignKey('curriculum.Level', verbose_name=_("Уровень в IB"), on_delete=models.SET_NULL, \
        null=True, blank=False, related_name="objective")
    strand = models.ForeignKey('curriculum.Strand', verbose_name=_("Стрэнд"), on_delete=models.SET_NULL, \
        null=True, blank=False, related_name="objective")
    name_eng = models.CharField(max_length=255,verbose_name=_("Описание на англ. языке"), null=True, blank=False)
    name_rus = models.CharField(max_length=255,verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    class Meta:
        verbose_name = 'Образовательная цель'
        verbose_name_plural = 'Образовательные цели'
        ordering = ['level', 'strand']
    def __str__(self):
        return "{} | {}. {}...".format(self.level, self.strand.letter, self.name_eng[:10])

class AchievementLevel(models.Model):
    """ Уровни достижений образовательных целей """
    objective = models.ForeignKey('curriculum.Objective', verbose_name=_("Образовательная цель"), on_delete=models.CASCADE, \
        null=True, blank=False, related_name="achievelevel")
    name_eng = models.TextField(verbose_name=_("Описание на англ. языке"), null=True, blank=False)
    name_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    point = models.PositiveIntegerField(verbose_name=_("Баллы"), default=0)
    class Meta:
        verbose_name = 'Уровень достижений'
        verbose_name_plural = 'Уровни достижений'
        ordering = ['objective', 'point']
    def __str__(self):
        return "{}... - {}".format(self.name_eng[:30], self.point)
    
class KeyConcept(models.Model):
    """ Ключевые концепты """
    name_eng = models.CharField(max_length=32, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=32, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    description_eng = models.TextField(verbose_name=_("Описание на англ. языке"), null=True, blank=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    recommended_subjects = models.ManyToManyField('curriculum.SubjectGroupIB',
                                                  verbose_name=_("Рекомендуемые предметные группы"),
                                                  through='curriculum.RecommendSubjectKC', blank=True,
                                                  related_name="key_concept")
    class Meta:
        verbose_name = 'KC: Ключевой концепт'
        verbose_name_plural = 'KC: Ключевые концепты'
        ordering = ['name_eng']
    def __str__(self):
        return "{}".format(self.name_eng)

class RecommendSubjectKC(models.Model):
    """ Рекомендуемые предметы для ключевых концептов с описанием """
    key_concept = models.ForeignKey('curriculum.KeyConcept', verbose_name=_("Ключевой концепт"), on_delete=models.SET_NULL,
                                null=True, related_name="recomend_subject")
    subject_group = models.ForeignKey('curriculum.SubjectGroupIB', verbose_name=_("Предметная группа"), on_delete=models.SET_NULL,
                             null=True, related_name="recomend_subject")
    comment_eng = models.TextField(verbose_name=_("Комментарии на англ. языке"), null=True, blank=True)
    comment_rus = models.TextField(verbose_name=_("Комментарии на рус. языке"), null=True, blank=True)
    class Meta:
        verbose_name = 'KC: Рекомендуемый предмет'
        verbose_name_plural = 'KC: Рекомендуемые предметы'
        ordering = ['subject_group', 'key_concept']
        
class SubjectDirectionRC(models.Model):
    """ Предметные направления """
    name_eng = models.CharField(max_length=128, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=128, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    subject_group = models.ForeignKey('curriculum.SubjectGroupIB', verbose_name=_("Предметная группа"), on_delete=models.SET_NULL, \
        null=True, blank=True, related_name="connect_subjectrc")
    class Meta:
        verbose_name = 'RC: Предметное направление'
        verbose_name_plural = 'RC: Предметные направления'
        ordering = ['id', 'name_eng']
    def __str__(self):
        return "{}".format(self.name_eng)
    
class RelatedConcept(models.Model):
    """ Сопутствующие концепты """
    name_eng = models.CharField(max_length=64, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    description_eng = models.TextField(verbose_name=_("Описание на англ. языке"), null=True, blank=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    subject_directions = models.ManyToManyField('curriculum.SubjectDirectionRC', verbose_name=_("Предметное направление"), related_name="related_concept")
    class Meta:
        verbose_name = 'RC: Предметный концепт'
        verbose_name_plural = 'RC: Предметные концепты'
        ordering = ['id', 'name_eng']
    def __str__(self):
        return "{}".format(self.name_eng)
    
class GlobalContext(models.Model):
    """ Глобальные контексты """
    name_eng = models.CharField(max_length=64, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    description_eng = models.TextField(verbose_name=_("Описание на англ. языке"), null=True, blank=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    focus_questions_eng = models.CharField(max_length=255, verbose_name=_("Вопросы на англ. языке"), null=True, blank=True)
    focus_questions_rus = models.CharField(max_length=255, verbose_name=_("Вопросы на рус. языке"), null=True, blank=True)
    class Meta:
        verbose_name = 'GC: Глобальный контекст'
        verbose_name_plural = 'GC: Глобальные контексты'
        ordering = ['id']
    def __str__(self):
        return "{}".format(self.name_eng)

class ExplorationToDevelop(models.Model):
    """ Линии исследования """
    name_eng = models.CharField(max_length=64, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    gcontext = models.ForeignKey('curriculum.GlobalContext', verbose_name=_("Глобальный контекст"), on_delete=models.CASCADE, \
        null=True, blank=False, related_name="exploration")
    class Meta:
        verbose_name = 'GC: Линия исследования'
        verbose_name_plural = 'GC: Линии исследований'
        ordering = ['gcontext', 'name_eng']
    def __str__(self):
        return "{} ({})".format(self.name_eng, self.gcontext)

class CategoryATL(models.Model):
    """ Категории ATL """
    name_eng = models.CharField(max_length=64, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    class Meta:
        verbose_name = 'ATL: Категория '
        verbose_name_plural = 'ATL: Категории'
        ordering = ['id']
    def __str__(self):
        return "{}".format(self.name_eng)

class ClusterATL(models.Model):
    """ Кластеры ATL """
    name_eng = models.CharField(max_length=64, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=64, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    category = models.ForeignKey('curriculum.CategoryATL', verbose_name=_("Категория ATL"), on_delete=models.CASCADE, \
        null=True, blank=False, related_name="cluster")
    class Meta:
        verbose_name = 'ATL: Кластер'
        verbose_name_plural = 'ATL: Кластеры'
        ordering = ['category', 'id']
    def __str__(self):
        return "{} ({})".format(self.name_eng, self.category)

class SkillATL(models.Model):
    """ Навыки ATL """
    name_eng = models.CharField(max_length=255, verbose_name=_("Название на англ. языке"))
    name_rus = models.CharField(max_length=255, verbose_name=_("Название на рус. языке"), null=True, blank=True)
    description_eng = models.TextField(verbose_name=_("Описание на англ. языке"), null=True, blank=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    cluster = models.ForeignKey('curriculum.ClusterATL', verbose_name=_("Кластер ATL"), on_delete=models.CASCADE, \
        null=True, blank=False, related_name="skillATL")
    class Meta:
        verbose_name = 'ATL: Навыки'
        verbose_name_plural = 'ATL: Навыки'
        ordering = ['cluster', 'name_eng']
    def __str__(self):
        return "{} ({})".format(self.name_eng, self.cluster)

class Aim(models.Model):
    """ Цели """
    subject_group = models.ForeignKey('curriculum.SubjectGroupIB', verbose_name=_("Предметная группа"), on_delete=models.SET_NULL, null=True, related_name="aim")
    name_eng = models.CharField(max_length=255,verbose_name=_("Название на англ. языке"), null=True, blank=False)
    name_rus = models.CharField(max_length=255,verbose_name=_("Название на рус. языке"), null=True, blank=True)
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        ordering = ['subject_group', 'name_eng']
    def __str__(self):
        return "{} | {}...".format(self.subject_group, self.name_eng[:10])
    
class LearnerProfileIB(models.Model):
    """ Профили студента """
    name_eng = models.CharField(max_length=255,verbose_name=_("Название на англ. языке"), null=True, blank=False)
    name_rus = models.CharField(max_length=255,verbose_name=_("Название на рус. языке"), null=True, blank=True)
    description_eng = models.TextField(verbose_name=_("Описание на англ. языке"), null=True, blank=True)
    description_rus = models.TextField(verbose_name=_("Описание на рус. языке"), null=True, blank=True)
    class Meta:
        verbose_name = 'Профиль студента'
        verbose_name_plural = 'Профили студента'
        ordering = ['name_eng']
    def __str__(self):
        return "{}".format(self.name_eng)
    
class UnitPlannerMYP(models.Model):
    """ ЮнитПланеры MYP """
    # Основная информация о юните
    title = models.CharField(max_length=255, verbose_name=_("Название юнита"))
    subjects = models.ManyToManyField('curriculum.Subject', verbose_name=_("Предметы"), blank=True, related_name="unitplan_myp", through='curriculum.SubjectLevelMYP')
    authors = models.ManyToManyField('member.ProfileTeacher', verbose_name=_("Авторы"), related_name="unitplan_myp")
    order = models.PositiveSmallIntegerField(verbose_name=_("Номер"), default=0)
    # interdisciplinary = models.BooleanField(default=False, verbose_name=_("Междисциплинарный юнит"))
    class_year = models.ForeignKey('curriculum.ClassYear', verbose_name=_("Год обучения"), on_delete=models.SET_NULL, null=True, blank=False, related_name="unitplan_myp")
    hours = models.PositiveSmallIntegerField(verbose_name=_("Кол-во часов"), default=0)
    description = models.TextField(verbose_name=_("Описание"), null=True, blank=True)
    # Информация по Inquiry (Исследовательские вопросы добавляются в связанных таблицах)
    key_concepts = models.ManyToManyField('curriculum.KeyConcept', verbose_name=_("Ключевые концепты"), blank=True, related_name="unitplan_myp")
    related_concepts = models.ManyToManyField('curriculum.RelatedConcept', verbose_name=_("Сопутствующие концепты"), blank=True, related_name="unitplan_myp")
    conceptual_understanding = models.TextField(verbose_name=_("Концептуальное понимание"), null=True, blank=True)
    global_context = models.ForeignKey('curriculum.GlobalContext', verbose_name=_("Глобальный контекст"), on_delete=models.SET_NULL, null=True, blank=True, related_name="unitplan_myp")
    explorations = models.ManyToManyField('curriculum.ExplorationToDevelop', verbose_name=_("Линии исследования"), blank=True, related_name="unitplan_myp")
    statement_inquiry = models.TextField(verbose_name=_("Формулировка исследования"), null=True, blank=True)
    # Образовательные цели   
    aims = models.ManyToManyField('curriculum.Aim', verbose_name=_("Цели"), blank=True, related_name="unitplan_myp")
    strands = models.ManyToManyField('curriculum.Strand', verbose_name=_("Стренды предметной группы"), blank=True, related_name="unitplan_myp")
    content = models.TextField(verbose_name=_("Содержание (темы, знания и умения)"), null=True, blank=True)
    skills = models.TextField(verbose_name=_("Умения"), null=True, blank=True)
    learner_profile = models.ManyToManyField('curriculum.LearnerProfileIB',verbose_name=_("Профиль студента"), blank=True, related_name="unitplan_myp")
    description_lp = models.TextField(verbose_name=_("Описание развития профиля"), null=True, blank=True)
    international_mindedness = models.TextField(verbose_name=_("Межкультурное понимание"), null=True, blank=True)
    academic_integrity = models.TextField(verbose_name=_("Академическая честность"), null=True, blank=True)
    language_development = models.TextField(verbose_name=_("Языковое развитие"), null=True, blank=True)
    infocom_technology = models.TextField(verbose_name=_("Использование средств ИКТ"), null=True, blank=True)
    service_as_action = models.TextField(verbose_name=_("Служение как действие"), null=True, blank=True)
    # Оценивание по юниту
    criteria = models.ManyToManyField('curriculum.Criterion', verbose_name=_("Критерии оценки"), blank=True, related_name="unitplan_myp")
    formative_assessment = models.TextField(verbose_name=_("Формирующее оценивание"), null=True, blank=True)
    summative_assessment_task = models.TextField(verbose_name=_("Итоговое оценивание (задачи)"), null=True, blank=True)
    summative_assessment_soi = models.TextField(verbose_name=_("Итоговое оценивание (взаимосвязь с SOI)"), null=True, blank=True)
    peer_self_assessment = models.TextField(verbose_name=_("Взаимное и самооценивание"), null=True, blank=True)
    standardization_moderation = models.TextField(verbose_name=_("Стандартизация и модерация"), null=True, blank=True)
    prior_experiences = models.TextField(verbose_name=_("Предыдущий опыт обучения"), null=True, blank=True)
    learning_experiences = models.TextField(verbose_name=_("Учебная деятельность"), null=True, blank=True)
    teaching_strategies = models.TextField(verbose_name=_("Стратегии преподавания"), null=True, blank=True) 
    student_expectations = models.TextField(verbose_name=_("Ожидания студентов"), null=True, blank=True)
    feedback = models.TextField(verbose_name=_("Обратная связь"), null=True, blank=True)
    differentiation = models.TextField(verbose_name=_("Дифференцированный подход"), null=True, blank=True)
    resources = models.TextField(verbose_name=_("Ресурсы"), null=True, blank=True)
    # Посты обратной связи от педагогов добавляются в связанных таблицах
    class Meta:
        verbose_name = 'UnitPlan MYP: Основные данные юнита'
        verbose_name_plural = 'UnitPlan MYP: Основные данные юнитов'
        ordering = ['class_year', 'order', 'title']
    def __str__(self):
        return "{} ({})".format(self.title, self.class_year)

class SubjectLevelMYP(models.Model):
    """ Промежуточная таблица уровней изучаемых предметов """
    unit = models.ForeignKey('curriculum.UnitPlannerMYP', verbose_name=_("Юнит"), on_delete=models.CASCADE, related_name="subject_unit")
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Предмет"), on_delete=models.CASCADE, related_name="subject_unit")
    level = models.ForeignKey('curriculum.Level', verbose_name=_("Уровень"), on_delete=models.CASCADE, related_name="subject_unit")
    class Meta:
        verbose_name = 'UnitPlan MYP: Выбор предмета и уровня'
        verbose_name_plural = 'UnitPlan MYP: Выборы предметов и уровней'
        ordering = ['unit', 'subject']
    def __str__(self):
        return "{} ({})".format(self.unit, self.subject)
    
    
class UnitPlannerMYPID(models.Model):
    """ Дополнение для междисциплинарных планеров MYP """
    unitplan_myp = models.OneToOneField('curriculum.UnitPlannerMYP', verbose_name=_("ЮнитПланер MYP"), related_name='inter', on_delete=models.CASCADE)
    form_integration = models.TextField(verbose_name=_("Формы интеграции"), null=True, blank=True)
    purpose_integration = models.TextField(verbose_name=_("Цель интеграции"), null=True, blank=True)
    interdisciplinary_links = models.TextField(verbose_name=_("Междисциплинарные связи"), null=True, blank=True)
    inter_criteria = models.ManyToManyField('curriculum.Criterion', verbose_name=_("Критерии оценки"), blank=True, related_name="inter")
    inter_aims = models.ManyToManyField('curriculum.Aim', verbose_name=_("Цели"), blank=True, related_name="inter")
    inter_strands = models.ManyToManyField('curriculum.Strand', verbose_name=_("Образовательные цели"), blank=True, related_name="inter")
    class Meta:
        verbose_name = 'UnitPlan MYP: Междисциплинарность'
        verbose_name_plural = 'UnitPlan MYP: Междисциплинарности'
        ordering = ['unitplan_myp']
    def __str__(self):
        return "{}".format(self.unitplan_myp)
    
class InquiryQuestionMYP(models.Model):
    """ Исследовательские вопросы планеров MYP """
    QUESTION_TYPE = [
        ('Factual', 'Фактический'),
        ('Conceptual', 'Концептуальный'),
        ('Debatable', 'Дискуссионный'),
    ]
    question = models.CharField(max_length=255, verbose_name=_("Исследовательский вопрос"))
    type_inq = models.CharField(choices=QUESTION_TYPE, verbose_name=_("Тип вопроса"), default='Factual', max_length=12)
    line = models.CharField(max_length=255, verbose_name=_("Линия исследования"), null=True, blank=True)
    planner = models.ForeignKey('curriculum.UnitPlannerMYP', verbose_name=_("Планнер MYP"), on_delete=models.CASCADE,
                                related_name="inquestions")
    class Meta:
        verbose_name = 'UnitPlan MYP: Исследовательский вопрос'
        verbose_name_plural = 'UnitPlan MYP: Исследовательские вопросы'
        ordering = ['type_inq', 'question']
    def __str__(self):
        return "{} ({})".format(self.question, self.type_inq)
    
class ATLMappingMYP(models.Model):
    """ Карта навыков в планерах MYP """
    atl = models.ForeignKey('curriculum.SkillATL', verbose_name=_("Навыки ATL"), blank=True, on_delete=models.CASCADE, related_name="atlmapping")
    # objective = models.ForeignKey('curriculum.Objective', verbose_name=_("Предметная цель"), blank=True, on_delete=models.CASCADE, related_name="atlmapping")
    strand = models.ForeignKey('curriculum.Strand', verbose_name=_("Предметный стрэнд"), blank=True, on_delete=models.CASCADE, related_name="atlmapping")
    action = models.TextField(verbose_name=_("Описание учебных действий"), null=True, blank=True)
    planner = models.ForeignKey('curriculum.UnitPlannerMYP', verbose_name=_("Планнер MYP"), on_delete=models.CASCADE,
                                related_name="atlmapping")
    class Meta:
        verbose_name = 'UnitPlan MYP: Карта навыков ATL'
        verbose_name_plural = 'UnitPlan MYP: Карты навыков ATL'
        ordering = ['planner', 'strand']
    def __str__(self):
        return "{} ({})".format(self.atl, self.action)

class ReflectionMYP(models.Model):
    """ Посты рефлексии по планеру MYP """
    POST_TYPE = [
        ('Prior', 'Перед началом юнита'),
        ('During', 'Во время юнита'),
        ('After', 'После окончания юнита'),
    ]
    type_post = models.CharField(choices=POST_TYPE, verbose_name=_("Тип рефлексии"), default='After', max_length=6)
    post = models.TextField(verbose_name=_("Содержание рефлексии"), null=True, blank=True)
    planner = models.ForeignKey('curriculum.UnitPlannerMYP', verbose_name=_("Планнер MYP"), on_delete=models.CASCADE, related_name="reflections")
    author = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Автор поста"), on_delete=models.SET_NULL,
                               null=True, related_name="reflections")
    class Meta:
        verbose_name = 'UnitPlan MYP: Пост рефлексии'
        verbose_name_plural = 'UnitPlan MYP: Посты рефлексии'
        ordering = ['planner', 'type_post']
    def __str__(self):
        return "{}: {}".format(self.type_post, self.planner, self.post[:15])

class UnitPlannerDP(models.Model):
    """ ЮнитПланеры DP """
    LEVEL_TYPE = [
        ('SL', 'Standart Level'),
        ('HL', 'High Level'),
        ('SL+HL', 'Standart + High Level'),
    ]
    # Основная информация о юните
    order = models.PositiveSmallIntegerField(verbose_name=_("Order"), default=0)
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    subject = models.ForeignKey('curriculum.Subject', verbose_name=_("Subject"), on_delete=models.SET_NULL, null=True, blank=False, related_name="unitplan_dp")
    class_year = models.ForeignKey('curriculum.ClassYear', verbose_name=_("Grade"), on_delete=models.SET_NULL, null=True, blank=False, related_name="unitplan_dp")
    levels = models.CharField(choices=LEVEL_TYPE, verbose_name=_("Levels"), default='SL+HL', max_length=5)
    hours = models.PositiveSmallIntegerField(verbose_name=_("Hours"), default=0)
    course_part = models.CharField(max_length=255, verbose_name=_("Course Part"))
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    # Информация по Inquiry (+ Guiding questions)
    transfer_goals = models.TextField(verbose_name=_("Transfer goals"), null=True, blank=True)
    essen_understand = models.TextField(verbose_name=_("Essential Understandings"), null=True, blank=True)
    misunderstand = models.TextField(verbose_name=_("Missed concepts/misunderstandings"), null=True, blank=True)
    # >>> aims >> DataBase
    # >>> objectives >> DataBase
    # >>> syllabus content >> DataBase
    content = models.TextField(verbose_name=_("Content"), null=True, blank=True)
    skills = models.TextField(verbose_name=_("Skills"), null=True, blank=True)
    concepts = models.TextField(verbose_name=_("Concepts"), null=True, blank=True)
    # >>> metacognition >> MultipleChoice + Text
    international_mindedness = models.TextField(verbose_name=_("International Mindedness"), null=True, blank=True)
    academic_integrity = models.TextField(verbose_name=_("Academic Integrity"), null=True, blank=True)
    infocom_technology = models.TextField(verbose_name=_("Information Communication Technology"), null=True, blank=True)
    # >>> language_learning >> MultipleChoice + Text
    # >>> tok_connections >> MultipleChoice + Text
    # >>> cas_connections >> MultipleChoice + Text
    # >>> atl_skills >> DataBase
    description_atl = models.TextField(verbose_name=_("Description ATL"), null=True, blank=True)
    # >> learner_profile >> DataBase
    description_lp = models.TextField(verbose_name=_("Description Learning Profile"), null=True, blank=True)
    formative_assessment = models.TextField(verbose_name=_("Formative assessment"), null=True, blank=True)
    summative_assessment = models.TextField(verbose_name=_("Summative assessment"), null=True, blank=True)
    peer_self_assessment = models.TextField(verbose_name=_("Peer and self assessment"), null=True, blank=True)
    standardization_moderation = models.TextField(verbose_name=_("Standardization and moderation"), null=True, blank=True)
    # >> criteria >> DataBase
    description_criteria = models.TextField(verbose_name=_("Description Criteria"), null=True, blank=True)
    prior_experiences = models.TextField(verbose_name=_("Prior learning experience"), null=True, blank=True)
    pedagogical_approaches = models.TextField(verbose_name=_("Pedagogical approaches"), null=True, blank=True)
    feedback = models.TextField(verbose_name=_("Feedback"), null=True, blank=True)
    student_expectations = models.TextField(verbose_name=_("Student expectations"), null=True, blank=True)
    # >>> support_materials >> MultipleChoice + Text
    # >>> learning_process >> MultipleChoice + Text
    # >>> differentiation >> MultipleChoice + Text
    class Meta:
        verbose_name = 'UnitPlan DP: Основные данные юнита'
        verbose_name_plural = 'UnitPlan DP: Основные данные юнитов'
        ordering = ['class_year', 'subject', 'order', 'title']
    def __str__(self):
        return "{} ({} | {})".format(self.title, self.subject, self.class_year)

class InquiryQuestionDP(models.Model):
    """ Исследовательские вопросы планеров DP """
    QUESTION_TYPE = [
        ('Skills-based', 'Skills-based'),
        ('Content-based', 'Content-based'),
        ('Debatable', 'Debatable'),
        ('Concept-based', 'Concept-based'),
    ]
    question = models.CharField(max_length=255, verbose_name=_("Question"))
    type_inq = models.CharField(choices=QUESTION_TYPE, verbose_name=_("Type"), default='Skills-based', max_length=24)
    planner = models.ForeignKey('curriculum.UnitPlannerDP', verbose_name=_("Planner DP"), on_delete=models.CASCADE,
                                related_name="inquestions")
    class Meta:
        verbose_name = 'UnitPlan DP: Исследовательский вопрос'
        verbose_name_plural = 'UnitPlan DP: Исследовательские вопросы'
        ordering = ['type_inq', 'question']
    def __str__(self):
        return "{} ({})".format(self.question, self.type_inq)

class ReflectionDP(models.Model):
    """ Посты рефлексии по планеру DP """
    POST_TYPE = [
        ('Prior', 'Prior to studying the unit'),
        ('During', 'During the unit'),
        ('Worked Well', 'What worked well'),
        ('Didn’t work well', 'What didn’t work well'),
        ('Transfer reflection', 'Transfer reflection'),        
    ]
    type_post = models.CharField(choices=POST_TYPE, verbose_name=_("Type"), default='Prior', max_length=24)
    post = models.TextField(verbose_name=_("Post"), null=True, blank=True)
    planner = models.ForeignKey('curriculum.UnitPlannerDP', verbose_name=_("Planner DP"), on_delete=models.CASCADE, related_name="reflections")
    author = models.ForeignKey('member.ProfileTeacher', verbose_name=_("Author"), on_delete=models.SET_NULL,
                               null=True, related_name="reflection_dp")
    class Meta:
        verbose_name = 'UnitPlan DP: Пост рефлексии'
        verbose_name_plural = 'UnitPlan DP: Посты рефлексии'
        ordering = ['planner', 'type_post']
    def __str__(self):
        return "{}: {}".format(self.type_post, self.planner, self.post[:15])