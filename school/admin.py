from django.contrib import admin
from .models import Attendance,StudentExtra,TeacherExtra,Notice, Subject, Academics
# Register your models here. (by GEC.luv)
class StudentExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(StudentExtra, StudentExtraAdmin)

class TeacherExtraAdmin(admin.ModelAdmin):
    pass
admin.site.register(TeacherExtra, TeacherExtraAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attendance, AttendanceAdmin)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)


class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subject, NoticeAdmin)

class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Academics, NoticeAdmin)
