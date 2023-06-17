from django.contrib import admin
from .models import Quiz,Option , Teacher, Student, Subject, ExaminationInfo ,UserQuizInfo,Payment,InstitutionInfo

# Register your models here.

admin.site.register(Quiz)
admin.site.register(Option)
admin.site.register(UserQuizInfo)

admin.site.register(Teacher)
admin.site.register(Student)
# admin.site.register(District)
# admin.site.register(Subdistrict)
# admin.site.register(Thana)

admin.site.register(InstitutionInfo)
admin.site.register(Subject)
admin.site.register(ExaminationInfo)
admin.site.register(Payment)



