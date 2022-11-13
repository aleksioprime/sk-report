from xml.etree.ElementInclude import include
from django.urls import path
from member.views import UserAuth, Logout, DepartmentViewSet, RoleUserViewSet, ClassGroupViewSet, UserViewSet, \
    import_users


urlpatterns = [
    path('auth', UserAuth.as_view()),
    path('logout', Logout.as_view()),
    path('department', DepartmentViewSet.as_view({'get': 'list'})),
    path('role', RoleUserViewSet.as_view({'get': 'list'})),
    path('class', ClassGroupViewSet.as_view({'get': 'list'})),
    path('user/import', import_users),
    path('user', UserViewSet.as_view({'get': 'list', 'delete': 'destroy', 'post': 'create'})),
    path('user/<int:pk>', UserViewSet.as_view({'get': 'get', 'put': 'update'})),
]