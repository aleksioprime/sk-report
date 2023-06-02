from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin
from member.models import User, ProfileTeacher, ProfileStudent, Department

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ("username", "first_name", "middle_name", "last_name", 'is_active')

@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    list_display = ("name",)
    
@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ("name",)
    
@admin.register(ProfileStudent)
class ProfileStudentAdmin(ImportExportModelAdmin):
    list_display = ("user", "id_dnevnik")
    
@admin.register(ProfileTeacher)
class ProfileTeacherAdmin(ImportExportModelAdmin):
    list_display = ("user", "id_dnevnik", 'position', 'admin')
