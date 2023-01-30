from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin
from member.models import User, RoleUser, ProfileTeacher, ProfileStudent, WorkLoad, Department

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ("username", "first_name", "middle_name", "last_name")

@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    list_display = ("name",)
    
@admin.register(RoleUser)
class RoleUserAdmin(ImportExportModelAdmin):
    list_display = ("name", "codename")
    
@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ("name",)
    
@admin.register(ProfileStudent)
class ProfileStudentAdmin(ImportExportModelAdmin):
    list_display = ("user", "short_name", "id_dnevnik", "group")
    
@admin.register(ProfileTeacher)
class ProfileTeacherAdmin(ImportExportModelAdmin):
    list_display = ("user", "short_name", "id_dnevnik")
    
@admin.register(WorkLoad)
class WorkLoadAdmin(ImportExportModelAdmin):
    list_display = ("teacher", "subject", "group", "hours")