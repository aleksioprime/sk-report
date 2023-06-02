from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from assess.models import StudyYear, ClassGroup, StudyPeriod, SummativeWork, WorkAssessment, WorkCriteriaMark, \
    PeriodAssessment, WorkGroupDate, ReportPeriod, ReportTeacher, ReportMentor, EventType, \
        EventParticipation, ReportPsychologist, WorkLoad, ReportAchievements, ReportCriteria

# Register your models here.
@admin.register(StudyYear)
class StudyYearAdmin(ImportExportModelAdmin):
    list_display = ("name", "date_start", "date_end")
    
@admin.register(ClassGroup)
class ClassGroupAdmin(ImportExportModelAdmin):
    list_display = ("class_year", "letter", "id_dnevnik", "study_year")

@admin.register(WorkLoad)
class WorkLoadAdmin(ImportExportModelAdmin):
    list_display = ("teacher", "subject", "hours")
    
@admin.register(StudyPeriod)
class StudyPeriodAdmin(ImportExportModelAdmin):
    list_display = ("study_year", "number", "type", "date_start", "date_end")

@admin.register(SummativeWork)
class SummativeWorkAdmin(ImportExportModelAdmin):
    list_display = ("title", "unit", "period", "subject")

@admin.register(WorkGroupDate)
class WorkGroupDateAdmin(ImportExportModelAdmin):
    list_display = ("work", "group", "date", "lesson")

@admin.register(WorkAssessment)
class WorkAssessmentAdmin(ImportExportModelAdmin):
    list_display = ("work_date", "student", "grade")

@admin.register(WorkCriteriaMark)
class WorkCriteriaMarkAdmin(ImportExportModelAdmin):
    list_display = ("work_assess", "criterion", "mark")

@admin.register(PeriodAssessment)
class PeriodAssessmentAdmin(ImportExportModelAdmin):
    list_display = ("period", "student", "criterion_a", "criterion_b", "criterion_c", "criterion_d", "final_grade")

@admin.register(ReportPeriod)
class ReportPeriodAdmin(ImportExportModelAdmin):
    list_display = ("study_year", "number", "date_start", "date_end")

@admin.register(ReportTeacher)
class ReportTeacherAdmin(ImportExportModelAdmin):
    list_display = ("student", "period", "subject", "author", "created", "updated")

@admin.register(ReportCriteria)
class ReportCriteriaAdmin(ImportExportModelAdmin):
    list_display = ("report_teacher", "criterion", "mark")

@admin.register(ReportAchievements)
class ReportAchievementsAdmin(ImportExportModelAdmin):
    list_display = ("objective", "achievement")

@admin.register(ReportMentor)
class ReportMentorAdmin(ImportExportModelAdmin):
    list_display = ("student", "period", "text", "author", "created", "updated")

@admin.register(ReportPsychologist)
class ReportPsychologistAdmin(ImportExportModelAdmin):
    list_display = ("student", "period", "text", "author", "created", "updated")

@admin.register(EventType)
class EventTypeAdmin(ImportExportModelAdmin):
    list_display = ("name", "description")

@admin.register(EventParticipation)
class EventParticipationAdmin(ImportExportModelAdmin):
    list_display = ("title", "type", "result")