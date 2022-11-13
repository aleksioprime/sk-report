from rest_framework import serializers
from curriculum.models import UnitPlannerMYP, KeyConcept, SubjectGroupIB, RelatedConcept, SubjectDirectionRC, Subject, \
    SubjectGroupIB, ClassYear, GlobalContext, ExplorationToDevelop, Aim, Objective, Strand, Criterion, Level, IndicatorATL, \
    SubClusterATL, ClusterATL, CategoryATL
from member.models import ProfileTeacher, User, Department

class SubjectGroupIBSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectGroupIB
        fields = '__all__'

class KeyConceptSerializer(serializers.ModelSerializer):
    recommended_subjects = SubjectGroupIBSerializer(many=True, required=False)
    class Meta:
        model = KeyConcept
        fields = '__all__'

class SubjectDirectionRCSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectDirectionRC
        fields = '__all__'
        
class RelatedConceptSerializer(serializers.ModelSerializer):
    subdirections = SubjectDirectionRCSerializer(many=True, required=False)
    class Meta:
        model = RelatedConcept
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'gender']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ProfileTeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    departments = DepartmentSerializer(many=True)
    class Meta:
        model = ProfileTeacher
        fields = '__all__'

class SubjectGroupIBSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectGroupIB
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    group_ib = SubjectGroupIBSerializer()
    department = DepartmentSerializer()
    class Meta:
        model = Subject
        fields = '__all__'
        
class ClassYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassYear
        fields = '__all__'

class GlobalContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalContext
        fields = '__all__'

class ExplorationToDevelopSerializer(serializers.ModelSerializer):
    gcontext = GlobalContextSerializer()
    class Meta:
        model = ExplorationToDevelop
        fields = '__all__'

class AimSerializer(serializers.ModelSerializer):
    subject_group = SubjectGroupIBSerializer()
    class Meta:
        model = Aim
        fields = '__all__'
        
class CriterionSerializer(serializers.ModelSerializer):
    subject_group = SubjectGroupIBSerializer()
    class Meta:
        model = Criterion
        fields = '__all__'
        
class StrandSerializer(serializers.ModelSerializer):
    criterion = CriterionSerializer()
    class Meta:
        model = Strand
        fields = '__all__'
        
class LevelSerializer(serializers.ModelSerializer):
    years = ClassYearSerializer(many=True)
    class Meta:
        model = Level
        fields = '__all__'

class ObjectiveSerializer(serializers.ModelSerializer):
    strand = StrandSerializer()
    level = LevelSerializer()
    class Meta:
        model = Objective
        fields = '__all__'

class CategoryATLSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryATL
        fields = '__all__'

class ClusterATLSerializer(serializers.ModelSerializer):
    category = CategoryATLSerializer()
    class Meta:
        model = ClusterATL
        fields = '__all__'

class SubClusterATLSerializer(serializers.ModelSerializer):
    cluster = ClusterATLSerializer()
    class Meta:
        model = SubClusterATL
        fields = '__all__'

class IndicatorATLSerializer(serializers.ModelSerializer):
    subcluster = SubClusterATLSerializer()
    class Meta:
        model = IndicatorATL
        fields = '__all__'

class UnitMYPSerializerViewEdit(serializers.ModelSerializer):
    key_concepts = KeyConceptSerializer(many=True, required=False)
    related_concepts = RelatedConceptSerializer(many=True, required=False)
    authors = ProfileTeacherSerializer(many=True, required=False)
    subject = SubjectSerializer(required=False)
    class_year = ClassYearSerializer(required=False)
    global_context = GlobalContextSerializer()
    explorations = ExplorationToDevelopSerializer(many=True)
    aims = AimSerializer(many=True)
    objectives = ObjectiveSerializer(many=True)
    atl_skills = IndicatorATLSerializer(many=True)
    criteria = CriterionSerializer(many=True)
    class Meta:
        model = UnitPlannerMYP
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.save()
        return instance
    
class UnitMYPSerializerListCreate(serializers.ModelSerializer):
    key_concepts = KeyConceptSerializer(many=True, required=False)
    related_concepts = RelatedConceptSerializer(many=True, required=False)
    authors = ProfileTeacherSerializer(many=True, read_only=True)
    subject = SubjectSerializer(read_only=True)
    class_year = ClassYearSerializer(read_only=True)
    global_context = GlobalContextSerializer(required=False)
    explorations = ExplorationToDevelopSerializer(many=True, required=False)
    criteria = CriterionSerializer(many=True, read_only=True)
    atl_skills = IndicatorATLSerializer(many=True, required=False)
    class Meta:
        model = UnitPlannerMYP
        fields = ['id', 'title', 'subject', 'order', 'class_year', 'hours', 'interdisciplinary', 'key_concepts', 
                  'related_concepts', 'authors', 'global_context', 'explorations', 'statement_inquiry', 'criteria', 'atl_skills',
                  'criteria_ids', 'subject_id', 'class_year_id', 'authors_ids']
        extra_kwargs = {
            'criteria_ids': {'source': 'criteria', 'write_only': True},
            'subject_id': {'source': 'subject', 'write_only': True},
            'class_year_id': {'source': 'class_year', 'write_only': True},
            'authors_ids': {'source': 'authors', 'write_only': True},
        }
    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)