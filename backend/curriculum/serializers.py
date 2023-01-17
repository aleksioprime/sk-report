from rest_framework import serializers
from curriculum.models import UnitPlannerMYP, KeyConcept, SubjectGroupIB, RelatedConcept, SubjectDirectionRC, Subject, \
    SubjectGroupIB, ClassYear, GlobalContext, ExplorationToDevelop, Aim, Objective, Strand, Criterion, Level, SkillATL, \
    ClusterATL, CategoryATL, LearnerProfileIB, InquiryQuestionMYP, ATLMappingMYP, ReflectionMYP
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

class LearnerProfileIBSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerProfileIB
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

class SkillATLSerializer(serializers.ModelSerializer):
    cluster = ClusterATLSerializer()
    class Meta:
        model = SkillATL
        fields = '__all__'

class InQuestionMYPSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiryQuestionMYP
        fields = '__all__'
        
class ATLMappingMYPSerializer(serializers.ModelSerializer):
    atl = SkillATLSerializer(read_only=True)
    objective = ObjectiveSerializer(read_only=True)
    class Meta:
        model = ATLMappingMYP
        fields = ['id', 'atl', 'atl_id', 'objective', 'objective_id', 'action', 'planner']
        extra_kwargs = {
            'objective_id': {'source': 'objective', 'write_only': True},
            'atl_id': {'source': 'atl', 'write_only': True},
        }
        
class ReflectionMYPSerializer(serializers.ModelSerializer):
    author = ProfileTeacherSerializer(read_only=True)
    class Meta:
        model = ReflectionMYP
        fields = ['id', 'type_post', 'post', 'author', 'author_id', 'planner']
        extra_kwargs = {
            'author_id': {'source': 'author', 'write_only': True},
        }

class UnitMYPSerializerViewEdit(serializers.ModelSerializer):
    key_concepts = KeyConceptSerializer(many=True, read_only=True)
    related_concepts = RelatedConceptSerializer(many=True, read_only=True)
    authors = ProfileTeacherSerializer(many=True, read_only=True)
    subject = SubjectSerializer(read_only=True)
    class_year = ClassYearSerializer(read_only=True)
    global_context = GlobalContextSerializer(read_only=True)
    explorations = ExplorationToDevelopSerializer(many=True, read_only=True)
    aims = AimSerializer(many=True, read_only=True)
    objectives = ObjectiveSerializer(many=True, read_only=True)
    criteria = CriterionSerializer(many=True, read_only=True)
    learner_profile = LearnerProfileIBSerializer(many=True, read_only=True)
    inquestions = InQuestionMYPSerializer(many=True, read_only=True)
    atlmapping = ATLMappingMYPSerializer(many=True, read_only=True)
    reflections = ReflectionMYPSerializer(many=True, read_only=True)
    class Meta:
        model = UnitPlannerMYP
        fields = ['id', 'title', 'subject', 'authors', 'order', 'interdisciplinary', 'class_year', 'hours', 'description',
                  'key_concepts', 'related_concepts', 'conceptual_understanding', 'global_context', 'explorations', 'statement_inquiry',
                  'aims', 'objectives', 'content', 'skills', 'learner_profile', 'description_lp', 'international_mindedness',
                  'academic_integrity', 'language_development', 'infocom_technology', 'service_as_action', 'criteria', 'formative_assessment', 'summative_assessment_task',
                  'summative_assessment_soi', 'peer_self_assessment', 'standardization_moderation', 'prior_experiences', 'learning_experiences', 'teaching_strategies', 
                  'teaching_strategies', 'student_expectations', 'feedback', 'differentiation', 'criteria_ids', 'learner_profile_ids', 'objectives_ids',
                  'aims_ids', 'global_context_id', 'explorations_ids', 'key_concepts_ids', 'related_concepts_ids', 'class_year_id', 'authors_ids', 'subject_id', 
                  'inquestions', 'atlmapping', 'reflections',
                  ]
        extra_kwargs = {
            'title': {'required': False},
            'criteria_ids': {'source': 'criteria', 'write_only': True},
            'learner_profile_ids': {'source': 'learner_profile', 'write_only': True},
            'atl_skills_ids': {'source': 'atl_skills', 'write_only': True},
            'objectives_ids': {'source': 'objectives', 'write_only': True},
            'aims_ids': {'source': 'aims', 'write_only': True},
            'global_context_id': {'source': 'global_context', 'write_only': True},
            'explorations_ids': {'source': 'explorations', 'write_only': True},
            'key_concepts_ids': {'source': 'key_concepts', 'write_only': True},
            'related_concepts_ids': {'source': 'related_concepts', 'write_only': True},
            'class_year_id': {'source': 'class_year', 'write_only': True},
            'authors_ids': {'source': 'authors', 'write_only': True, 'required': False},
            'subject_id': {'source': 'subject', 'write_only': True},
            }
    def update(self, instance, validated_data):
        print(validated_data)
        return super().update(instance, validated_data)
    
class UnitMYPSerializerListCreate(serializers.ModelSerializer):
    key_concepts = KeyConceptSerializer(many=True, required=False)
    related_concepts = RelatedConceptSerializer(many=True, required=False)
    authors = ProfileTeacherSerializer(many=True, read_only=True)
    subject = SubjectSerializer(read_only=True)
    class_year = ClassYearSerializer(read_only=True)
    global_context = GlobalContextSerializer(required=False)
    explorations = ExplorationToDevelopSerializer(many=True, required=False)
    criteria = CriterionSerializer(many=True, read_only=True)
    class Meta:
        model = UnitPlannerMYP
        fields = ['id', 'title', 'subject', 'order', 'class_year', 'hours', 'interdisciplinary', 'key_concepts', 
                  'related_concepts', 'authors', 'global_context', 'explorations', 'statement_inquiry', 'criteria',
                  'criteria_ids', 'subject_id', 'class_year_id', 'authors_ids',
                  ]
        extra_kwargs = {
            'criteria_ids': {'source': 'criteria', 'write_only': True},
            'subject_id': {'source': 'subject', 'write_only': True},
            'class_year_id': {'source': 'class_year', 'write_only': True},
            'authors_ids': {'source': 'authors', 'write_only': True},
            }
    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)
        
        