from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from quiz_app.models import Quiz, Student, Teacher, ExaminationInfo ,Payment
from django.contrib.auth import authenticate



class QuizForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea)
    hints = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Quiz
        fields = ['exam_info','title', 'hints']
        labels = {
            'title': ('Quiz'),
        }
        widgets = {
            'exam_info' : forms.HiddenInput(attrs={'class': 'form-control'})
        }



class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control', 'placeholder': ' You can Use email as username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control', 'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={
    'class': 'form-control', 'placeholder': 'Type your email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    'class': 'form-control', 'placeholder': 'Repeat Password'}))

    class Meta:
        model = User
        fields = ['username','first_name', 'email', 'password1', 'password2']





class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    password = forms.CharField(
        label='Password',
        widget=forms.TextInput(
            attrs={'type': 'password',
            'class': 'form-control'
            }
        )
    )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            print(user)
            if not user:
                print('not correct')
                raise forms.ValidationError('Incorract credentials')

        return super(UserLoginForm, self).clean(*args, **kwargs)




class CreateStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['user_info', 'class_name']
        widgets = {
            'user_info' : forms.HiddenInput(attrs={'class': 'form-control'}),
            'class_name' : forms.Select(attrs={'class': 'form-control'}),
        }


class CreateTeacherForm(forms.ModelForm):
    
    class Meta:
        model = Teacher
        fields = ['user_info', 'phone_number']
        widgets = {
            'user_info' : forms.HiddenInput(attrs={'class': 'form-control'}),
            'phone_number' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Use +88'}),

        }



class ExaminationInfoForm(forms.ModelForm):

    class Meta:
        model = ExaminationInfo
        fields = ['exam_name', 'class_name', 'subject_name', 'teacher', 'par_ques_marks', 'total_time','pay_status']
        widgets = {
            'exam_name' :forms.TextInput(attrs={'class': 'form-control'}),
            'class_name' :forms.Select(attrs={'class': 'form-control'}),
            'subject_name' : forms.Select(attrs={'class': 'form-control'}),
            'teacher' : forms.HiddenInput(attrs={'class': 'form-control'}),
            'par_ques_marks' : forms.NumberInput(attrs={'class': 'form-control'}),
            'total_time' : forms.NumberInput(attrs={'class': 'form-control'}),
            'pay_status' : forms.Select(attrs={'class': 'form-control'}),
        }


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['user_info','phone_number']
        widgets = {
            'user_info' : forms.HiddenInput(attrs={'class': 'form-control'}),
            'phone_number' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bkash Number'}),
        }
