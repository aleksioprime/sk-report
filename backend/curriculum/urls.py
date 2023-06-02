from django.urls import path
from curriculum.views import UnitPlannerMYPViewEdit, UnitPlannerMYPListCreate, ClassYearViewSet, \
    SubjectViewSet, CriterionViewSet, DepartmentViewSet, LearnerProfileIBViewSet, SkillATLViewSet, ObjectiveViewSet, StrandViewSet, \
    AimViewSet, GlobalContextViewSet, ExplorationToDevelopViewSet, KeyConceptViewSet, RelatedConceptViewSet, \
    InQuestionMYPViewSet, ATLMappingMYPViewSet, ReflectionMYPViewSet, LevelViewSet, UnitPlannerMYPIDListCreateSet, \
    UnitExport, UnitPlannerMYPList, UnitPlannerMYPIDViewEditSet, CriterionDetailViewSet, AcademicPlanViewSet, HoursSubjectInYearViewSet, \
    CriteriaGroupsViewSet, SubjectGroupFGOSViewSet

urlpatterns = [
    path('myp/unit', UnitPlannerMYPListCreate.as_view({'get': 'list', 'post': 'create'})),
    path('myp/unitlist', UnitPlannerMYPList.as_view({'get': 'list'})),
    path('myp/unit/<int:pk>', UnitPlannerMYPViewEdit.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('departments', DepartmentViewSet.as_view({'get': 'list'})),
    path('myp/years', ClassYearViewSet.as_view({'get': 'list'})),
    path('myp/levels', LevelViewSet.as_view({'get': 'list'})),
    path('myp/subjects', SubjectViewSet.as_view({'get': 'list'})),
    path('myp/criteria', CriterionViewSet.as_view({'get': 'list'})),
    path('myp/criteria/detail', CriterionDetailViewSet.as_view({'get': 'list'})),
    path('myp/ibprofile', LearnerProfileIBViewSet.as_view({'get': 'list'})),
    path('myp/atl', SkillATLViewSet.as_view({'get': 'list'})),
    path('myp/objectives', ObjectiveViewSet.as_view({'get': 'list'})),
    path('myp/strands', StrandViewSet.as_view({'get': 'list'})),
    path('myp/aims', AimViewSet.as_view({'get': 'list'})),
    path('myp/gcontext', GlobalContextViewSet.as_view({'get': 'list'})),
    path('myp/explorations', ExplorationToDevelopViewSet.as_view({'get': 'list'})),
    path('myp/kconcepts', KeyConceptViewSet.as_view({'get': 'list'})),
    path('myp/rconcepts', RelatedConceptViewSet.as_view({'get': 'list'})),
    path('unitplans/myp/export', UnitExport.as_view()),
    path('unitplans/myp/inquestion', InQuestionMYPViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unitplans/myp/inquestion/<int:pk>', InQuestionMYPViewSet.as_view({'put': 'update', 'delete': 'destroy' })),
    path('unitplans/myp/atlmapping', ATLMappingMYPViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unitplans/myp/atlmapping/<int:pk>', ATLMappingMYPViewSet.as_view({'put': 'update', 'delete': 'destroy' })),
    path('unitplans/myp/reflection', ReflectionMYPViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unitplans/myp/reflection/<int:pk>', ReflectionMYPViewSet.as_view({'put': 'update', 'delete': 'destroy' })),
    path('myp/interdisciplinary', UnitPlannerMYPIDListCreateSet.as_view({'get': 'list', 'post': 'create'})),
    path('myp/interdisciplinary/<int:pk>', UnitPlannerMYPIDViewEditSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy' })),
    # path('unitplans/myp/subject', SubjectLevelMYPViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('unitplans/myp/subject/<int:pk>', SubjectLevelMYPViewSet.as_view({'put': 'update', 'delete': 'destroy' })),
    path('curriculum/academicplans', AcademicPlanViewSet.as_view({'get': 'list'})),
    path('curriculum/academicplans/<int:pk>', AcademicPlanViewSet.as_view({'get': 'retrieve'})),
    path('curriculum/subjecthours', HoursSubjectInYearViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('curriculum/subjecthours/<int:pk>', HoursSubjectInYearViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('curriculum/criteriagroups', CriteriaGroupsViewSet.as_view({'get': 'list'})),
    path('curriculum/subjectgroups', SubjectGroupFGOSViewSet.as_view({'get': 'list'})),
]