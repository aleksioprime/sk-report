from django.shortcuts import render
from rest_framework import routers, viewsets, permissions
from member.serializers import UserSerializer, DepartmentSerializer, RoleSerializer, ClassGroupSerializer
from member.models import User, Department, RoleUser
from assess.models import ClassGroup
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt, openpyxl
from rest_framework.generics import get_object_or_404
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework.decorators import action

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    
class RoleUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RoleUser.objects.all()
    serializer_class = RoleSerializer

class ClassGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupSerializer
    def get_queryset(self):
        # добавить фильтрацию по текущему учебному году
        return ClassGroup.objects.filter(study_year=1)

# Набор CRUD-методов для работы с моделью Пользователи
class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if not pk:
            return User.objects.all()
        return User.objects.filter(pk=pk)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk=None, *args, **kwargs)
    def update(self, request, pk=None, *args, **kwargs):
        return super().update(request, pk=None, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        print(request.data)
        users = request.data.get('select_users')
        if len(users):
            User.objects.filter(id__in=users).delete()
            return Response({'DELETE': "Success"})
        return Response({'DELETE': "Error! Not found USER"})

# Получение пользователя по JWT-токену
class UserAuth(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        token = request.COOKIES.get('jwt_token')
        print(token)
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256', 'HS384', 'HS512'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        print(payload)
        user =  User.objects.filter(id=payload['user_id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)    

# Разлогинивание пользователя и удаление токенов
class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt_token')
        response.delete_cookie('jwt_refresh')
        response.data = {'message': 'success'}
        return response

# Создание путей для CRUD-методов модели Пользователи
# def get_router_urls():
#     router = routers.DefaultRouter()
#     router.register(r'user', UserViewSet, basename='user')
#     return router.urls

# Экспорт пользователей через CSV
def import_users(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel')
        if excel_file:
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb.active
            for value in worksheet.iter_rows(values_only=True):
                print(value)
            return JsonResponse({'data':'success'})
    return JsonResponse({'data':'fail'})