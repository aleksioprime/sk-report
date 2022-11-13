from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from assess.models import StudyYear, ClassGroup

# Register your models here.
@admin.register(StudyYear)
class StudyYearAdmin(ImportExportModelAdmin):
    list_display = ("name", "date_start", "date_end")
    
@admin.register(ClassGroup)
class ClassGroupAdmin(ImportExportModelAdmin):
    list_display = ("class_year", "letter", "id_dnevnik", "study_year")