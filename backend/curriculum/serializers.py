from rest_framework import serializers
from curriculum.models import UnitPlannerMYP, KeyConcept, SubjectGroupIB, RelatedConcept, SubjectDirectionRC, Subject, \
    SubjectGroupIB, ClassYear, GlobalContext, ExplorationToDevelop, Aim, Objective, Strand, Criterion, Level, SkillATL, \
    ClusterATL, CategoryATL, LearnerProfileIB, InquiryQuestionMYP, ATLMappingMYP, ReflectionMYP, UnitPlannerMYPID, SubjectLevelMYP
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
    subject_group = SubjectGroupIBSerializer()
    class Meta:
        model = SubjectDirectionRC
        fields = '__all__'
        
class RelatedConceptSerializer(serializers.ModelSerializer):
    subject_directions = SubjectDirectionRCSerializer(many=True)
    class Meta:
        model = RelatedConcept
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'gender']

class ProfileTeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ProfileTeacher
        fields = '__all__'

class SubjectGroupIBSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectGroupIB
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    group_ib = SubjectGroupIBSerializer()
    class Meta:
        model = Subject
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many=True)
    class Meta:
        model = Department
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

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'
        
class SubjectLevelMYPSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    class Meta:
        model = SubjectLevelMYP
        fields = ['id', 'subject', 'level', 'subject_id', 'level_id']
        extra_kwargs = {
            'subject_id': {'source': 'subject', 'write_only': True},
            'level_id': {'source': 'level', 'write_only': True},
        }

class ObjectiveSerializer(serializers.ModelSerializer):
    level = LevelSerializer()
    class Meta:
        model = Objective
        fields = '__all__'
     
class StrandSerializer(serializers.ModelSerializer):
    criterion = CriterionSerializer()
    objective = ObjectiveSerializer(many=True)
    class Meta:
        model = Strand
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
    strand = StrandSerializer(read_only=True)
    class Meta:
        model = ATLMappingMYP
        fields = ['id', 'atl', 'atl_id', 'strand', 'strand_id', 'action', 'planner']
        extra_kwargs = {
            'strand_id': {'source': 'strand', 'write_only': True},
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

class UnitPlannerMYPIDSerializer(serializers.ModelSerializer):
    inter_criteria = CriterionSerializer(many=True, read_only=True)
    inter_aims = AimSerializer(many=True, read_only=True)
    inter_strands = StrandSerializer(many=True, read_only=True)
    class Meta:
        model = UnitPlannerMYPID
        fields = ['id', 'form_integration', 'purpose_integration', 'interdisciplinary_links', 'inter_criteria', 'inter_aims', 'inter_strands', 'inter_criteria_ids', 'inter_aims_ids', 'inter_strands_ids']
        extra_kwargs = {
            'inter_criteria_ids': {'source': 'inter_criteria', 'write_only': True},
            'inter_aims_ids': {'source': 'inter_aims', 'write_only': True},
            'inter_strands_ids': {'source': 'inter_strands', 'write_only': True},
        }

class UnitMYPSerializerViewEdit(serializers.ModelSerializer):
    key_concepts = KeyConceptSerializer(many=True, read_only=True)
    related_concepts = RelatedConceptSerializer(many=True, read_only=True)
    authors = ProfileTeacherSerializer(many=True, read_only=True)
    class_year = ClassYearSerializer(read_only=True)
    global_context = GlobalContextSerializer(read_only=True)
    explorations = ExplorationToDevelopSerializer(many=True, read_only=True)
    aims = AimSerializer(many=True, read_only=True)
    strands = StrandSerializer(many=True, read_only=True)
    subjects = SubjectLevelMYPSerializer(many=True, source='subject_unit', required=False)
    criteria = CriterionSerializer(many=True, read_only=True)
    learner_profile = LearnerProfileIBSerializer(many=True, read_only=True)
    inquestions = InQuestionMYPSerializer(many=True, read_only=True)
    atlmapping = ATLMappingMYPSerializer(many=True, read_only=True)
    reflections = ReflectionMYPSerializer(many=True, read_only=True)
    inter = UnitPlannerMYPIDSerializer(read_only=True)
    class Meta:
        model = UnitPlannerMYP
        fields = ['id', 'title', 'authors', 'order', 'class_year', 'hours', 'description',
                  'key_concepts', 'related_concepts', 'conceptual_understanding', 'global_context', 'explorations', 'statement_inquiry',
                  'aims', 'strands', 'content', 'skills', 'learner_profile', 'description_lp', 'international_mindedness',
                  'academic_integrity', 'language_development', 'infocom_technology', 'service_as_action', 'criteria', 'formative_assessment', 'summative_assessment_task',
                  'summative_assessment_soi', 'peer_self_assessment', 'standardization_moderation', 'prior_experiences', 'learning_experiences', 'teaching_strategies', 
                  'teaching_strategies', 'student_expectations', 'feedback', 'differentiation', 'criteria_ids', 'learner_profile_ids', 
                  'aims_ids', 'global_context_id', 'explorations_ids', 'key_concepts_ids', 'related_concepts_ids', 'class_year_id', 'authors_ids', 
                  'inquestions', 'atlmapping', 'reflections', 'strands_ids', 'subjects', 'inter', 'resources'
                  ]
        extra_kwargs = {
            'title': {'required': False},
            'criteria_ids': {'source': 'criteria', 'write_only': True},
            'learner_profile_ids': {'source': 'learner_profile', 'write_only': True},
            'atl_skills_ids': {'source': 'atl_skills', 'write_only': True},
            'strands_ids': {'source': 'strands', 'write_only': True},
            'aims_ids': {'source': 'aims', 'write_only': True},
            'global_context_id': {'source': 'global_context', 'write_only': True},
            'explorations_ids': {'source': 'explorations', 'write_only': True},
            'key_concepts_ids': {'source': 'key_concepts', 'write_only': True},
            'related_concepts_ids': {'source': 'related_concepts', 'write_only': True},
            'class_year_id': {'source': 'class_year', 'write_only': True},
            'authors_ids': {'source': 'authors', 'write_only': True, 'required': False},
            }
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        if 'subject_unit' in validated_data.keys():
            instance_subjects = SubjectLevelMYP.objects.filter(unit=instance)
            list_subjects = [x.get('subject').id for x in validated_data['subject_unit']]
            # Перебор имеющихся предметов в юните и удаление тех, которых нет в запросе
            for data in instance_subjects.values():
                if data['subject_id'] not in list_subjects:
                    SubjectLevelMYP.objects.filter(id=data['id']).delete()
            # Перебор предметов в запросе, добавление тех, которых нет в юните и редактирование уровня остальных
            new_subjects = []
            for data in validated_data['subject_unit']:
                if not instance_subjects.filter(subject=data.get('subject')).count():
                    new_subjects.append(SubjectLevelMYP(unit=instance, subject=data.get('subject'), level=data.get('level')))
                else:
                    SubjectLevelMYP.objects.filter(unit=instance, subject=data.get('subject')).update(level=data.get('level'))
            SubjectLevelMYP.objects.bulk_create(new_subjects)
            update_subject_list = SubjectLevelMYP.objects.filter(unit=instance)
            # Если предметов больше 1, то сделать юнит междисциплинарным
            if update_subject_list.count() > 1:
                UnitPlannerMYPID.objects.get_or_create(unitplan_myp=instance)
            else:
                UnitPlannerMYPID.objects.filter(unitplan_myp=instance).delete()
            validated_data.pop('subject_unit', None)
        return super().update(instance, validated_data)
    
class UnitMYPSerializerListCreate(serializers.ModelSerializer):
    key_concepts = KeyConceptSerializer(many=True, required=False)
    related_concepts = RelatedConceptSerializer(many=True, required=False)
    authors = ProfileTeacherSerializer(many=True, read_only=True)
    subjects = SubjectLevelMYPSerializer(many=True, source='subject_unit')
    class_year = ClassYearSerializer(read_only=True)
    global_context = GlobalContextSerializer(required=False)
    explorations = ExplorationToDevelopSerializer(many=True, required=False)
    criteria = CriterionSerializer(many=True, read_only=True)
    atlmapping = ATLMappingMYPSerializer(many=True, read_only=True)
    class Meta:
        model = UnitPlannerMYP
        fields = ['id', 'title', 'subjects', 'order', 'class_year', 'hours', 'key_concepts', 
                  'related_concepts', 'authors', 'global_context', 'explorations', 'statement_inquiry', 'criteria',
                  'criteria_ids', 'class_year_id', 'authors_ids', 'atlmapping', 
                  ]
        extra_kwargs = {
            'criteria_ids': {'source': 'criteria', 'write_only': True},
            'class_year_id': {'source': 'class_year', 'write_only': True},
            'authors_ids': {'source': 'authors', 'write_only': True},
            }
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        instance = UnitPlannerMYP.objects.create(
            title=validated_data['title'],
            hours=validated_data['hours'],
            class_year=validated_data['class_year'],
        )
        instance.criteria.set(validated_data['criteria'])
        instance.authors.set(validated_data['authors'])
        subjects = [SubjectLevelMYP(unit=instance, subject=data.get('subject'), level=data.get('level')) for data in validated_data['subject_unit']]
        create_subject_list = SubjectLevelMYP.objects.bulk_create(subjects)
        # Если предметов больше 1, то сделать юнит междисциплинарным
        if len(create_subject_list) > 1:
            UnitPlannerMYPID.objects.get_or_create(unitplan_myp=instance)
        else:
            UnitPlannerMYPID.objects.filter(unitplan_myp=instance).delete()
        return instance
        # return super().create(validated_data)
        
        