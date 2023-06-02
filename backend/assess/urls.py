from django.urls import path
from assess.views import StudyYearViewSet, ClassGroupViewSet, StudyPeriodViewSet, SummativeWorkViewSet, \
    WorkAssessmentViewSet, PeriodAssessmentViewSet, StudentViewSet, WorkGroupDateItemViewSet, \
    StudentWorkViewSet, AssessmentJournalAPIView, ReportPeriodViewSet, StudentReportTeacherViewSet, \
    ReportTeacherViewSet, EventParticipationViewSet, EventTypeViewSet, StudentReportMentorViewSet, \
    ReportMentorViewSet, ReportMentorJournalAPIView, AssessmentDnevnikAPIView, ReportTeacherJournalAPIView, \
    ClassGroupStudentsViewSet, WorkLoadViewSet, WorkAssessmentGiveMarksAPIView, TextTranslateAPIView, \
    GenerateReportAPIView, ExportReportMentorDOCXAPIView, ReportPsychologistJournalAPIView, ReportPsychologistViewSet, \
    StudentReportPsychologistViewSet, FinalMarksDnevnikAPIView, WorkLoadSubjectViewSet, ClassGroupForReportTeacherViewSet, \
    ClassGroupForReportPsychoViewSet, ClassYearForReportViewSet, ClassGroupForReportMentorViewSet

urlpatterns = [
    path('student', StudentViewSet.as_view({'get': 'list'})),
    path('assessment/year', StudyYearViewSet.as_view({'get': 'list'})),
    path('assessment/group', ClassGroupViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/group/students', ClassGroupStudentsViewSet.as_view({'get': 'list'})),
    path('assessment/group/<int:pk>', ClassGroupViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('assessment/period', StudyPeriodViewSet.as_view({'get': 'list'})),
    path('assessment/report/period', ReportPeriodViewSet.as_view({'get': 'list'})),
    path('assessment/student/report/teacher', StudentReportTeacherViewSet.as_view({'get': 'list'})),
    path('assessment/student/report/psychologist', StudentReportPsychologistViewSet.as_view({'get': 'list'})),
    path('assessment/student/report/mentor', StudentReportMentorViewSet.as_view({'get': 'list'})),
    path('assessment/student', StudentWorkViewSet.as_view({'get': 'list'})),
    path('assessment/sumwork', SummativeWorkViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/sumwork/<int:pk>', SummativeWorkViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('assessment/workgroup/<int:pk>', WorkGroupDateItemViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path('assessment/workassess', WorkAssessmentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/workassess/<int:pk>', WorkAssessmentViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('assessment/workassess/givemarks', WorkAssessmentGiveMarksAPIView.as_view()),
    path('assessment/periodassess', PeriodAssessmentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/periodassess/<int:pk>', PeriodAssessmentViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('assessment/report/teacher', ReportTeacherViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/report/teacher/<int:pk>', ReportTeacherViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('assessment/report/psychologist', ReportPsychologistViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/report/psychologist/<int:pk>', ReportPsychologistViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('assessment/report/mentor', ReportMentorViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('assessment/report/mentor/<int:pk>', ReportMentorViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('assessment/journal', AssessmentJournalAPIView.as_view()),
    path('assessment/journal/dnevnik', AssessmentDnevnikAPIView.as_view()),
    path('assessment/report/mentor/journal', ReportMentorJournalAPIView.as_view()),
    path('assessment/report/teacher/journal', ReportTeacherJournalAPIView.as_view()),
    path('assessment/report/teacher/dnevnik', FinalMarksDnevnikAPIView.as_view()),
    path('assessment/report/psychologist/journal', ReportPsychologistJournalAPIView.as_view()),
    path('assessment/events', EventParticipationViewSet.as_view({'get': 'list'})),
    path('assessment/events/types', EventTypeViewSet.as_view({'get': 'list'})),
    path('translate', TextTranslateAPIView.as_view()),
    path('generate/report', GenerateReportAPIView.as_view()),
    path('assessment/export/reportmentor/docx', ExportReportMentorDOCXAPIView.as_view()),
    path('workload/subjects', WorkLoadSubjectViewSet.as_view({'get': 'list'})),
    path('workload/subjects/<int:pk>', WorkLoadSubjectViewSet.as_view({'get': 'retrieve'})),
    path('workload', WorkLoadViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('workload/<int:pk>', WorkLoadViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('report/teacher/groups', ClassGroupForReportTeacherViewSet.as_view({'get': 'list'})),
    path('report/psychologist/groups', ClassGroupForReportPsychoViewSet.as_view({'get': 'list'})),
    path('report/mentor/groups', ClassGroupForReportMentorViewSet.as_view({'get': 'list'})),
    path('report/years', ClassYearForReportViewSet.as_view({'get': 'list'})),

]