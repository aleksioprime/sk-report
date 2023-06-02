from curriculum.models import UnitPlannerMYP, ClassYear, Subject, Criterion, LearnerProfileIB, SkillATL, Objective, Aim, GlobalContext, \
    ExplorationToDevelop, KeyConcept, RelatedConcept, InquiryQuestionMYP, ATLMappingMYP, ReflectionMYP, Strand, Level, UnitPlannerMYPID, \
        DevelopProfileMYP, AcademicPlan, HoursSubjectInYear, SubjectGroupIB, SubjectGroupFGOS
from member.models import ProfileTeacher, Department
from curriculum.serializers import UnitMYPSerializerViewEdit, UnitMYPSerializerListCreate, ProfileTeacherSerializer, ClassYearSerializer, \
    SubjectSerializer, CriterionSerializer, DepartmentSerializer, LearnerProfileIBSerializer, SkillATLSerializer, ObjectiveSerializer, \
    AimSerializer, GlobalContextSerializer, ExplorationToDevelopSerializer, KeyConceptSerializer, RelatedConceptSerializer, InQuestionMYPSerializer, \
    ATLMappingMYPSerializer, ReflectionMYPSerializer, StrandSerializer, LevelSerializer, UnitPlannerMYPIDListCreate, UnitPlannerMYPIDViewEdit, \
        CriterionViewSerializer, AcademicPlanSerializer, HoursSubjectInYearSerializer, SubjectGroupIBSerializer, SubjectGroupFGOSSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from docxtpl import DocxTemplate
from rest_framework.views import APIView
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q

import os
from htmldocx import HtmlToDocx
from docx import Document
import tempfile


class AcademicPlanViewSet(viewsets.ModelViewSet):
    queryset = AcademicPlan.objects.all()
    serializer_class = AcademicPlanSerializer
    def get_queryset(self):
        study_year = self.request.query_params.get("study_year", None)
        academic_plan = AcademicPlan.objects.all()
        if study_year:
            academic_plan = academic_plan.filter(study_year=study_year)
        return academic_plan

class HoursSubjectInYearViewSet(viewsets.ModelViewSet):
    queryset = HoursSubjectInYear.objects.all()
    serializer_class = HoursSubjectInYearSerializer

class CriteriaGroupsViewSet(viewsets.ModelViewSet):
    queryset = SubjectGroupIB.objects.all()
    serializer_class = SubjectGroupIBSerializer

class SubjectGroupFGOSViewSet(viewsets.ModelViewSet):
    queryset = SubjectGroupFGOS.objects.all()
    serializer_class = SubjectGroupFGOSSerializer
    
# Набор методов для просмотра, редактирования и удаления текущей записи UnitPlannerMYP
class UnitPlannerMYPViewEdit(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = UnitPlannerMYP.objects.all()
    serializer_class = UnitMYPSerializerViewEdit
    def retrieve(self, request, pk=None, *args, **kwargs):
        return super().retrieve(request, pk=None, *args, **kwargs)
    def update(self, request, pk=None, *args, **kwargs):
        print('Переданные данные для обновления: ', request.data)
        return super().update(request, pk=None, *args, **kwargs)
    def destroy(self, request, pk=None, *args, **kwargs):
        print('Переданные данные для удаления: ', pk)
        ReflectionMYP.objects.filter(unitplan_myp=pk).delete()
        InquiryQuestionMYP.objects.filter(unitplan_myp=pk).delete()
        DevelopProfileMYP.objects.filter(unitplan_myp=pk).delete()
        ATLMappingMYP.objects.filter(unitplan_myp=pk).delete()
        return super().destroy(request, pk=None, *args, **kwargs)

class UnitsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50

# Набор методов для просмотра списка записей и добавления новой записи UnitPlannerMYP
class UnitPlannerMYPListCreate(viewsets.ModelViewSet):
    queryset = UnitPlannerMYP.objects.all()
    serializer_class = UnitMYPSerializerListCreate
    pagination_class = UnitsSetPagination
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        print('Переданные данные: ', request.data)
        return super().create(request, *args, **kwargs)
    def get_queryset(self):
        department = self.request.query_params.get("department", None)
        teacher = self.request.query_params.get("teacher", None)
        subject = self.request.query_params.get("subject", None)
        years = self.request.query_params.getlist("years[]", None)
        print('Переданные параметры: ', self.request.query_params)
        units_myp = UnitPlannerMYP.objects.all()
        if department:
            units_myp = units_myp.filter(subject__department=department)
        if teacher:
            units_myp = units_myp.filter(authors__in=[teacher])
        if subject:
            units_myp = units_myp.filter(subject=subject)
        if years:
            units_myp = units_myp.filter(class_year__in=years)
        return units_myp

# Получение списка юнитов
class UnitPlannerMYPList(viewsets.ModelViewSet):
    queryset = UnitPlannerMYP.objects.all()
    serializer_class = UnitMYPSerializerListCreate
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def get_queryset(self):
        units_myp = UnitPlannerMYP.objects.all()
        year = self.request.query_params.get("year", None)
        subject = self.request.query_params.get("subject", None)
        interdisciplinary = self.request.query_params.get("interdisciplinary", None)
        if year:
            units_myp = units_myp.filter(class_year__in=year)
        if subject:
            units_myp = units_myp.filter(subject=subject)
        if interdisciplinary == 'no':
            units_myp = units_myp.filter(interdisciplinary=None)
        elif interdisciplinary:
            units_myp = units_myp.filter(Q(interdisciplinary=None) | Q(interdisciplinary=interdisciplinary))
        print(units_myp)
        return units_myp

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    
class ClassYearViewSet(viewsets.ModelViewSet):
    queryset = ClassYear.objects.all()
    serializer_class = ClassYearSerializer
    def get_queryset(self):
        class_year = ClassYear.objects.all()
        program = self.request.query_params.get("program", None)
        level = self.request.query_params.get("level", None)
        subject = self.request.query_params.get("subject", None)
        department = self.request.query_params.getlist("department", None)
        author = self.request.query_params.get("author", None)
        teacher = self.request.query_params.get("teacher", None)
        if program:
            class_year = class_year.filter(program=program)
        if level:
            class_year = class_year.filter(level=level)
        if author:
            class_year = class_year.filter(unitplan_myp__authors__in=[author]).distinct()
        if subject:
            class_year = class_year.filter(unitplan_myp__subject=subject).distinct()
        if teacher:
            class_year = class_year.filter(group__workload__teacher=teacher).distinct()
        if department:
            class_year = class_year.filter(unitplan_myp__subject__department__in=department).distinct()
        return class_year

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    def get_queryset(self):
        levels = Level.objects.all()
        subject = self.request.query_params.get("subject", None)
        if subject:
            levels = levels.filter(subject_groups__subject__in=[subject]).distinct()
        return levels
    
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    def get_queryset(self):
        subjects = Subject.objects.all()
        level = self.request.query_params.get("level", None)
        type_string = self.request.query_params.get("type", None)
        author = self.request.query_params.get("author", None)
        department = self.request.query_params.get("department", None)
        program = self.request.query_params.get("program", None)
        teacher = self.request.query_params.get("teacher", None)
        need_report = self.request.query_params.get("need_report", None)
        plan = self.request.query_params.get("plan", None)
        if department:
            subjects = subjects.filter(department=department)
        if level:
            subjects = subjects.filter(level=level)
        if type_string:
            subjects = subjects.filter(Q(type__icontains=type_string))
        if program:
            subjects = subjects.filter(group_ib__program=program)
        if author:
            subjects = subjects.filter(unitplan_myp__authors__in=[author]).distinct()
        if teacher:
            subjects = subjects.filter(workload__teacher=teacher).distinct()
        if need_report:
            subjects = subjects.filter(need_report=need_report)
        if plan:
            subjects = subjects.filter(subject_year__academic_plan__in=[plan]).distinct()
        return subjects
    
# class SubjectLevelMYPViewSet(viewsets.ModelViewSet):
#     queryset = SubjectLevelMYP.objects.all()
#     serializer_class = SubjectLevelMYPSerializer
#     def get_queryset(self):
#         subject_level = SubjectLevelMYP.objects.all()
#         unit = self.request.query_params.get("unit", None)
#         if unit:
#             subject_level = subject_level.filter(unit=unit)
#         return subject_level

class KeyConceptViewSet(viewsets.ModelViewSet):
    queryset = KeyConcept.objects.all()
    serializer_class = KeyConceptSerializer
    
class RelatedConceptViewSet(viewsets.ModelViewSet):
    queryset = RelatedConcept.objects.all()
    serializer_class = RelatedConceptSerializer
    def get_queryset(self):
        subject = self.request.query_params.get("subject", None)
        subjects = self.request.query_params.getlist("subjects[]", None)
        rconcepts = RelatedConcept.objects.all()
        if subject:
            rconcepts = rconcepts.filter(subject_directions__subject_group__subject__in=[subject]).distinct()
        if subjects:
            rconcepts = rconcepts.filter(subject_directions__subject_group__subject__in=subjects).distinct()
        return rconcepts

class GlobalContextViewSet(viewsets.ModelViewSet):
    queryset = GlobalContext.objects.all()
    serializer_class = GlobalContextSerializer

class ExplorationToDevelopViewSet(viewsets.ModelViewSet):
    queryset = ExplorationToDevelop.objects.all()
    serializer_class = ExplorationToDevelopSerializer
    def get_queryset(self):
        gcontext = self.request.query_params.get("gcontext", None)
        explorations = ExplorationToDevelop.objects.all()
        if gcontext:
            explorations = explorations.filter(gcontext=gcontext)
        return explorations

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
        subject = self.request.query_params.get("subject", None)
        group = self.request.query_params.get("group", None)
        if subject:
            aims = aims.filter(subject_group__subject__in=[subject]).distinct()
        if group:
            aims = aims.filter(subject_group=group)
        return aims

class CriterionViewSet(viewsets.ModelViewSet):
    queryset = Criterion.objects.all()
    serializer_class = CriterionSerializer
    def get_queryset(self):
        criteria = Criterion.objects.all()
        subject = self.request.query_params.get("subject", None)
        group = self.request.query_params.get("group", None)
        if subject:
            criteria = criteria.filter(subject_group__subject__in=[subject]).distinct()
        if group:
            criteria = criteria.filter(subject_group=group)
        return criteria

class CriterionDetailViewSet(viewsets.ModelViewSet):
    queryset = Criterion.objects.all()
    serializer_class = CriterionViewSerializer
    def get_queryset(self):
        criteria = Criterion.objects.all()
        subject = self.request.query_params.get("subject", None)
        group = self.request.query_params.get("group", None)
        if subject:
            criteria = criteria.filter(subject_group__subject__in=[subject]).distinct()
        if group:
            criteria = criteria.filter(subject_group=group)
        return criteria

class StrandViewSet(viewsets.ModelViewSet):
    queryset = Strand.objects.all()
    serializer_class = StrandSerializer
    def get_queryset(self):
        subject = self.request.query_params.get("subject", None)
        criteria = self.request.query_params.getlist("criteria[]", None)
        group = self.request.query_params.get("group", None)
        strands = Strand.objects.all()
        if subject:
            strands = strands.filter(criterion__subject_group__subject__in=[subject])
        if group:
            strands = strands.filter(criterion__subject_group__in=[group])
        if criteria:
            strands = strands.filter(criterion__in=criteria)
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
        strand = self.request.query_params.get("strand", None)
        criterion = self.request.query_params.get("criterion", None)
        subject = self.request.query_params.get("subject", None)
        objectives = Objective.objects.all()
        if strand:
            objectives = objectives.filter(strand=strand)
        if criterion:
            objectives = objectives.filter(strand__criterion__in=[criterion]).distinct()
        if subject:
            objectives = objectives.filter(strand__criterion__subject_group__subject__in=[subject]).distinct()
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

class UnitPlannerMYPIDListCreateSet(viewsets.ModelViewSet):
    queryset = UnitPlannerMYPID.objects.all()
    serializer_class = UnitPlannerMYPIDListCreate
    def get_queryset(self):
        idu = UnitPlannerMYPID.objects.all()
        class_year = self.request.query_params.get("class_year", None)
        if class_year:
            idu = idu.filter(class_year=class_year)
        return idu

class UnitPlannerMYPIDViewEditSet(viewsets.ModelViewSet):
    queryset = UnitPlannerMYPID.objects.all()
    serializer_class = UnitPlannerMYPIDViewEdit
    def get_queryset(self):
        idu = UnitPlannerMYPID.objects.all()
        return idu
    def destroy(self, request, pk=None, *args, **kwargs):
        print('Переданные данные: ', pk)
        ReflectionMYP.objects.filter(idu=pk).delete()
        InquiryQuestionMYP.objects.filter(idu=pk).delete()
        return super().destroy(request, pk=None, *args, **kwargs)

def get_docx_from_html(file, field):
    document = Document()
    parser = HtmlToDocx()
    if field is None:
        field = ''
    parser.add_html_to_document(field, document)
    document.save(file)
    return file

class UnitExport(APIView):
    def get(self, request):
        doc = DocxTemplate(os.path.join(settings.BASE_DIR, 'reports', 'temp_unitplan_myp.docx'))
        # type = request.query_params.get("type", None)
        current_unitplan = UnitPlannerMYP.objects.filter(id=request.query_params.get("unit", None)).first()
        if current_unitplan:
            temp_file = tempfile.NamedTemporaryFile(prefix="tmp_", dir=os.path.join(settings.BASE_DIR, 'tmp'))
            # Подготовка данных полей для экспорта
            text_authors = "\n".join([teacher.user.get_full_name() for teacher in current_unitplan.authors.all()])
            text_subjects = ", ".join([f'{subject.name_rus} ({subject.group_ib.name_eng})' for subject in current_unitplan.subjects.all()])
            text_key_concepts = ", ".join([key.name_eng for key in current_unitplan.key_concepts.all()])
            text_related_concepts = ", ".join([related.name_eng for related in current_unitplan.related_concepts.all()])
            text_explorations = "\n".join([exp.name_eng for exp in current_unitplan.explorations.all()])
            doc_conceptual_understanding = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.conceptual_understanding))
            doc_statement_inquiry = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.statement_inquiry))
            text_inquiry_questions = "\n".join([f'{inq.type_inq} - {inq.question} ({inq.line})' for inq in current_unitplan.inquestions.all()])
            text_aims = "\n".join([f'- {aim.name_eng}' for aim in current_unitplan.aims.all()])
            text_strands = "\n\n".join([f'{cr.letter}. {cr.name_eng}\n'+"\n".join([f'{st.get_letter_display()}. {st.name_eng}' for st in current_unitplan.strands.filter(criterion=cr)]) for cr in current_unitplan.criteria.all()])
            doc_summative_assessment_task = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.summative_assessment_task))
            doc_summative_assessment_soi = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.summative_assessment_soi))
            text_atlmapping = "\n".join([f'{atl.atl.name_eng} ({atl.atl.cluster.name_eng})\n{atl.strand.get_letter_display()}. {atl.strand.name_eng}: \n{atl.action}' for atl in current_unitplan.atlmapping.all()])
            doc_content = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.content))
            doc_skills = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.skills))
            doc_prior_experiences = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.prior_experiences))
            doc_learning_experiences = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.learning_experiences))
            doc_teaching_strategies = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.teaching_strategies))
            doc_formative_assessment = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.formative_assessment))
            doc_differentiation = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.differentiation))
            doc_peer_self_assessment = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.peer_self_assessment))
            doc_standardization_moderation = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.standardization_moderation))
            doc_student_expectations = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.student_expectations))
            doc_feedback = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.feedback))
            text_learner_profile = "\n".join([f'- {lp.name_eng}' for lp in current_unitplan.learner_profile.all()])
            doc_description_lp = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.description_lp))
            doc_international_mindedness = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.international_mindedness))
            doc_academic_integrity = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.academic_integrity))
            doc_language_development = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.language_development))
            doc_infocom_technology = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.infocom_technology))
            doc_service_as_action = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.service_as_action))
            doc_resources = doc.new_subdoc(get_docx_from_html(temp_file, current_unitplan.resources))
            text_prior_reflection = "\n".join([f'{ref.post} ({ref.author})' for ref in current_unitplan.reflections.filter(type_post="Prior")])
            text_during_reflection = "\n".join([f'{ref.post} ({ref.author})' for ref in current_unitplan.reflections.filter(type_post="During")])
            text_after_reflection = "\n".join([f'{ref.post} ({ref.author})' for ref in current_unitplan.reflections.filter(type_post="After")])
            # print(doc_statement_inquiry)
            # new_parser = HtmlToDocx()
            # docx = new_parser.parse_html_string(current_unitplan.statement_inquiry)
            context = {'title': current_unitplan.title, 
                       'authors': text_authors,
                       'subjects': text_subjects,
                       'class_year': current_unitplan.class_year.year_ib,
                       'hrs': current_unitplan.hours,
                       'key_concepts': text_key_concepts,
                       'related_concepts': text_related_concepts,
                       'global_context': current_unitplan.global_context.name_eng,
                       'explorations': text_explorations,
                       'conceptual_understanding': doc_conceptual_understanding,
                       'statement_inquiry': doc_statement_inquiry,
                       'inquiry_questions': text_inquiry_questions,
                       'aims': text_aims,
                       'strands': text_strands,
                       'summative_assessment_task': doc_summative_assessment_task,
                       'summative_assessment_soi': doc_summative_assessment_soi,
                       'atlmapping': text_atlmapping,
                       'content': doc_content,
                       'skills': doc_skills,
                       'prior_experiences': doc_prior_experiences,
                       'learning_experiences': doc_learning_experiences,
                       'teaching_strategies': doc_teaching_strategies,
                       'formative_assessment': doc_formative_assessment,
                       'differentiation': doc_differentiation,
                       'peer_self_assessment': doc_peer_self_assessment,
                       'standardization_moderation': doc_standardization_moderation,
                       'student_expectations': doc_student_expectations,
                       'feedback': doc_feedback,
                       'learner_profile': text_learner_profile,
                       'description_lp': doc_description_lp,
                       'international_mindedness': doc_international_mindedness,
                       'academic_integrity': doc_academic_integrity,
                       'language_development': doc_language_development,
                       'infocom_technology': doc_infocom_technology,
                       'service_as_action': doc_service_as_action,
                       'resources': doc_resources,
                       'prior_reflection': text_prior_reflection,
                       'during_reflection': text_during_reflection,
                       'after_reflection': text_after_reflection,
                       }
            doc.render(context)
            doc.save(os.path.join(settings.BASE_DIR, 'tmp', 'generated_report.docx'))
            # if type == 'pdf':
            #     pypandoc.convert_file(os.path.join(settings.BASE_DIR, 'tmp', 'generated_report.docx'),
            #                           'pdf', outputfile=os.path.join(settings.BASE_DIR, 'tmp', 'generated_report.pdf'))
            #     file_path = os.path.join(settings.BASE_DIR, 'tmp', 'generated_report.pdf')
            #     with open(file_path, 'rb') as file:
            #         print('Экспорт в PDF')
            #         response_file = HttpResponse(file.read())
            #         response_file["Content-Disposition"] = "attachment; filename=generated_report.pdf"
            #         response_file["Content-Type"] = "application/pdf"
            #         return response_file
            file_path = os.path.join(settings.BASE_DIR, 'tmp', 'generated_report.docx')
            with open(file_path, 'rb') as file:
                print('Экспорт в WORD')
                response_file = HttpResponse(file.read())
                response_file["Content-Disposition"] = "attachment; filename=generated_report.docx"
                response_file["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                return response_file
        return Response({
            'Message': 'ERROR'})
    