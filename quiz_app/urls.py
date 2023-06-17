from django.urls import path, include
# from rest_framework import routers
from . import views


# router = routers.DefaultRouter()
# router.register('quizes', views.QuizView)
# router.register('options',views.OptionView)

app_name = 'quiz_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('student/exam_list/', views.exam_list_view, name='exam_list'),
    # path('student/exam_view', views.exam_view, name='exam_view'),
    path('student/quiz_view/<int:id>/<int:pk>/', views.quiz_view, name='quiz_view'),
    path('student/re_exam/<int:pk>/',views.re_exam, name='re_exam'),
    path('result/<int:pk>/', views.result_view, name='result_view'),
    path('exam_status/<int:pk>/', views.exam_status_view, name='exam_status_view'),
    path('get_paid_account/',views.get_paid_account, name='get_paid_account'),
    # path('subject/', views.subject_view, name='subject_view'),
    # path('topic/<int:pk>/' , views.topic_view, name='topic_view'),
    path('user_quiz_info_list/',views.user_quiz_info_list, name='user_quiz_info'),
    path('teacher/exam_info_input/', views.exam_info_input, name='exam_info_input'),
    path('teacher/exam_info_details/<int:pk>', views.exam_info_details_view, name='exam_info_details'),
    path('teacher/exam_info_update/<int:pk>/',views.exam_info_update, name='exam_info_update'),
    path('teacher/exam_info_delete/<int:pk>/',views.exam_info_delete, name='exam_info_delete'),
    path('teacher/exam_info_publish/<int:pk>/',views.exam_info_publish, name='exam_info_publish'),
    path('teacher/question_input_form/<int:pk>/', views.question_input_form, name='data_input_form'),
    path('teacher/question_check/<int:pk>/', views.question_check_view, name='question_check'),
    # path('teacher/question_edit_form/<int:pk>/', views.question_edit, name='question_edit'),
    path('teacher/question_delete/<int:pk>/', views.question_delete, name='question_delete'),
    path('teacher/stu_of_inst/', views.std_info_institu, name='students_of_institution'),
    path('teacher/stu_activ_list/',views.std_approved_list, name='std_approved_list'),
    path('teacher/stu_not_activ_list/',views.std_not_approved_list, name='std_not_approved_list'),
    path('teacher/stud_activ/<int:pk>/', views.stu_activation, name='stud_activat'),
    # path('get_options_by_quiz/<int:pk>/', views.OptionsByQuiz.as_view(), name = 'get_options_by_quiz'),
    path('student/regis/', views.student_regis, name = 'student_regis'),
    path('teacher/regis', views.teacher_regis, name = 'teacher_regis'),
    # path('student/profile_update/', views.student_profile_update(), name='student_profile_update'),
    # path('teacher/profile_update/', views.teacher_profile_update(), name='teacher_profile_update'),
    path('teacher/dashboard/', views.exam_info_list, name='teacher_dashboard'),
    path('super/dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('super/inst_list_filter/', views.Institution_info_list, name='inst_list_filter'),
    path('super/make_payment/<int:pk>/', views.make_payment, name='make_payment'),
    # path('', include(router.urls)),
]