from rest_framework import serializers
from member.models import User, Department, ProfileStudent, ProfileTeacher
from assess.models import ClassGroup
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ProfileStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileStudent
        fields = ['id', 'id_dnevnik']

class ClassGroupSerializer(serializers.ModelSerializer):
    class_year = serializers.CharField(source='class_year.year_rus', read_only=True)
    class Meta:
        model = ClassGroup
        fields = '__all__'

class ProfileTeacherSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    middle_name = serializers.CharField(source='user.middle_name', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    short_name = serializers.CharField(source='user.get_short_name', read_only=True)
    groups = ClassGroupSerializer(many=True, required=False)
    psycho_groups = ClassGroupSerializer(many=True, required=False)
    # units = UnitMYPSerializerListCreate(source='unitplan_myp', many=True, read_only=True)
    class Meta:
        model = ProfileTeacher
        fields = ['id', 'id_dnevnik', 'position', 'admin', 'last_name', 'first_name', 
                  'middle_name', 'groups', 'psycho_groups', 'full_name', 'short_name']
        extra_kwargs = {
            'groups': {'required': False, 'read_only': True},
            'psycho_groups': {'required': False, 'read_only': True},
            }

class UserCreateSerializer(serializers.ModelSerializer):
    student = ProfileStudentSerializer(required=False)
    teacher = ProfileTeacherSerializer(required=False)
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "middle_name", 
                  "last_name", "last_login", "date_of_birth", "gender", "student", 
                  "teacher", "photo", 'is_staff', 'password', 'is_active']
        read_only_fields = ['photo', 'is_staff']
        write_only_fields = ["password"]
        # extra_kwargs = {'username': {'required': False}, 'role': {'validators': []}}
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            }
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        user = User.objects.create(
            username=validated_data.get('username').lower(),
            email=validated_data.get('email').lower(),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            middle_name=validated_data.get('middle_name'),
            date_of_birth=validated_data.get('date_of_birth'),
            gender=validated_data.get('gender'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        if 'teacher' in validated_data:
            teacher = ProfileTeacher.objects.create(user=user, **validated_data.get('teacher'))
            print('Создан учитель:', teacher)
        if 'student' in validated_data:
            print("Добавление студента")
            student = ProfileStudent.objects.create(user=user, **validated_data.get('student'))
            print('Создан студент:', student)
        return user
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop('password', None)
        return response
    
class UserSerializer(serializers.ModelSerializer):
    student = ProfileStudentSerializer(required=False)
    teacher = ProfileTeacherSerializer(required=False)
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "middle_name", 
                  "last_name", "last_login", "date_of_birth", "gender", "student", 
                  "teacher", "photo", 'is_staff', 'is_active', 'access_token_dnevnik']
        read_only_fields = ['photo', 'is_staff']
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            }
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        if 'student' in validated_data:
            ProfileStudent.objects.update_or_create(user=instance, defaults=dict(validated_data.get('student')))
            validated_data.pop('student')
        if 'teacher' in validated_data:
            ProfileTeacher.objects.update_or_create(user=instance, defaults=dict(validated_data.get('teacher')))
            validated_data.pop('teacher')
        return super().update(instance, validated_data)

class UserImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ContactSerailizer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    message = serializers.CharField()