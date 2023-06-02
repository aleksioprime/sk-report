from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from curriculum.models import SubjectGroupIB, ClassYear, SubjectGroupFGOS, Subject, Criterion, Strand, \
    Level, Objective, AchievementLevel, KeyConcept, RecommendSubjectKC, SubjectDirectionRC, RelatedConcept, \
    GlobalContext, ExplorationToDevelop, CategoryATL, ClusterATL, SkillATL, ReflectionMYP, \
    InquiryQuestionMYP, Aim, LearnerProfileIB, UnitPlannerMYP, UnitPlannerMYPID, UnitPlannerDP, \
        ReflectionDP, InquiryQuestionDP, ATLMappingMYP, DevelopProfileMYP, AcademicPlan, HoursSubjectInYear

@admin.register(AcademicPlan)
class AcademicPlanAdmin(ImportExportModelAdmin):
    list_display = ("study_year", "name_rus")

@admin.register(HoursSubjectInYear)
class HoursSubjectInYearAdmin(ImportExportModelAdmin):
    list_display = ("subject", "hours")

@admin.register(SubjectGroupIB)
class SubjectGroupIBAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "name_rus", "program")
    
@admin.register(ClassYear)
class ClassYearAdmin(ImportExportModelAdmin):
    list_display = ("year_rus", "year_ib", "program", "level")
    
@admin.register(SubjectGroupFGOS)
class SubjectGroupFGOSAdmin(ImportExportModelAdmin):
    list_display = ("name_rus", "type")
    
@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    list_display = ("name_rus", "id_dnevnik", "group_ib", "group_fgos", "type")

@admin.register(Criterion)
class CriterionAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "letter", "subject_group")

@admin.register(Strand)
class StrandAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "letter", "number", "criterion")

@admin.register(Level)
class LevelAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "name_rus")

@admin.register(Objective)
class ObjectiveAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "strand", "level")

@admin.register(AchievementLevel)
class AchievementLevelAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "point", "objective")

@admin.register(KeyConcept)
class KeyConceptAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "description_eng")

@admin.register(RecommendSubjectKC)
class RecommendSubjectKCAdmin(ImportExportModelAdmin):
    list_display = ("key_concept", "subject_group", "comment_eng")

@admin.register(SubjectDirectionRC)
class SubjectDirectionRCAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "name_rus", "subject_group")

@admin.register(RelatedConcept)
class RelatedConceptAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "description_eng")
    
# @admin.register(ConnectSubjectRC)
# class ConnectSubjectRCAdmin(ImportExportModelAdmin):
#     list_display = ("related_concept", "subject_group", "subject_direction")

@admin.register(GlobalContext)
class GlobalContextAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "focus_questions_eng", "description_eng")

@admin.register(ExplorationToDevelop)
class ExplorationToDevelopAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "name_rus", "gcontext")

@admin.register(CategoryATL)
class CategoryATLAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "name_rus")

@admin.register(ClusterATL)
class ClusterATLAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "name_rus", "category")

@admin.register(SkillATL)
class SkillATLAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "name_rus", "cluster")

@admin.register(Aim)
class AimAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "name_rus", "subject_group")

@admin.register(LearnerProfileIB)
class LearnerProfileIBAdmin(ImportExportModelAdmin):
    list_display = ("name_eng", "name_rus", "description_eng")

@admin.register(UnitPlannerMYP)
class UnitPlannerMYPAdmin(ImportExportModelAdmin):
    list_display = ("title", "class_year", "subject")

@admin.register(UnitPlannerMYPID)
class UnitPlannerMYPIDAdmin(ImportExportModelAdmin):
    list_display = ("title", "purpose_integration")
    
@admin.register(ReflectionMYP)
class ReflectionMYPAdmin(ImportExportModelAdmin):
    list_display = ("type", "author", "post")

@admin.register(InquiryQuestionMYP)
class InquiryQuestionMYPAdmin(ImportExportModelAdmin):
    list_display = ("question", "type")

@admin.register(ATLMappingMYP)
class ATLMappingMYPAdmin(ImportExportModelAdmin):
    list_display = ("atl", "strand", "action")

@admin.register(DevelopProfileMYP)
class DevelopProfileMYPAdmin(ImportExportModelAdmin):
    list_display = ("profile", "description")

@admin.register(UnitPlannerDP)
class UnitPlannerDPAdmin(ImportExportModelAdmin):
    list_display = ("title", "subject", "class_year")
    
@admin.register(ReflectionDP)
class ReflectionDPAdmin(ImportExportModelAdmin):
    list_display = ("planner", "type_post", "author")

@admin.register(InquiryQuestionDP)
class InquiryQuestionDPAdmin(ImportExportModelAdmin):
    list_display = ("question", "type_inq", "planner")