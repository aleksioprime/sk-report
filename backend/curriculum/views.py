from django.shortcuts import render
from curriculum.models import UnitPlannerMYP, ClassYear, Subject, Criterion, LearnerProfileIB, SkillATL, Objective, Aim, GlobalContext, \
    ExplorationToDevelop, KeyConcept, RelatedConcept, InquiryQuestionMYP, ATLMappingMYP, ReflectionMYP
from member.models import ProfileTeacher, Department
from curriculum.serializers import UnitMYPSerializerViewEdit, UnitMYPSerializerListCreate, ProfileTeacherSerializer, ClassYearSerializer, \
    SubjectSerializer, CriterionSerializer, DepartmentSerializer, LearnerProfileIBSerializer, SkillATLSerializer, ObjectiveSerializer, \
    AimSerializer, GlobalContextSerializer, ExplorationToDevelopSerializer, KeyConceptSerializer, RelatedConceptSerializer, InQuestionMYPSerializer, \
    ATLMappingMYPSerializer, ReflectionMYPSerializer
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
        print(request.data)
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
        return super().create(request, *args, **kwargs)
    def get_queryset(self):
        department = self.request.query_params.get("department", None)
        teacher = self.request.query_params.get("teacher", None)
        units_myp = UnitPlannerMYP.objects.all()
        if department:
            units_myp = units_myp.filter(subject__department=department)
        if teacher:
            units_myp = units_myp.filter(authors__in=[teacher])
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
    
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    def get_queryset(self):
        subjects = Subject.objects.all()
        level = self.request.query_params.get("level", None)
        type_subject = self.request.query_params.get("type", None)
        if level:
            subjects = subjects.filter(group_fgos__level=level)
        if level:
            subjects = subjects.filter(type_subject=type_subject)
        return subjects
    
class CriterionViewSet(viewsets.ModelViewSet):
    queryset = Criterion.objects.all()
    serializer_class = CriterionSerializer
    def get_queryset(self):
        criteria = Criterion.objects.all()
        subject = self.request.query_params.get("subject", None)
        if subject:
            criteria = criteria.filter(subject_group__subject=subject)
        return criteria
    
class LearnerProfileIBViewSet(viewsets.ModelViewSet):
    queryset = LearnerProfileIB.objects.all()
    serializer_class = LearnerProfileIBSerializer
    
class SkillATLViewSet(viewsets.ModelViewSet):
    queryset = SkillATL.objects.all()
    serializer_class = SkillATLSerializer
    
class ObjectiveViewSet(viewsets.ModelViewSet):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer
    def get_queryset(self):
        subject = self.request.query_params.get("subject", None)
        class_year = self.request.query_params.get("class_year", None)
        criteria = self.request.query_params.get("criteria", None)
        print(subject, class_year, criteria)
        objectives = Objective.objects.all()
        if subject:
            objectives = objectives.filter(strand__criterion__subject_group__subject=subject)
            print(objectives)
        if class_year:
            objectives = objectives.filter(level__years__in=class_year)
            print(objectives)
        if criteria:
            objectives = objectives.filter(strand__criterion__in=criteria.split(','))
            print(objectives)
        return objectives
    
class AimViewSet(viewsets.ModelViewSet):
    queryset = Aim.objects.all()
    serializer_class = AimSerializer
    def get_queryset(self):
        aims = Aim.objects.all()
        subject = self.request.query_params.get("subject", None)
        if subject:
            aims = aims.filter(subject_group__subject=subject)
        return aims
    
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
    
class KeyConceptViewSet(viewsets.ModelViewSet):
    queryset = KeyConcept.objects.all()
    serializer_class = KeyConceptSerializer
    
class RelatedConceptViewSet(viewsets.ModelViewSet):
    queryset = RelatedConcept.objects.all()
    serializer_class = RelatedConceptSerializer
    def get_queryset(self):
        subject = self.request.query_params.get("subject", None)
        print(subject)
        rconcepts = RelatedConcept.objects.all()
        if subject:
            rconcepts = rconcepts.filter(subdirections__subject_group__subject__in=[subject]).distinct()
        return rconcepts
    
class InQuestionMYPViewSet(viewsets.ModelViewSet):
    queryset = InquiryQuestionMYP.objects.all()
    serializer_class = InQuestionMYPSerializer
    def get_queryset(self):
        inquestions = InquiryQuestionMYP.objects.all()
        unit = self.request.query_params.get("unit", None)
        if unit:
            inquestions = inquestions.filter(planner=unit)
        return inquestions
    
    
class ATLMappingMYPViewSet(viewsets.ModelViewSet):
    queryset = ATLMappingMYP.objects.all()
    serializer_class = ATLMappingMYPSerializer
    def get_queryset(self):
        mapping = ATLMappingMYP.objects.all()
        unit = self.request.query_params.get("unit", None)
        if unit:
            mapping = mapping.filter(planner=unit)
        return mapping
    
class ReflectionMYPViewSet(viewsets.ModelViewSet):
    queryset = ReflectionMYP.objects.all()
    serializer_class = ReflectionMYPSerializer
    def get_queryset(self):
        reflections = ReflectionMYP.objects.all()
        unit = self.request.query_params.get("unit", None)
        if unit:
            reflections = reflections.filter(planner=unit)
        return reflections