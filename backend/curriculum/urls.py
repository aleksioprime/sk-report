from django.urls import path
from curriculum.views import UnitPlannerMYPViewEdit, UnitPlannerMYPListCreate, TeacherViewSet, ClassYearViewSet, \
    SubjectViewSet, CriterionViewSet, DepartmentViewSet, LearnerProfileIBViewSet, IndicatorATLViewSet, ObjectiveViewSet, \
    AimViewSet, GlobalContextViewSet, ExplorationToDevelopViewSet, KeyConceptViewSet, RelatedConceptViewSet

urlpatterns = [
    path('unitplans/myp', UnitPlannerMYPListCreate.as_view({'get': 'list', 'post': 'create'})),
    path('unitplans/myp/<int:pk>', UnitPlannerMYPViewEdit.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('departments', DepartmentViewSet.as_view({'get': 'list'})),
    path('teachers', TeacherViewSet.as_view({'get': 'list'})),
    path('grades', ClassYearViewSet.as_view({'get': 'list'})),
    path('subjects', SubjectViewSet.as_view({'get': 'list'})),
    path('criteria', CriterionViewSet.as_view({'get': 'list'})),
    path('ibprofile', LearnerProfileIBViewSet.as_view({'get': 'list'})),
    path('atlskills', IndicatorATLViewSet.as_view({'get': 'list'})),
    path('objectives', ObjectiveViewSet.as_view({'get': 'list'})),
    path('aims', AimViewSet.as_view({'get': 'list'})),
    path('gcontext', GlobalContextViewSet.as_view({'get': 'list'})),
    path('explorations', ExplorationToDevelopViewSet.as_view({'get': 'list'})),
    path('kconcepts', KeyConceptViewSet.as_view({'get': 'list'})),
    path('rconcepts', RelatedConceptViewSet.as_view({'get': 'list'})),
]