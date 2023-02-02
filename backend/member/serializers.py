from rest_framework import serializers
from member.models import User, RoleUser, Department, ProfileStudent, ProfileTeacher
from assess.models import ClassGroup
from curriculum.serializers import SubjectSerializer, UnitMYPSerializerListCreate

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleUser
        fields = '__all__'
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        
class ClassGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassGroup
        fields = '__all__'

class ProfileStudentSerializer(serializers.ModelSerializer):
    group = ClassGroupSerializer(read_only=True)
    class Meta:
        model = ProfileStudent
        fields = ['id', 'id_dnevnik', 'group', 'group_id']
        extra_kwargs = {
            'group_id': {'source': 'group', 'write_only': True}
        }

class ProfileTeacherSerializer(serializers.ModelSerializer):
    units = UnitMYPSerializerListCreate(source='unitplan_myp', many=True, read_only=True)
    class Meta:
        model = ProfileTeacher
        fields = ['id', 'id_dnevnik', 'units']

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True, read_only=True)
    student = ProfileStudentSerializer()
    teacher = ProfileTeacherSerializer()
    class Meta:
        model = User
        fields = ["id", "id_str", "username", "email", "first_name", "middle_name", 
                  "last_name", "last_login", "date_of_birth", "gender", "role", "student", 
                  "teacher", "photo", 'roles_ids', 'is_staff', 'password']
        read_only_fields = ['photo', 'is_staff']
        write_only_fields = ["password"]
        # extra_kwargs = {'username': {'required': False}, 'role': {'validators': []}}
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'roles_ids': {'source': 'role', 'write_only': True},
            }
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            middle_name=validated_data.get('middle_name'),
            date_of_birth=validated_data.get('date_of_birth'),
            gender=validated_data.get('gender'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        user.role.set(validated_data.get('role'))
        roles_list = [x.id for x in validated_data.get('role')]
        print(roles_list)
        print('Создан пользователь: ', user)
        if 1 in roles_list:
            student = ProfileStudent.objects.create(user=user, **validated_data.get('student'))
            print('Создан студент: ', student)
        if 2 in roles_list:
            teacher = ProfileTeacher.objects.create(user=user, **validated_data.get('teacher'))
            print('Создан учитель: ', teacher)
        return user
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        roles_list = [x.id for x in validated_data.get('role')]
        if 1 in roles_list:
            ProfileStudent.objects.update_or_create(user=instance, defaults=dict(validated_data.get('student')))
        else:
            ProfileStudent.objects.filter(user=instance).delete()
        if 2 in roles_list:
            ProfileTeacher.objects.update_or_create(user=instance, defaults=dict(validated_data.get('teacher')))
        else:
            ProfileTeacher.objects.filter(user=instance).delete()
        validated_data.pop('teacher')
        validated_data.pop('student')
        return super().update(instance, validated_data)

class UserImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"