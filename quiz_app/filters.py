from .models import Teacher, Student, UserQuizInfo , Payment
from django.contrib.auth.models import User 
import django_filters

class UserQuizInfoFilter(django_filters.FilterSet):
    CLASS_CHOICES = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('8','8'),
        ('9','9'),
        ('10','10'),
        ('11','11'),
        ('12','12')
    ]
    class_name = django_filters.ChoiceFilter(field_name='examination_info__class_name', choices=CLASS_CHOICES , label='class')
    username = django_filters.CharFilter(field_name= 'user_info__user_info__username', lookup_expr='icontains', label='username')
    Email = django_filters.CharFilter(field_name = 'user_info__user_info__email', lookup_expr='icontains', label='email')
    num_of_correct_ans__gt = django_filters.NumberFilter(field_name='num_of_correct_ans', lookup_expr='gt',)
    num_of_correct_ans__lt = django_filters.NumberFilter(field_name='num_of_correct_ans', lookup_expr='lt')
    roll_num = django_filters.NumberFilter(field_name='user_info__roll_num', label='Roll No.')


    class Meta:
        model = UserQuizInfo
        fields = ['num_of_correct_ans']


class StudentInfoFilter(django_filters.FilterSet):

    class Meta:
        model = Student
        fields = '__all__'



class TeacherInfoFilter(django_filters.FilterSet):


    class Meta:
        model = Teacher
        fields = '__all__'



class PaymentInfoFilter(django_filters.FilterSet):

    class Meta:
        model = Payment
        fields = '__all__'
