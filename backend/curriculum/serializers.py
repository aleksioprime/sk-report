from rest_framework import serializers
from curriculum.models import UnitPlannerMYP, KeyConcept, SubjectGroupIB, RelatedConcept, SubjectDirectionRC, Subject, \
    SubjectGroupIB, ClassYear, GlobalContext, ExplorationToDevelop, Aim, Objective, Strand, Criterion, Level, SkillATL, \
    ClusterATL, CategoryATL, LearnerProfileIB, InquiryQuestionMYP, ATLMappingMYP, ReflectionMYP, UnitPlannerMYPID, \
    DevelopProfileMYP, AchievementLevel, AcademicPlan, HoursSubjectInYear, SubjectGroupFGOS
from member.models import ProfileTeacher, User, Department
from django.db.models import Q

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
    last_name = serializers.CharField(source='user.last_name')
    first_name = serializers.CharField(source='user.first_name')
    middle_name = serializers.CharField(source='user.middle_name')
    class Meta:
        model = ProfileTeacher
        fields = '__all__'

class SubjectGroupIBSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectGroupIB
        fields = '__all__'

class SubjectGroupFGOSSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='get_type_display', read_only=True)
    class Meta:
        model = SubjectGroupFGOS
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display', read_only=True)
    type_name = serializers.CharField(source='get_type_display', read_only=True)
    group_ib = SubjectGroupIBSerializer()
    group_fgos = SubjectGroupFGOSSerializer()
    class Meta:
        model = Subject
        fields = '__all__'
    
class DepartmentSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many=True)
    class Meta:
        model = Department
        fields = '__all__'

class ClassYearSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display', read_only=True)
    program_name = serializers.CharField(source='get_program_display', read_only=True)
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
    class Meta:
        model = Criterion
        fields = ['id', 'letter', 'name_eng', 'name_rus', 'subject_group']

class LevelSerializer(serializers.ModelSerializer):
    # class_year = ClassYearSerializer(many=True, read_only=True)
    class Meta:
        model = Level
        fields = '__all__'
     
class StrandSerializer(serializers.ModelSerializer):
    letter_i = serializers.CharField(source='get_letter_display')
    criterion = CriterionSerializer(read_only=True)
    class Meta:
        model = Strand
        fields = ['id', 'number', 'letter', 'letter_i', 'name_eng', 'name_rus', 'criterion']

class AchievementLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementLevel
        fields = '__all__'

class ObjectiveSerializer(serializers.ModelSerializer):
    level = LevelSerializer(read_only=True)
    strand = StrandSerializer(read_only=True)
    achievelevel = AchievementLevelSerializer(read_only=True, many=True)
    class Meta:
        model = Objective
        fields = ['level', 'id', 'name_eng', 'name_rus', 'strand', 'achievelevel']

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
    type_text = serializers.CharField(source='get_type_display', read_only=True)
    class Meta:
        model = InquiryQuestionMYP
        fields = '__all__'
        
class ATLMappingMYPSerializer(serializers.ModelSerializer):
    atl = SkillATLSerializer(read_only=True)
    strand = StrandSerializer(read_only=True)
    class Meta:
        model = ATLMappingMYP
        fields = ['id', 'atl', 'atl_id', 'strand', 'strand_id', 'action', 'unitplan_myp']
        extra_kwargs = {
            'strand_id': {'source': 'strand', 'write_only': True},
            'atl_id': {'source': 'atl', 'write_only': True},
            'unitplan_myp': {'required': False},
        }
        
class DevelopProfileMYPSerializer(serializers.ModelSerializer):
    profile = LearnerProfileIBSerializer(read_only=True)
    class Meta:
        model = DevelopProfileMYP
        fields = ['id', 'profile', 'profile_id', 'description']
        extra_kwargs = {
            'profile_id': {'source': 'profile', 'write_only': True},
        }

class ReflectionMYPSerializer(serializers.ModelSerializer):
    author = ProfileTeacherSerializer(read_only=True)
    class Meta:
        model = ReflectionMYP
        fields = ['id', 'type', 'post', 'author', 'author_id']
        extra_kwargs = {
            'author_id': {'source': 'author', 'write_only': True},
        }

class UnitMYPSmallSerilizer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    class Meta:
        model = UnitPlannerMYP
        fields = ['subject']

class IDUSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField('get_subjects')
    unitplan_myp = UnitMYPSmallSerilizer(many=True, read_only=True)
    sb = SubjectSerializer(source='unitplan_myp.subject', many=True, read_only=True)
    class Meta:
        model = UnitPlannerMYPID
        fields = ['id', 'title', 'hours', 'subjects', 'unitplan_myp', 'sb']
    # TODO: сделать поле предметов без дополнительного сериализатора
    def get_subjects(self, instance):
        units = instance.unitplan_myp
        # print(type(units))
        # subjects = SubjectSerializer(instance.unitplan_myp.prefetch_related("subject"))
        return 'test'

class UnitPlannerMYPIDListCreate(serializers.ModelSerializer):
    class_year = ClassYearSerializer(read_only=True)
    key_concepts = KeyConceptSerializer(many=True, read_only=True)
    related_concepts = RelatedConceptSerializer(many=True, read_only=True)
    global_context = GlobalContextSerializer(read_only=True)
    explorations = ExplorationToDevelopSerializer(many=True, read_only=True)
    criteria = CriterionSerializer(many=True, read_only=True)
    aims = AimSerializer(many=True, read_only=True)
    strands = StrandSerializer(many=True, read_only=True)
    inquiry_questions = InQuestionMYPSerializer(many=True, required=False)
    reflections = ReflectionMYPSerializer(many=True, read_only=True)
    reflections_prior = ReflectionMYPSerializer(many=True, required=False, write_only=True)
    reflections_during = ReflectionMYPSerializer(many=True, required=False, write_only=True)
    reflections_after = ReflectionMYPSerializer(many=True, required=False, write_only=True)
    unitplan_myp = UnitMYPSmallSerilizer(many=True, required=False, read_only=True)
    class Meta:
        model = UnitPlannerMYPID
        # fields = '__all__'
        # extra_fields = ['class_year_id', 'global_context_id', 'explorations_ids', 'key_concepts_ids', 'related_concepts_ids',
        #                 'criteria_ids', 'aims_ids', 'strands_ids']
        fields = ['id', 'title', 'hours', 'purpose_integration', 'conceptual_understanding', 'statement_inquiry',
                  'tasks', 'introduction', 'learning_teaching', 'formative_assessment', 'summative_assessment', 
                  'differentiation',
                  'key_concepts', 'key_concepts_ids', 'related_concepts', 'related_concepts_ids',
                  'global_context', 'global_context_id', 'explorations', 'explorations_ids',
                  'purpose_integration', 'criteria', 'unitplan_myp', 'class_year', 'class_year_id',
                  'aims', 'strands', 'criteria_ids', 'aims_ids', 'strands_ids', 'unitplan_myp_ids',
                  'inquiry_questions', 'reflections', 'reflections_prior', 'reflections_during', 'reflections_after']
        extra_kwargs = {
            'class_year_id': {'source': 'class_year', 'write_only': True},
            'global_context_id': {'source': 'global_context', 'write_only': True},
            'explorations_ids': {'source': 'explorations', 'write_only': True},
            'key_concepts_ids': {'source': 'key_concepts', 'write_only': True},
            'related_concepts_ids': {'source': 'related_concepts', 'write_only': True},
            'criteria_ids': {'source': 'criteria', 'write_only': True},
            'aims_ids': {'source': 'aims', 'write_only': True},
            'strands_ids': {'source': 'strands', 'write_only': True},
            'unitplan_myp_ids': {'source': 'unitplan_myp', 'write_only': True },
        }
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        return super().create(validated_data)



class UnitMYPSerializerViewEdit(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    level = LevelSerializer(read_only=True)
    key_concepts = KeyConceptSerializer(many=True, read_only=True)
    related_concepts = RelatedConceptSerializer(many=True, read_only=True)
    authors = ProfileTeacherSerializer(many=True, read_only=True)
    class_year = ClassYearSerializer(read_only=True)
    global_context = GlobalContextSerializer(read_only=True)
    explorations = ExplorationToDevelopSerializer(many=True, read_only=True)
    aims = AimSerializer(many=True, read_only=True)
    strands = StrandSerializer(many=True, read_only=True)
    criteria = CriterionSerializer(many=True, read_only=True)
    inquiry_questions = InQuestionMYPSerializer(many=True, required=False)
    atl_mapping = ATLMappingMYPSerializer(many=True, required=False)
    learner_profile = DevelopProfileMYPSerializer(many=True, required=False)
    reflections = ReflectionMYPSerializer(many=True, read_only=True)
    reflections_prior = ReflectionMYPSerializer(many=True, required=False, write_only=True)
    reflections_during = ReflectionMYPSerializer(many=True, required=False, write_only=True)
    reflections_after = ReflectionMYPSerializer(many=True, required=False, write_only=True)
    interdisciplinary = UnitPlannerMYPIDListCreate(read_only=True)
    class Meta:
        model = UnitPlannerMYP
        fields = ['id', 'title', 'authors', 'order', 'class_year', 'hours', 
                  'key_concepts', 'related_concepts', 'conceptual_understanding', 'global_context', 'explorations', 'statement_inquiry',
                  'aims', 'strands', 'content', 'skills', 'learner_profile', 'international_mindedness',
                  'academic_integrity', 'language_development', 'infocom_technology', 'service_as_action', 'criteria', 'formative_assessment', 'summative_assessment_task',
                  'summative_assessment_soi', 'peer_self_assessment', 'standardization_moderation', 'prior_experiences', 'learning_experiences', 'teaching_strategies', 
                  'teaching_strategies', 'student_expectations', 'feedback', 'differentiation', 'criteria_ids',
                  'aims_ids', 'global_context_id', 'explorations_ids', 'key_concepts_ids', 'related_concepts_ids', 'class_year_id', 'authors_ids', 
                  'inquiry_questions', 'atl_mapping', 'reflections', 'strands_ids','resources', 'subject', 'subject_id', 'level', 'level_id', 
                  'reflections_prior', 'reflections_during', 'reflections_after', 'interdisciplinary', 'interdisciplinary_id',
                  ]
        extra_kwargs = {
            'title': {'required': False},
            'criteria_ids': {'source': 'criteria', 'write_only': True},
            'atl_skills_ids': {'source': 'atl_skills', 'write_only': True},
            'strands_ids': {'source': 'strands', 'write_only': True},
            'aims_ids': {'source': 'aims', 'write_only': True},
            'global_context_id': {'source': 'global_context', 'write_only': True},
            'explorations_ids': {'source': 'explorations', 'write_only': True},
            'key_concepts_ids': {'source': 'key_concepts', 'write_only': True},
            'related_concepts_ids': {'source': 'related_concepts', 'write_only': True},
            'class_year_id': {'source': 'class_year', 'write_only': True},
            'subject_id': {'source': 'subject', 'write_only': True},
            'level_id': {'source': 'level', 'write_only': True},
            'authors_ids': {'source': 'authors', 'write_only': True, 'required': False},
            'interdisciplinary_id': {'source': 'interdisciplinary', 'write_only': True},
            }
    def create_or_update_inquestions(self, inquestions):
        inquestion_ids = []
        for inquestion in inquestions:
            inquestion_instance, created = InquiryQuestionMYP.objects.update_or_create(pk=inquestion.get('id'), defaults=inquestion)
            inquestion_ids.append(inquestion_instance.pk)
        return inquestion_ids
    def create_or_update_atl(self, atls):
        atl_ids = []
        for atl in atls:
            atl_instance, created = ATLMappingMYP.objects.update_or_create(pk=atl.get('id'), defaults=atl)
            atl_ids.append(atl_instance.pk)
        return atl_ids
    def create_or_update_profile(self, profiles):
        profile_ids = []
        for profile in profiles:
            profile_instance, created = DevelopProfileMYP.objects.update_or_create(pk=profile.get('id'), defaults=profile)
            profile_ids.append(profile_instance.pk)
        return profile_ids
    def create_or_update_reflection(self, reflections):
        reflection_ids = []
        for reflection in reflections:
            reflection_instance, created = ReflectionMYP.objects.update_or_create(pk=reflection.get('id'), defaults=reflection)
            reflection_ids.append(reflection_instance.pk)
        return reflection_ids
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        inquiry_questions = validated_data.pop('inquiry_questions', None)
        if inquiry_questions is not None:
            original = InquiryQuestionMYP.objects.filter(unitplan_myp=instance)
            original.filter(~Q(id__in=[item.get('id') for item in inquiry_questions if 'id' in item])).delete()
            instance.inquiry_questions.set(self.create_or_update_inquestions(inquiry_questions))
            instance.save()
        atl_mapping = validated_data.pop('atl_mapping', None)
        if atl_mapping is not None:
            original = ATLMappingMYP.objects.filter(unitplan_myp=instance)
            original.filter(~Q(id__in=[item.get('id') for item in atl_mapping if 'id' in item])).delete()
            instance.atl_mapping.set(self.create_or_update_atl(atl_mapping))
            instance.save()
        learner_profile = validated_data.pop('learner_profile', None)
        if learner_profile is not None:
            original = DevelopProfileMYP.objects.filter(unitplan_myp=instance)
            original.filter(~Q(id__in=[item.get('id') for item in learner_profile if 'id' in item])).delete()
            instance.learner_profile.set(self.create_or_update_profile(learner_profile))
            instance.save()
        reflections_prior = validated_data.pop('reflections_prior', None)
        if reflections_prior is not None:
            original = ReflectionMYP.objects.filter(unitplan_myp=instance, type='Prior')
            original.filter(~Q(id__in=[item.get('id') for item in reflections_prior if 'id' in item])).delete()
            for item in self.create_or_update_reflection(reflections_prior):
                instance.reflections.add(item)
            instance.save()
        reflections_during = validated_data.pop('reflections_during', None)
        if reflections_during is not None:
            original = ReflectionMYP.objects.filter(unitplan_myp=instance, type='During')
            original.filter(~Q(id__in=[item.get('id') for item in reflections_during if 'id' in item])).delete()
            for item in self.create_or_update_reflection(reflections_during):
                instance.reflections.add(item)
            instance.save()
        reflections_after = validated_data.pop('reflections_after', None)
        if reflections_after is not None:
            original = ReflectionMYP.objects.filter(unitplan_myp=instance, type='After')
            original.filter(~Q(id__in=[item.get('id') for item in reflections_after if 'id' in item])).delete()
            for item in self.create_or_update_reflection(reflections_after):
                instance.reflections.add(item)
            instance.save()
        return super().update(instance, validated_data)
    def to_representation(self, instance):
        result = super(UnitMYPSerializerViewEdit, self).to_representation(instance)
        count_field = 0
        for field in instance._meta.get_fields():
            if field.name not in ['sumwork', 'order', 'interdisciplinary']:
                if field.name == 'reflections':
                    reflection_types = set([item.type for item in field.value_from_object(instance)])
                    count_field += len(reflection_types)
                elif field.value_from_object(instance):
                    count_field += 1
        result['fullness'] = round(count_field / (len(instance._meta.get_fields()) - 1) * 100)
        return result

class UnitMYPSerializerListCreate(serializers.ModelSerializer):
    subject = SubjectSerializer(required=False)
    level = LevelSerializer(required=False, read_only=True)
    class_year = ClassYearSerializer(read_only=True)
    key_concepts = KeyConceptSerializer(many=True, required=False)
    related_concepts = RelatedConceptSerializer(many=True, required=False)
    authors = ProfileTeacherSerializer(many=True, read_only=True)
    global_context = GlobalContextSerializer(required=False)
    explorations = ExplorationToDevelopSerializer(many=True, required=False)
    criteria = CriterionSerializer(many=True, read_only=True)
    atl_mapping = ATLMappingMYPSerializer(many=True, read_only=True)
    interdisciplinary = IDUSerializer(read_only=True)
    class Meta:
        model = UnitPlannerMYP
        fields = ['id', 'title', 'order', 'subject', 'subject_id', 'level', 'level_id', 'class_year', 'hours', 'key_concepts', 
                  'related_concepts', 'authors', 'global_context', 'explorations', 'statement_inquiry', 'criteria',
                  'criteria_ids', 'class_year_id', 'authors_ids', 'atl_mapping', 'interdisciplinary'
                  ]
        extra_kwargs = {
            'criteria_ids': {'source': 'criteria', 'write_only': True},
            'subject_id': {'source': 'subject', 'write_only': True},
            'level_id': {'source': 'level', 'write_only': True},
            'class_year_id': {'source': 'class_year', 'write_only': True},
            'authors_ids': {'source': 'authors', 'write_only': True},
            }
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        return super().create(validated_data)
    def to_representation(self, instance):
        result = super(UnitMYPSerializerListCreate, self).to_representation(instance)
        current_data = UnitPlannerMYP.objects.filter(pk=instance.id).first()
        count_field = 0
        for field in current_data._meta.get_fields():
            if field.name not in ['sumwork', 'order', 'interdisciplinary']: 
                if field.name == 'reflections':
                    reflection_types = set([item.type for item in field.value_from_object(instance)])
                    count_field += len(reflection_types)
                elif field.value_from_object(instance):
                    count_field += 1
        result['fullness'] = round(count_field / (len(current_data._meta.get_fields()) - 1) * 100)
        return result

class UnitPlannerMYPIDViewEdit(serializers.ModelSerializer):
    class_year = ClassYearSerializer(read_only=True)
    key_concepts = KeyConceptSerializer(many=True, read_only=True)
    related_concepts = RelatedConceptSerializer(many=True, read_only=True)
    global_context = GlobalContextSerializer(read_only=True)
    explorations = ExplorationToDevelopSerializer(many=True, read_only=True)
    criteria = CriterionSerializer(many=True, read_only=True)
    aims = AimSerializer(many=True, read_only=True)
    strands = StrandSerializer(many=True, read_only=True)
    inquiry_questions = InQuestionMYPSerializer(many=True, required=False)
    reflections = ReflectionMYPSerializer(many=True, read_only=True)
    reflections_prior = ReflectionMYPSerializer(many=True, required=False, write_only=True)
    reflections_during = ReflectionMYPSerializer(many=True, required=False, write_only=True)
    reflections_after = ReflectionMYPSerializer(many=True, required=False, write_only=True)
    unitplan_myp = UnitMYPSerializerListCreate(many=True, required=False, read_only=True)
    class Meta:
        model = UnitPlannerMYPID
        # fields = '__all__'
        # extra_fields = ['class_year_id', 'global_context_id', 'explorations_ids', 'key_concepts_ids', 'related_concepts_ids',
        #                 'criteria_ids', 'aims_ids', 'strands_ids']
        fields = ['id', 'title', 'hours', 'purpose_integration', 'conceptual_understanding', 'statement_inquiry',
                  'tasks', 'introduction', 'learning_teaching', 'formative_assessment', 'summative_assessment', 
                  'differentiation',
                  'key_concepts', 'key_concepts_ids', 'related_concepts', 'related_concepts_ids',
                  'global_context', 'global_context_id', 'explorations', 'explorations_ids',
                  'purpose_integration', 'criteria', 'unitplan_myp', 'unitplan_myp_ids', 'class_year', 'class_year_id',
                  'aims', 'strands', 'criteria_ids', 'aims_ids', 'strands_ids',
                  'inquiry_questions', 'reflections', 'reflections_prior', 'reflections_during', 'reflections_after']
        extra_kwargs = {
            'title': {'required': False},
            'class_year_id': {'source': 'class_year', 'write_only': True},
            'global_context_id': {'source': 'global_context', 'write_only': True},
            'explorations_ids': {'source': 'explorations', 'write_only': True},
            'key_concepts_ids': {'source': 'key_concepts', 'write_only': True},
            'related_concepts_ids': {'source': 'related_concepts', 'write_only': True},
            'criteria_ids': {'source': 'criteria', 'write_only': True},
            'aims_ids': {'source': 'aims', 'write_only': True},
            'strands_ids': {'source': 'strands', 'write_only': True},
            'unitplan_myp_ids': {'source': 'unitplan_myp', 'write_only': True, 'required': False},
        }
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        return super().create(validated_data)
    def create_or_update_inquestions(self, inquestions):
        inquestion_ids = []
        for inquestion in inquestions:
            inquestion_instance, created = InquiryQuestionMYP.objects.update_or_create(pk=inquestion.get('id'), defaults=inquestion)
            inquestion_ids.append(inquestion_instance.pk)
        return inquestion_ids
    def create_or_update_reflection(self, reflections):
        reflection_ids = []
        for reflection in reflections:
            reflection_instance, created = ReflectionMYP.objects.update_or_create(pk=reflection.get('id'), defaults=reflection)
            reflection_ids.append(reflection_instance.pk)
        return reflection_ids
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        inquiry_questions = validated_data.pop('inquiry_questions', None)
        if inquiry_questions is not None:
            original = InquiryQuestionMYP.objects.filter(idu=instance)
            original.filter(~Q(id__in=[item.get('id') for item in inquiry_questions if 'id' in item])).delete()
            instance.inquiry_questions.set(self.create_or_update_inquestions(inquiry_questions))
            instance.save()
        reflections_prior = validated_data.pop('reflections_prior', None)
        if reflections_prior is not None:
            original = ReflectionMYP.objects.filter(idu=instance, type='Prior')
            original.filter(~Q(id__in=[item.get('id') for item in reflections_prior if 'id' in item])).delete()
            for item in self.create_or_update_reflection(reflections_prior):
                instance.reflections.add(item)
            instance.save()
        reflections_during = validated_data.pop('reflections_during', None)
        if reflections_during is not None:
            original = ReflectionMYP.objects.filter(idu=instance, type='During')
            original.filter(~Q(id__in=[item.get('id') for item in reflections_during if 'id' in item])).delete()
            for item in self.create_or_update_reflection(reflections_during):
                instance.reflections.add(item)
            instance.save()
        reflections_after = validated_data.pop('reflections_after', None)
        if reflections_after is not None:
            original = ReflectionMYP.objects.filter(idu=instance, type='After')
            original.filter(~Q(id__in=[item.get('id') for item in reflections_after if 'id' in item])).delete()
            for item in self.create_or_update_reflection(reflections_after):
                instance.reflections.add(item)
            instance.save()
        return super().update(instance, validated_data)
    def to_representation(self, instance):
        result = super(UnitPlannerMYPIDViewEdit, self).to_representation(instance)
        count_field = 0
        for field in instance._meta.get_fields():
            if field.name not in ['unitplan_myp']:
                if field.name == 'reflections':
                    reflection_types = set([item.type for item in field.value_from_object(instance)])
                    count_field += len(reflection_types)
                elif field.value_from_object(instance):
                    count_field += 1
        result['fullness'] = round(count_field / (len(instance._meta.get_fields()) + 1) * 100)
        return result

class AchievementLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementLevel
        fields = '__all__'

class ObjectiveViewSerializer(serializers.ModelSerializer):
    achievelevel = AchievementLevelSerializer(many=True, read_only=True)
    level = LevelSerializer(read_only=True)
    class Meta:
        model = Objective
        fields = '__all__'

class StrandViewSerializer(serializers.ModelSerializer):
    objective = ObjectiveViewSerializer(many=True, read_only=True)
    letter_i = serializers.CharField(source='get_letter_display', read_only=True)
    class Meta:
        model = Strand
        fields = '__all__'

class CriterionViewSerializer(serializers.ModelSerializer):
    subject_group = SubjectGroupIBSerializer(read_only=True)
    strand = StrandViewSerializer(many=True, read_only=True)
    class Meta:
        model = Criterion
        fields = '__all__'


#################
# УЧЕБНЫЕ ПЛАНЫ #
#################

class HoursSubjectInYearSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    years = ClassYearSerializer(many=True, read_only=True)
    class Meta:
        model = HoursSubjectInYear
        fields = ['id', 'years', 'subject', 'hours', 'subject_id', 'academic_plan_id', 'years_ids']
        extra_kwargs = {
            'subject_id': {'source': 'subject', 'write_only': True},
            'academic_plan_id': {'source': 'academic_plan', 'write_only': True},
            'years_ids': {'source': 'years', 'write_only': True},
            }
    def update(self, instance, validated_data):
        print('Валидированные данные: ', validated_data)
        return super().update(instance, validated_data)
    def create(self, validated_data):
        print('Валидированные данные: ', validated_data)
        return super().create(validated_data)

class AcademicPlanSerializer(serializers.ModelSerializer):
    subject_year = HoursSubjectInYearSerializer(many=True, read_only=True)
    class Meta:
        model = AcademicPlan
        fields = '__all__'
