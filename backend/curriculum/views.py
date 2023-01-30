from django.shortcuts import render
from curriculum.models import UnitPlannerMYP, ClassYear, Subject, Criterion, LearnerProfileIB, SkillATL, Objective, Aim, GlobalContext, \
    ExplorationToDevelop, KeyConcept, RelatedConcept, InquiryQuestionMYP, ATLMappingMYP, ReflectionMYP, Strand, Level, UnitPlannerMYPID, SubjectLevelMYP
from member.models import ProfileTeacher, Department
from curriculum.serializers import UnitMYPSerializerViewEdit, UnitMYPSerializerListCreate, ProfileTeacherSerializer, ClassYearSerializer, \
    SubjectSerializer, CriterionSerializer, DepartmentSerializer, LearnerProfileIBSerializer, SkillATLSerializer, ObjectiveSerializer, \
    AimSerializer, GlobalContextSerializer, ExplorationToDevelopSerializer, KeyConceptSerializer, RelatedConceptSerializer, InQuestionMYPSerializer, \
    ATLMappingMYPSerializer, ReflectionMYPSerializer, StrandSerializer, LevelSerializer, UnitPlannerMYPIDSerializer, SubjectLevelMYPSerializer
from rest_framework import viewsets
from rest_framework.response import Response

# Набор методов для просмотра, редактирования и удаления текущей записи UnitPlannerMYP
class UnitPlannerMYPViewEdit(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = UnitPlannerMYP.objects.all()
    serializer_class = UnitMYPSerializerViewEdit
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk=None, *args, **kwargs)
    def update(self, request, pk=None, *args, **kwargs):
        print('Переданные данные: ', request.data)
        return super().update(request, pk=None, *args, **kwargs)
    def destroy(self, request, pk=None, *args, **kwargs):
        print(request.data)
        return super().destroy(request, pk=None, *args, **kwargs)

# Набор методов для просмотра списка записей и добавления новой записи UnitPlannerMYP
class UnitPlannerMYPListCreate(viewsets.ModelViewSet):
    queryset = UnitPlannerMYP.objects.all()
    serializer_class = UnitMYPSerializerListCreate
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        print('Переданные данные: ', request.data)
        return super().create(request, *args, **kwargs)
    def get_queryset(self):
        department = self.request.query_params.get("department", None)
        teacher = self.request.query_params.get("teacher", None)
        subjects = self.request.query_params.get("subject", None)
        units_myp = UnitPlannerMYP.objects.all()
        if department:
            units_myp = units_myp.filter(subjects__department=department)
        if teacher:
            units_myp = units_myp.filter(authors__in=[teacher])
        if subjects:
            units_myp = units_myp.filter(subjects__in=[subjects])
        return units_myp
       
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = ProfileTeacher.objects.all()
    serializer_class = ProfileTeacherSerializer
    
class ClassYearViewSet(viewsets.ModelViewSet):
    queryset = ClassYear.objects.all()
    serializer_class = ClassYearSerializer
    def get_queryset(self):
        program = self.request.query_params.get("program", None)
        if not program:
            return ClassYear.objects.all()
        return ClassYear.objects.filter(program=program)

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    def get_queryset(self):
        subjects = Subject.objects.all()
        level = self.request.query_params.get("level", None)
        type_subject = self.request.query_params.get("type", None)
        if level:
            subjects = subjects.filter(group_fgos__level=level)
        if type_subject:
            subjects = subjects.filter(type_subject=type_subject)
        return subjects
    
class SubjectLevelMYPViewSet(viewsets.ModelViewSet):
    queryset = SubjectLevelMYP.objects.all()
    serializer_class = SubjectLevelMYPSerializer
    def get_queryset(self):
        subject_level = SubjectLevelMYP.objects.all()
        unit = self.request.query_params.get("unit", None)
        if unit:
            subject_level = subject_level.filter(unit=unit)
        return subject_level

class KeyConceptViewSet(viewsets.ModelViewSet):
    queryset = KeyConcept.objects.all()
    serializer_class = KeyConceptSerializer
    
class RelatedConceptViewSet(viewsets.ModelViewSet):
    queryset = RelatedConcept.objects.all()
    serializer_class = RelatedConceptSerializer
    def get_queryset(self):
        subjects = self.request.query_params.get("subjects", None)
        # print(subjects)
        rconcepts = RelatedConcept.objects.all()
        if subjects:
            rconcepts = rconcepts.filter(subject_directions__subject_group__subject__in=subjects.split(',')).distinct()
        return rconcepts

class GlobalContextViewSet(viewsets.ModelViewSet):
    queryset = GlobalContext.objects.all()
    serializer_class = GlobalContextSerializer

class ExplorationToDevelopViewSet(viewsets.ModelViewSet):
    queryset = ExplorationToDevelop.objects.all()
    serializer_class = ExplorationToDevelopSerializer
    def get_queryset(self):
        gcontext = self.request.query_params.get("gcontext", None)
        if not gcontext:
            return ExplorationToDevelop.objects.all()
        return ExplorationToDevelop.objects.filter(gcontext=gcontext)

class InQuestionMYPViewSet(viewsets.ModelViewSet):
    queryset = InquiryQuestionMYP.objects.all()
    serializer_class = InQuestionMYPSerializer
    def get_queryset(self):
        inquestions = InquiryQuestionMYP.objects.all()
        unit = self.request.query_params.get("unit", None)
        if unit:
            inquestions = inquestions.filter(planner=unit)
        return inquestions

class AimViewSet(viewsets.ModelViewSet):
    queryset = Aim.objects.all()
    serializer_class = AimSerializer
    def get_queryset(self):
        aims = Aim.objects.all()
        subjects = self.request.query_params.get("subjects", None)
        group = self.request.query_params.get("group", None)
        print(subjects)
        if subjects:
            aims = aims.filter(subject_group__subject__in=subjects.split(','))
        if group:
            aims = aims.filter(subject_group=group)
        return aims

class CriterionViewSet(viewsets.ModelViewSet):
    queryset = Criterion.objects.all()
    serializer_class = CriterionSerializer
    def get_queryset(self):
        criteria = Criterion.objects.all()
        subjects = self.request.query_params.get("subjects", None)
        group = self.request.query_params.get("group", None)
        if subjects:
            criteria = criteria.filter(subject_group__subject__in=subjects.split(','))
        if group:
            criteria = criteria.filter(subject_group=group)
        return criteria

class StrandViewSet(viewsets.ModelViewSet):
    queryset = Strand.objects.all()
    serializer_class = StrandSerializer
    def get_queryset(self):
        subjects = self.request.query_params.get("subjects", None)
        criteria = self.request.query_params.get("criteria", None)
        group = self.request.query_params.get("group", None)
        # print(subjects, criteria)
        strands = Strand.objects.all()
        if subjects:
            strands = strands.filter(criterion__subject_group__subject__in=subjects.split(','))
        if group:
            strands = strands.filter(criterion__subject_group=group)
        if criteria:
            strands = strands.filter(criterion__in=criteria.split(','))
        return strands
    
class SkillATLViewSet(viewsets.ModelViewSet):
    queryset = SkillATL.objects.all()
    serializer_class = SkillATLSerializer

class ATLMappingMYPViewSet(viewsets.ModelViewSet):
    queryset = ATLMappingMYP.objects.all()
    serializer_class = ATLMappingMYPSerializer
    def get_queryset(self):
        mapping = ATLMappingMYP.objects.all()
        unit = self.request.query_params.get("unit", None)
        if unit:
            mapping = mapping.filter(planner=unit)
        return mapping

class LearnerProfileIBViewSet(viewsets.ModelViewSet):
    queryset = LearnerProfileIB.objects.all()
    serializer_class = LearnerProfileIBSerializer
    
class ObjectiveViewSet(viewsets.ModelViewSet):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer
    def get_queryset(self):
        subjects = self.request.query_params.get("subjects", None)
        class_year = self.request.query_params.get("class_year", None)
        criteria = self.request.query_params.get("criteria", None)
        objectives = Objective.objects.all()
        if subjects:
            objectives = objectives.filter(strand__criterion__subject_group__subject__=subjects.split(','))
        if class_year:
            objectives = objectives.filter(level__years__in=class_year)
        if criteria:
            objectives = objectives.filter(strand__criterion__in=criteria.split(','))
        return objectives
    
class ReflectionMYPViewSet(viewsets.ModelViewSet):
    queryset = ReflectionMYP.objects.all()
    serializer_class = ReflectionMYPSerializer
    def get_queryset(self):
        reflections = ReflectionMYP.objects.all()
        unit = self.request.query_params.get("unit", None)
        if unit:
            reflections = reflections.filter(planner=unit)
        return reflections

class UnitPlannerMYPIDViewSet(viewsets.ModelViewSet):
    queryset = UnitPlannerMYPID.objects.all()
    serializer_class = UnitPlannerMYPIDSerializer
    def get_queryset(self):
        unit_inter = UnitPlannerMYPID.objects.all()
        unit = self.request.query_params.get("unit", None)
        if unit:
            unit_inter = unit_inter.filter(unitplan_myp=unit)
        return unit_inter