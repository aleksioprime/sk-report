from django.shortcuts import render
from rest_framework import routers, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from member.serializers import UserSerializer, DepartmentSerializer, UserCreateSerializer, ProfileTeacherSerializer, ContactSerailizer
from member.models import User, Department, ProfileStudent, ProfileTeacher
from assess.models import ClassGroup
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import get_object_or_404
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password
from django.db.models import Q
import csv
import jwt
import openpyxl
import pandas as pd
from django.forms.models import model_to_dict
from datetime import datetime
from django.core.mail import send_mail

temp_storage = FileSystemStorage(location='tmp/')

# Получение пользователя по JWT-токену


class UserAuth(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        token = request.headers['Authorization'].split()[1]
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[
                                 'HS256', 'HS384', 'HS512'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        # print(payload)
        user = User.objects.filter(id=payload['user_id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class UsersSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50

# Набор CRUD-методов для работы с моделью Пользователи

class UserCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    pagination_class = UsersSetPagination
    def get_queryset(self):
        role = self.request.query_params.get("role", None)
        search = self.request.query_params.get("search", None)
        users = User.objects.filter(is_active=True)
        if role == 'teacher':
            users = users.filter(teacher__isnull=False)
        if role == 'student':
            users = users.filter(student__isnull=False)
        if search:
            users = users.filter(Q(first_name__icontains=search) | Q(
                last_name__icontains=search))
        return users
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk=None, *args, **kwargs)
    def update(self, request, pk=None, *args, **kwargs):
        print('Переданные данные для редактирования: ', request.data)
        return super().update(request, pk=None, *args, **kwargs)
    def destroy(self, request, pk=None, *args, **kwargs):
        print('Переданные данные для удаления: ', pk)
        return super().destroy(request, pk=None, *args, **kwargs)

# # Разлогинивание пользователя и удаление токенов
# class Logout(APIView):
#     def post(self, request):
#         response = Response()
#         response.delete_cookie('jwt_token')
#         response.delete_cookie('jwt_refresh')
#         response.data = {'message': 'success'}
#         return response

# Создание путей для CRUD-методов модели Пользователи
# def get_router_urls():
#     router = routers.DefaultRouter()
#     router.register(r'user', UserViewSet, basename='user')
#     return router.urls

# Экспорт пользователей через CSV


    
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = ProfileTeacher.objects.all()
    serializer_class = ProfileTeacherSerializer
    def get_queryset(self):
        role = self.request.query_params.get("role", None)
        teachers = ProfileTeacher.objects.all()
        # if role == 'mentor':
        #     teachers = teachers.filter(group__isnull=True)
        return teachers


@csrf_exempt
def import_users(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel')
        if excel_file:
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb.active
            for value in worksheet.iter_rows(values_only=True):
                print(value)
            return JsonResponse({'data': 'success'})
    return JsonResponse({'data': 'fail'})


class UserImportView(APIView):
    def post(self, request):
        file = request.FILES.get('import')
        if file is None:
            return Response({'Message': 'No FILE'})
        content = file.read()
        file_content = ContentFile(content)
        file_name = temp_storage.save("_tmp.xlsx", file_content)
        tmp_file = temp_storage.path(file_name)

        dfs = pd.read_excel(tmp_file, engine='openpyxl').fillna('')
        applicant_list = dfs.to_dict('records')
        validated_list = [obj for obj in applicant_list if User.objects.filter(
            username=obj['username']).first() is None]

        temp_storage.delete(file_name)
        return Response({
            'applicant_users': applicant_list,
            'validated_users': validated_list,
            'file_import': file_name})


class UserImportApply(APIView, UsersSetPagination):
    pagination_class = UsersSetPagination
    def post(self, request):
        users_import = request.data.get("users", None)
        role = request.data.get("role", None)
        def valid_date(x): return None if x == "NaT" else datetime.fromisoformat(x)
        if users_import and role:
            usernames = [u['username'] for u in users_import]
            usernames_database = User.objects.filter(username__in=usernames).all()
            new_users = []
            new_teachers = []
            new_students = []
            if usernames_database is not None:
                groups = {}
                for item in users_import:
                    created_user = User(
                        username=item['username'],
                        email=item['email'],
                        password=make_password(item['password']),
                        first_name=item['first_name'],
                        middle_name=item.get('middle_name', None),
                        last_name=item['last_name'],
                        date_of_birth=valid_date(item['date_of_birth']),
                        gender=item['gender'],
                    )
                    new_users.append(created_user)
                    if role == 'teacher':
                        created_teacher = ProfileTeacher(
                            id_dnevnik=item['id_dnevnik'],
                            position=item['position'],
                            admin=item['admin'],
                        )
                        created_teacher.user = created_user
                        new_teachers.append(created_teacher)
                    if role == 'student':
                        created_student = ProfileStudent(
                            id_dnevnik=item['id_dnevnik'],
                        )
                        created_student.user = created_user
                        # created_student.groups.through(ClassGroup(pk=item.get('group', None)))
                        group_id = item.get('group', None)
                        if group_id:
                            groups[group_id] = groups.get(group_id, []) + [created_student]
                        new_students.append(created_student)
                print(new_users)
                users = User.objects.bulk_create(new_users)
                # users = User.objects.bulk_create(new_users, ignore_conflicts=True)
                print(f'Созданы пользователи: {users}')
                if role == 'teacher':
                    teachers = ProfileTeacher.objects.bulk_create(new_teachers)
                    print(f'Созданы сотрудники: {teachers}')
                elif role == 'student':
                    students = ProfileStudent.objects.bulk_create(new_students)
                    for key in groups:
                        group = ClassGroup.objects.filter(pk=key).first()
                        iterator_students = filter(lambda x: x in groups[group.id], students)
                        if group.students:
                            for item in iterator_students:
                                group.students.add(item)
                        else:
                            group.students.set(list(iterator_students))
                    print(f'Созданы студенты: {students}')
        if role == 'student':
            queryset = self.paginate_queryset(User.objects.filter(student__isnull=False, is_active=True), request)
        elif role == 'teacher':
            queryset = self.paginate_queryset(User.objects.filter(teacher__isnull=False, is_active=True), request)
        else:
            queryset = self.paginate_queryset(User.objects.filter(is_active=True), request)
        serializer = UserSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)


class FeedBackView(APIView):
    serializer_class = ContactSerailizer
    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerailizer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = 'alesemochkin@yandex.ru'
            subject = 'Stream Report - Обратная связь'
            message = data.get('message')
            print('Отправка сообщения')
            send_mail(f'{subject}', f'{message}\n\nОт {name}', from_email, ['alesemochkin@yandex.ru'])
            return Response({"result": "success"})
        return Response({"result": "failed"})