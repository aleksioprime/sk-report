from curriculum.models import UnitPlannerMYP, ClassYear, Subject, Criterion, LearnerProfileIB, SkillATL, Objective, Aim, GlobalContext, \
    ExplorationToDevelop, KeyConcept, RelatedConcept, InquiryQuestionMYP, ATLMappingMYP, ReflectionMYP, Strand, Level, UnitPlannerMYPID, SubjectLevelMYP
from member.models import ProfileTeacher, Department
from curriculum.serializers import UnitMYPSerializerViewEdit, UnitMYPSerializerListCreate, ProfileTeacherSerializer, ClassYearSerializer, \
    SubjectSerializer, CriterionSerializer, DepartmentSerializer, LearnerProfileIBSerializer, SkillATLSerializer, ObjectiveSerializer, \
    AimSerializer, GlobalContextSerializer, ExplorationToDevelopSerializer, KeyConceptSerializer, RelatedConceptSerializer, InQuestionMYPSerializer, \
    ATLMappingMYPSerializer, ReflectionMYPSerializer, StrandSerializer, LevelSerializer, UnitPlannerMYPIDSerializer, SubjectLevelMYPSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from docxtpl import DocxTemplate, RichText
from rest_framework.views import APIView
from django.conf import settings
from django.http import HttpResponse

import os
# from io import BytesIO
# import pypandoc
from htmldocx import HtmlToDocx
from docx import Document
import tempfile

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
    