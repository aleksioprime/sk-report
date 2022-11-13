from django.urls import path
from curriculum.views import UnitPlannerMYPViewEdit, UnitPlannerMYPListCreate, TeacherViewSet, ClassYearViewSet, \
    SubjectViewSet, CriterionViewSet, DepartmentViewSet

urlpatterns = [
    path('unitplans/myp', UnitPlannerMYPListCreate.as_view({'get': 'list', 'post': 'create'})),
    path('unitplans/myp/<int:pk>', UnitPlannerMYPViewEdit.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('departments', DepartmentViewSet.as_view({'get': 'list'})),
    path('teachers', TeacherViewSet.as_view({'get': 'list'})),
    path('grades', ClassYearViewSet.as_view({'get': 'list'})),
    path('subjects', SubjectViewSet.as_view({'get': 'list'})),
    path('criteria', CriterionViewSet.as_view({'get': 'list'})),
]