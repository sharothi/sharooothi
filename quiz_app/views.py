from django.shortcuts import render, redirect, get_object_or_404
from quiz_app.models import Quiz, Option, UserQuizInfo, Student, Payment
from django.shortcuts import get_object_or_404
from quiz_app.forms import QuizForm, CreateUserForm, UserLoginForm, CreateStudentForm, CreateTeacherForm, ExaminationInfoForm, PaymentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from .filters import UserQuizInfoFilter,TeacherInfoFilter, StudentInfoFilter


from django.http import HttpResponse, JsonResponse
# from rest_framework.parsers import JSONParser
from quiz_app.models import Quiz, Option, ExaminationInfo , Teacher, Student,Subject ,InstitutionInfo
# from quiz_app.serializers import QuizSerializer, OptionSerializer
# from rest_framework import viewsets, generics
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import datetime
from django.utils import timezone

import calendar
import time
import json

# def job():
#     print("I'm workent....")





# Create your views here.


def home(request):
    # d = datetime.timedelta( seconds = 30)
    # print(d)
    # payment_create_function()
    # institution_deactiv()

    # import pdb; pdb.set_trace()
    message = ''
    if request.headers.get('Referer'):
        if (request.headers['Referer'].find('student/regis/') != -1)or (request.headers['Referer'].find('teacher/regis/')!= -1) or (request.headers['Referer'].find('register/')!= -1) :
            message = 'Registration successful'
    
    homepage_message=''
    top_header=''
    if InstitutionInfo.objects.last():
        homepage_message = InstitutionInfo.objects.last().homepage_message
        top_header = InstitutionInfo.objects.last().top_header
    return render(request, 'home.html' ,{'message':message, 'homepage_message':homepage_message, 'top_header':top_header })


###---------------start registration, login, logout, change password ,update profile ---------###


##----- teacher registration-----##

def teacher_regis(request):
    user_form = CreateUserForm()
    teac_form = CreateTeacherForm()
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        teac_form = CreateTeacherForm(request.POST)
        if user_form.is_valid() and teac_form.is_valid() :
            user = user_form.save(commit=False)
            user.is_staff = True
            teacher = teac_form.save(commit=False)
            teacher.user_info = user
            user.save()
            teacher.save()

            return redirect('quiz_app:home')

    context = {'user_form':user_form, 'teac_form': teac_form}
    return render(request, 'teach_regis.html', context)




##----- student registration-----##


def student_regis(request):
    user_form = CreateUserForm()
    stu_form = CreateStudentForm()
    if request.method == 'POST':

        user_form = CreateUserForm(request.POST)
        stu_form = CreateStudentForm(request.POST)
        if user_form.is_valid() and stu_form.is_valid() :
            user = user_form.save()
            student = stu_form.save(commit=False)
            student.user_info = user
            student.save()

            return redirect('quiz_app:home')

    context = {'user_form':user_form, 'stu_form': stu_form}
    return render(request, 'student/stu_regis.html', context)






def login_page(request):


    form = UserLoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password') 
            user = authenticate(username=username, password=password)
            login(request, user)
            try:
                if request.user.teacher.is_teacher:
                    return redirect('quiz_app:teacher_dashboard')

            except:
                try:
                    if request.user.student.is_student:
                        return redirect('quiz_app:exam_list')
                except:
                    try:
                        if request.user:
                            return redirect('quiz_app:super_admin_dashboard')
                    except:
                        print("Something went wrong")


    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('quiz_app:home')



###---------------end registration, login, logout, change password ,update profile ---------###






### -----------start only for teacher ----------- ###


@login_required
def exam_info_list(request ):
    exam_info_ls = ExaminationInfo.objects.filter(teacher=request.user.teacher)
    return render(request,'dashboard.html',{'exam_info_ls':exam_info_ls})



            ### ---- for exam info ----##

@login_required
def exam_info_input(request):
    exam_info_form = ExaminationInfoForm()
    if request.method == 'POST':
        exam_info_form = ExaminationInfoForm(request.POST)
        if exam_info_form.is_valid():
            exam_info = exam_info_form.save(commit=False)
            exam_info.teacher = request.user.teacher
            exam_info.save()
            return redirect('quiz_app:teacher_dashboard')

        
    context = {'exam_info_form':exam_info_form}
    return render(request, 'teacher/exam_info_form.html', context)


@login_required
def exam_info_details_view(request, pk):
    exam_info = get_object_or_404(ExaminationInfo, pk=pk)
    return render(request, 'teacher/exam_info_details.html', {'exam_info':exam_info})


@login_required
def exam_info_update(request, pk):
    exam_info = get_object_or_404(ExaminationInfo, pk=pk)
    exam_info_form = ExaminationInfoForm(instance=exam_info)
    if request.method == "POST":
        exam_info_form = ExaminationInfoForm(request.POST, instance=exam_info)
        if exam_info_form.is_valid():
            exam_info = exam_info_form.save(commit=False)
            exam_info.teacher = request.user.teacher
            exam_info.save()
            return redirect('quiz_app:exam_info_details', pk=pk)

    context = {'exam_info_form':exam_info_form}
    return render(request, 'teacher/exam_info_form.html', context)



@login_required
def exam_info_publish(request, pk):
    exam_info = get_object_or_404(ExaminationInfo, pk=pk)
    exam_info.publish()
    return redirect('quiz_app:exam_info_details', pk=pk)
    

@login_required
def exam_info_status_change(request, pk):
    exam_info = get_object_or_404(ExaminationInfo, pk=pk)
    exam_info.change_status()
    return redirect('quiz_app:teacher_dashboard')

@login_required
def exam_info_delete(request, pk):
    exam_info= get_object_or_404(ExaminationInfo, pk=pk)
    if request.method == "POST":
        exam_info.delete()
        return redirect('quiz_app:teacher_dashboard')
    context = {'pk':pk}
    return render(request, 'teacher/exam_info_delete_view.html', context)




    ### -------question_input, edit ,delete --------###
    

@login_required
def question_input_form(request,pk=0):
    exam_info = ExaminationInfo.objects.get(teacher=request.user.teacher, pk=pk)
    number_of_questions = Quiz.objects.filter(exam_info=exam_info)
    quiz_form = QuizForm()

    if request.method == 'POST' :
        quiz_form = QuizForm(request.POST)
        
        if quiz_form.is_valid():

            quiz_title = quiz_form.cleaned_data['title']
            quiz_hints = quiz_form.cleaned_data['hints']
            quiz = Quiz.objects.create( exam_info=exam_info , title = quiz_title, hints = quiz_hints)
            try:
                options_titels = dict(request.POST)['option_title']
                i = 0 
                for opt_title in options_titels:
                    is_corre = 'is_correct_' + str(i)
                    is_corr = True if dict(request.POST).get(is_corre)[0] == 'True' else False 
                    Option.objects.create(quiz=quiz, title=opt_title, is_correct=is_corr)
                    i= i+1
            except:
                quiz.delete()
                return render(request, 'teacher/forms.html' , { 'quiz_form':quiz_form, 'message': 'Please input your data correctly' })

            else:
                quiz_form = QuizForm()
                return render(request, 'teacher/forms.html' , { 'quiz_form':quiz_form, 'message': 'Submited' ,'number_of_questions':number_of_questions })

                

    return render(request, 'teacher/forms.html' , { 'quiz_form':quiz_form , 'number_of_questions':number_of_questions })




@login_required
def question_check_view(request, pk):
    exam_info = ExaminationInfo.objects.get(teacher=request.user.teacher, pk=pk)
    questions = Quiz.objects.filter(exam_info=exam_info)
    return render(request, 'teacher/check_questions.html', {'questions':questions})





@login_required
def question_edit(request, pk):
    quiz_data = get_object_or_404(Quiz, pk=pk)
    quiz_form = QuizForm(instance=quiz_data)
    options = Option.objects.filter(quiz=quiz_data)

    if request.method == "POST":
        quiz_form = QuizForm(request.POST, instance=quiz_data)

        if quiz_form.is_valid():
            quiz = quiz_form.save()
            try:
                options_titels = dict(request.POST)['option_title']

                i=0
                for option in options_titels:
                    opt = get_object_or_404(Option, title=option)

                    is_corre = 'is_correct_' + str(i)
                    is_corr = True if dict(request.POST).get(is_corre)[0] == 'True' else False 
                    opt.update(title=opt_title, is_correct=is_corr)

                    i= i+1
            except:
                return render(request, 'questions_edit_form.html' , { 'quiz_form':quiz_form, 'message': 'Please input your data correctly' })

            else:
                quiz_form = QuizForm()
                return render(request, 'questions_edit_form.html' , { 'quiz_form':quiz_form, 'message': 'Submited' ,'number_of_questions':number_of_questions })
        
    context = {'quiz_form':quiz_form, 'options':options}
    return render(request, 'questions_edit_form.html', context)




@login_required
def question_delete(request, pk):
    quiz_data = get_object_or_404(Quiz, pk=pk)
    exam_info_pk = quiz_data.exam_info.pk
    if request.method == "POST":
        quiz_data.delete()
        return redirect('quiz_app:question_check', pk=exam_info_pk)
    context = {'pk':pk}
    return render(request, 'teacher/question_delete_view.html', context)
    

@login_required
def std_info_institu(request):
    students = Student.objects.all()
    return render(request, 'teacher/stdinfo_institu.html', {'students':students, 'query_type':'all'})


@login_required
def std_approved_list(request):
    approved_students = Student.objects.filter(approved = True)
    return render(request, 'teacher/stdinfo_institu.html', {'students':approved_students, 'query_type':'approved'})


@login_required
def std_not_approved_list(request):
    not_approved_students = Student.objects.filter(approved = False)
    return render(request, 'teacher/stdinfo_institu.html', {'students':not_approved_students, 'query_type':'not_approved'})


@login_required
def stu_activation(request, pk):
    student=Student.objects.get(pk=pk)
    student.activate_student()
    student.approved_by = request.user.teacher
    return redirect('quiz_app:students_of_institution')
###----------------end only for teacher----------###





###----------- start only for students -----------###





@login_required
def exam_list_view(request):
    payment_form = PaymentForm()
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.user_info = request.user.student
            payment.save()
            return redirect('quiz_app:exam_list')
        
    
    exam_list = ExaminationInfo.objects.filter(published=True, class_name =request.user.student.class_name)

    activation_message = 'There are no activation message from admin'
    if InstitutionInfo.objects.last():
        activation_message = InstitutionInfo.objects.last().activation_message
        # after_payment_message = InstitutionInfo.objects.last().after_payment_message

    if exam_list:
        if request.user.student.approved:
            user_exam_done = None
            exams=[]
            for exam in exam_list:
                try:
                    user_exam_done = UserQuizInfo.objects.get(examination_info=exam, exam_done=True, user_info=request.user.student)
                except:
                    exams.insert(len(exams),exam) 
                else:
                    exam.done = True
                    exams.insert(len(exams),exam) 
                    # return render(request, 'student/exam_view1.html', {'std_exam_info':exams, 'user_exam_done':user_exam_done})
            

            return render(request, 'student/exam_view1.html', {'std_exam_info':exams, 'user_exam_done':user_exam_done})
        else:
            exam_list = ExaminationInfo.objects.filter(published=True, pay_status='free', class_name=request.user.student.class_name)
            user_exam_done = None
            exams=[]
            print(exam_list)
            for exam in exam_list:
                try:
                    user_exam_done = UserQuizInfo.objects.get(examination_info=exam, exam_done=True, user_info=request.user.student)
                except:
                    exams.insert(len(exams),exam) 
                else:
                    exam.done = True
                    exams.insert(len(exams),exam) 
                    # return render(request, 'student/exam_view1.html', {'std_exam_info':exams, 'user_exam_done':user_exam_done})
            

            return render(request, 'student/exam_view1.html', {'std_exam_info':exams, 'user_exam_done':user_exam_done})
            # import pdb;pdb.set_trace()

            # if not request.user.student.stu_pay_info.last():
            #     return render(request, 'student/exam_view.html', { 'activation_message':activation_message, 'form':payment_form})
            # else:
            #     return render(request, 'student/exam_view1.html', {'after_payment_message':after_payment_message})

    return render(request, 'student/exam_view1.html', {'message':'There are no Qusetions available'})



@login_required
def get_paid_account(request):

    payment_form = PaymentForm()
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.user_info = request.user.student
            payment.save()
            return redirect('quiz_app:exam_list')
        
    activation_message = 'There are no activation message from admin'
    if InstitutionInfo.objects.last():
        activation_message = InstitutionInfo.objects.last().activation_message
        after_payment_message = InstitutionInfo.objects.last().after_payment_message

    if not request.user.student.stu_pay_info.last():
        return render(request, 'student/exam_view.html', { 'activation_message':activation_message, 'form':payment_form})
    else:
        print(after_payment_message)
        return render(request, 'student/exam_view1.html', {'after_payment_message':after_payment_message})




@login_required
def quiz_view(request, id , pk=0):
    if not request.user.student : 
        std_exam_info = ExaminationInfo.objects.get(pk=id)
        all_questions = Quiz.objects.filter(exam_info = std_exam_info)
        timeduration = int(std_exam_info.total_time*60)
        time = datetime.timedelta(seconds=timeduration)
    else:
        std_exam_info = ExaminationInfo.objects.get(pk=id)
        all_questions = Quiz.objects.filter(exam_info = std_exam_info)
        timeduration = int(std_exam_info.total_time*60)
        time = datetime.timedelta(seconds=timeduration)
    # print(time)
    if UserQuizInfo.objects.filter(examination_info=std_exam_info,user_info=request.user.student).exists():
        info = UserQuizInfo.objects.get(examination_info=std_exam_info,user_info=request.user.student)
        last_user_user_quiz_start_time = info.start_time
        # import pdb; pdb.set_trace()
        if (time < (timezone.now()-last_user_user_quiz_start_time)):
            if not info.exam_done:
                info.exam_done_ok()
                info.exam_end_time()
                # print('time over')
        # if UserQuizInfo.objects.get(examination_info=std_exam_info,user_info=request.user.student).exam_done:
        if info.exam_done:

            return render(request, 'student/index.html',{'quiz': 0,'result_info':info,'data':json.loads(info.data)})

    def get_next_data(quiz_list_id):
        # quiz = Quiz.objects.filter(pk=pk, exam_info = std_exam_info).count()
        # if (quiz == 1):
        #     quiz = Quiz.objects.get(pk=pk, exam_info = std_exam_info)
        #     # quiz = all_questions[]
        #     options = Option.objects.filter(quiz=quiz)
        #     next_pk = pk+1
            
        #     return {'quiz':quiz, 'options':options, 'pk':pk , 'next_pk':next_pk }
    
        # pk = pk + 1
        # return get_next_data(pk)
        quiz = all_questions[quiz_list_id]
        options = Option.objects.filter(quiz=quiz)
        next_pk = quiz_list_id + 1
        pk = quiz_list_id

        return {'quiz':quiz, 'options':options, 'pk':pk , 'next_pk':next_pk }

    if request.method == 'POST' :
        data = get_next_data(pk)
        quiz = data['quiz']
        options = data['options']
        pk = data['pk']
        next_pk = data['next_pk']
        corr_options = Option.objects.filter(quiz=quiz, is_correct = True)
        client_given = list(dict(request.POST).keys())
        corr_opt_list = [x.title for x in  corr_options]
        que_data = {'title':str(quiz),'client_given':client_given[1:],'corr_opt_list':corr_opt_list ,'status':True}

        if len(client_given)-1 >= 1:
            if (len(corr_options)) == (len(client_given)-1):
                for option in corr_options:
                    if str(option) not in client_given:
                        obj,created = UserQuizInfo.objects.get_or_create(user_info=request.user.student, examination_info=std_exam_info )
                        obj.last_answered_quiz_pk = quiz.pk
                        que_data['status'] = False
                        que_data = json.loads(obj.data) + [que_data]
                        obj.data = json.dumps(que_data)
                        obj.save()

                        return redirect('quiz_app:quiz_view',id=id, pk=next_pk)

                else:

                    obj,created = UserQuizInfo.objects.get_or_create(user_info=request.user.student , examination_info=std_exam_info )
                    obj.last_answered_quiz_pk = quiz.pk
                    que_data = json.loads(obj.data) + [que_data]
                    obj.data = json.dumps(que_data)
                    obj.num_of_correct_ans = obj.num_of_correct_ans + 1
                    obj.save()
                    return redirect('quiz_app:quiz_view', id=id, pk=next_pk)

            else:
                obj,created = UserQuizInfo.objects.get_or_create(user_info=request.user.student , examination_info=std_exam_info )
                obj.last_answered_quiz_pk = quiz.pk
                que_data['status'] = False
                que_data = json.loads(obj.data) + [que_data]
                obj.data = json.dumps(que_data)
                obj.save()
                return redirect('quiz_app:quiz_view', id=id, pk=next_pk)

        else:
            # import pdb; pdb.set_trace()
            return render(request, 'student/index.html', {'last_user_user_quiz_start_time':last_user_user_quiz_start_time,'quiz':quiz, 'options': options, 'next_pk':next_pk, 'error':'You have not provided any answer'})

            

    if pk == all_questions.count():
        # print(std_exam_info, request.user.student)
        # import pdb; pdb.set_trace()
        result_info = UserQuizInfo.objects.get(examination_info=std_exam_info,user_info=request.user.student)
        if (pk == all_questions.count()):
            result_info.exam_done_ok()
            result_info.exam_end_time()
        return render(request, 'student/index.html',{'quiz': 0,'result_info':result_info})
 
    else:

        outputs = get_next_data(pk)
        quiz = outputs['quiz']
        options = outputs['options']
        pk = outputs['pk']
        next_pk = outputs['next_pk']
        last_user_user_quiz_start_time = UserQuizInfo.objects.get_or_create(user_info=request.user.student, examination_info=std_exam_info )[0].start_time
        
        # import pdb; pdb.set_trace()
        return render(request, 'student/index.html', {'last_user_user_quiz_start_time':last_user_user_quiz_start_time,'quiz':quiz, 'options': options, 'next_pk':next_pk })

@login_required
def re_exam(request, pk ):

    try:
        examination_info=ExaminationInfo.objects.get(pk=pk)
        user_info=request.user.student
        user_quiz = UserQuizInfo.objects.get(examination_info=examination_info, exam_done=True, user_info=user_info)
        # user_quiz.last_answered_quiz_pk = 0
        # user_quiz.num_of_correct_ans = 0
        # user_quiz.data = json.dumps([])
        # user_quiz.exam_done = False
        # user_quiz.start_time = 
        # user_quiz.end_time = 
        # user_quiz.time_delta =
    except Exception as e:
        print(e)
        return redirect('quiz_app:quiz_view', id=pk, pk=0)
    else:
        user_quiz.delete()
        return redirect('quiz_app:quiz_view', id=pk, pk=0)



def user_quiz_info_list(request):
    print(request.user.teacher.institution_name)
    
    f = UserQuizInfoFilter(request.GET, queryset=UserQuizInfo.objects.filter(user_info__institution_name = request.user.teacher.institution_name))
    return render(request, 'user_quiz_info.html',{'filter':f})



@login_required
def result_view(request, pk):
    students_result = UserQuizInfo.objects.filter(examination_info=pk, exam_done=True).order_by('-num_of_correct_ans')[:30]
    if students_result:
        
        top_result = UserQuizInfo.objects.filter(exam_done=True, num_of_correct_ans=students_result[0].num_of_correct_ans).order_by('time_delta')[0]
        # import pdb;pdb.set_trace()
        # print(top_result)
        try:
            if request.user.teacher:
                return render(request, 'teacher/result_sheet.html', {'results':students_result ,'top_result':top_result})
        except:
            # UserQuizInfo.objects.get(pk=pk)
            return render(request,'student/result_sheet_student.html',{'results':students_result ,'top_result':top_result})

    message = 'কেউ এখনো পরীক্ষায় অংশগ্রহণ করেনি। '
    return render(request, 'student/result_sheet_student.html',{'message':message}) 


@login_required
def exam_status_view(request, pk):
    exam_status = json.loads(UserQuizInfo.objects.get(pk=pk).data)
    # print(exam_status)
    return render(request, 'student/exam_status_view.html', {'exam_status':exam_status} )






### ------------ only for agent ------------####



###--------------- for super admin ---------------###


def super_admin_dashboard(request):
    agents = Agent.objects.all()
    print(agents)
    # import pdb; pdb.set_trace()
    return render(request, 'dashboard.html', {'agents': agents})


def Institution_info_list(request):
    
    f = InstitutionInfoFilter(request.GET, queryset=Institution.objects.all())
    return render(request, 'institution_info_filter.html',{'filter':f})



def make_payment(request, pk):
    payment=get_object_or_404(Payment, pk=pk)
    payment.make_payment()
    return redirect('quiz_app:inst_list_filter')

###### how to ####
# get last instance of model object -----> ModelName.objects.last() ,ModelName.objects.filter(name='simple').first()










# >>>----------->>> code for JSON data <<<----------<<<

# class QuizView(viewsets.ModelViewSet):
#     queryset = Quiz.objects.all()
#     serializer_class = QuizSerializer

# class OptionView(viewsets.ModelViewSet):
#     queryset = Option.objects.all()
#     serializer_class = OptionSerializer


# class OptionsByQuiz(generics.ListCreateAPIView):
#     def get_queryset(self, *args, **kwargs):
#         get_quiz = Quiz.objects.get(pk=self.kwargs['pk'])
#         queryset = Option.objects.filter( quiz = get_quiz )
#         return queryset

#     serializer_class = OptionSerializer


