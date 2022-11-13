from django.shortcuts import render
from curriculum.models import UnitPlannerMYP, ClassYear, Subject, Criterion
from member.models import ProfileTeacher, Department
from curriculum.serializers import UnitMYPSerializerViewEdit, UnitMYPSerializerListCreate, ProfileTeacherSerializer, ClassYearSerializer, \
    SubjectSerializer, CriterionSerializer, DepartmentSerializer
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
        return super().update(request, pk=None, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        print(request.data)
        unitplan_myp = request.data.get('select_unitplat_myp')
        if len(unitplan_myp):
            UnitPlannerMYP.objects.filter(id__in=unitplan_myp).delete()
            return Response({'DELETE': "Success"})
        return Response({'DELETE': "Error! Not found UnitPlan MYP"})

# Набор методов для просмотра списка записей и добавления новой записи UnitPlannerMYP
class UnitPlannerMYPListCreate(viewsets.ModelViewSet):
    queryset = UnitPlannerMYP.objects.all()
    serializer_class = UnitMYPSerializerListCreate
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)
    
    
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
        subject = self.request.query_params.get("subject", None)
        if not subject:
            return Criterion.objects.all()
        return Criterion.objects.filter(subject_group__subject=subject)