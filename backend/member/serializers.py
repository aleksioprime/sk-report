from rest_framework import serializers
from member.models import User, RoleUser, Department, ProfileStudent, ProfileTeacher
from assess.models import ClassGroup

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
    class Meta:
        model = ProfileStudent
        fields = '__all__'

class ProfileTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileTeacher
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=True, required=False)
    student = ProfileStudentSerializer(required=False)
    teacher = ProfileTeacherSerializer(required=False)
    class Meta:
        model = User
        fields = ["id", "id_str", "username", "password", "email", "first_name", "middle_name", 
                  "last_name", "last_login", "date_of_birth", "gender", "role", "student", 
                  "teacher", "photo"]
        read_only_fields = ['password']
        extra_kwargs = {'username': {'required': False}, 'role': {'validators': []}}
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            middle_name=validated_data.get('middle_name'),
            date_of_birth=validated_data.get('date_of_birth'),
            gender=validated_data.get('gender'),
        )
        roles = [x['name'] for x in validated_data.get('role')]
        print(roles)
        user.role.set(RoleUser.objects.filter(name__in=roles))
        user.set_password(validated_data.get('password', '1qaz@WSX'))
        user.save()
        if validated_data.get('student'):
            student = ProfileStudent.objects.create(user=user, **validated_data.get('student'))
            student.save()
        if validated_data.get('teacher'):
            teacher = ProfileTeacher.objects.create(user=user, **validated_data.get('teacher'))
            teacher.save()
        return user
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance
        