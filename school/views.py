from django.shortcuts import render,redirect,reverse, HttpResponse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from plotly.offline import plot
from plotly.graph_objs import Scatter, Layout
import json

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/index.html')



#for showing signup/login button for teacher(by GEC)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/adminclick.html')


#for showing signup/login button for teacher(by GEC)
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/teacherclick.html')


#for showing signup/login button for student(by GEC)
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/studentclick.html')





def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'school/adminsignup.html',{'form':form})




def student_signup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'school/studentsignup.html',context=mydict)


def teacher_signup_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacherlogin')
    return render(request,'school/teachersignup.html',context=mydict)






#for checking user is techer , student or admin(by GEC)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        accountapproval=models.TeacherExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher-dashboard')
        else:
            return render(request,'school/teacher_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('student-dashboard')
        else:
            return render(request,'school/student_wait_for_approval.html')




#for dashboard of admin

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=models.TeacherExtra.objects.all().filter(status=True).count()
    pendingteachercount=models.TeacherExtra.objects.all().filter(status=False).count()

    studentcount=models.StudentExtra.objects.all().filter(status=True).count()
    pendingstudentcount=models.StudentExtra.objects.all().filter(status=False).count()

  
    notice=models.Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay(by GEC)
    mydict={
        'teachercount':teachercount,
        'pendingteachercount':pendingteachercount,

        'studentcount':studentcount,
        'pendingstudentcount':pendingstudentcount,

     
      
        'notice':notice

    }

    return render(request,'school/admin_dashboard.html',context=mydict)







#for teacher section by admin

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request,'school/admin_teacher.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-teacher')
    return render(request,'school/admin_add_teacher.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers=models.TeacherExtra.objects.all().filter(status=True)
    return render(request,'school/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_teacher_view(request):
    teachers=models.TeacherExtra.objects.all().filter(status=False)
    return render(request,'school/admin_approve_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    return redirect(reverse('admin-approve-teacher'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-approve-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)

    form1=forms.TeacherUserForm(instance=user)
    form2=forms.TeacherExtraForm(instance=teacher)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST,instance=user)
        form2=forms.TeacherExtraForm(request.POST,instance=teacher)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-teacher')
    return render(request,'school/admin_update_teacher.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_teacher_salary_view(request):
    teachers=models.TeacherExtra.objects.all()
    return render(request,'school/admin_view_teacher_salary.html',{'teachers':teachers})






#for student by admin

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'school/admin_student.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request,'school/admin_add_student.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=True)
    return render(request,'school/admin_view_student.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_from_school_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-approve-student')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentExtraForm(request.POST,instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('admin-view-student')
    return render(request,'school/admin_update_student.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students=models.StudentExtra.objects.all().filter(status=False)
    return render(request,'school/admin_approve_student.html',{'students':students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_student_view(request,pk):
    students=models.StudentExtra.objects.get(id=pk)
    students.status=True
    students.save()
    return redirect(reverse('admin-approve-student'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_student_fee_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'school/admin_view_student_fee.html',{'students':students})






#attendance related view
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_attendance_view(request):
    return render(request,'school/admin_attendance.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    print(students)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('admin-attendance')
        else:
            print('form invalid')
    return render(request,'school/admin_take_attendance.html',{'students':students,'aform':aform})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/admin_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/admin_view_attendance_ask_date.html',{'cl':cl,'form':form})









#fee related view by admin
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_fee_view(request):
    return render(request,'school/admin_fee.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_fee_view(request,cl):
    feedetails=models.StudentExtra.objects.all().filter(cl=cl)
    return render(request,'school/admin_view_fee.html',{'feedetails':feedetails,'cl':cl})








#notice related views
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('admin-dashboard')
    return render(request,'school/admin_notice.html',{'form':form})








#for TEACHER  LOGIN    
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.TeacherExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
       
        'mobile':teacherdata[0].mobile,
        'date':teacherdata[0].joindate,
        'notice':notice
    }
    return render(request,'school/teacher_dashboard.html',context=mydict)



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    return render(request,'school/teacher_attendance.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request,cl):
    students=models.StudentExtra.objects.all().filter(cl=cl)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=models.Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('teacher-attendance')
        else:
            print('form invalid')
    return render(request,'school/teacher_take_attendance.html',{'students':students,'aform':aform})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/teacher_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/teacher_view_attendance_ask_date.html',{'cl':cl,'form':form})



@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('teacher-dashboard')
        else:
            print('form invalid')
    return render(request,'school/teacher_notice.html',{'form':form})







#FOR STUDENT AFTER THEIR Login
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=models.Notice.objects.all()
    mydict={
        'roll':studentdata[0].roll,
        'mobile':studentdata[0].mobile,
       
        'notice':notice
    }
    return render(request,'school/student_dashboard.html',context=mydict)



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            studentdata=models.StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
            attendancedata=models.Attendance.objects.all().filter(date=date,cl=studentdata[0].cl,roll=studentdata[0].roll)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/student_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/student_view_attendance_ask_date.html',{'form':form})



def student_academics_add_result(request):
    # Subjects = []
    # semester = None
    studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    roll = studentdata[0].roll
    form = forms.SelectSemester()
    if(request.method == "POST"):
        semester = request.POST.get('sem')[0]
        Subjects = models.Subject.objects.all().filter(semester = semester) 
        marks_list = request.POST.getlist('marks')
        print('semester', semester)
        gp_list = request.POST.getlist('gp')
        i = 0
        for subject in Subjects:

            print('roll =', roll, 'subject_code =', subject.subject_code, 'obtained_marks =', marks_list[i], 'obtained_gp =', gp_list[i])
            academics = models.Academics(roll = roll, subject_code = subject.subject_code, obtained_marks = marks_list[i], obtained_gp = gp_list[i])
            i += 1

            academics.save()

    Subjects = models.Subject.objects.all() 
    subject_dict = {}
    for subject in Subjects:

        subject_code = subject.subject_code
        semester = subject.semester
        subject_name = subject.subject_name
        total_marks = subject.subject_total_marks
        total_credits = subject.total_credits
        if semester not in subject_dict:
            subject_dict[semester] = []
        subject_dict[semester].append([semester,subject_code, subject_name, total_marks, total_credits])
        
    subject_details_json  = json.dumps(subject_dict)

    context={
        "subject_details_json":subject_details_json,
        "subjects":Subjects
    } 
    # print("CONTEXT ", context)

    return render(request,'school/student_academics_add_result.html',context)
   


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_academics_analysis(request):

    return render(request, "school/student_academics_analysis.html")


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_vs_subject_graph(request):

    studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    roll = studentdata[0].roll

    # FROM HELPER FUNCTION BELOW
    semester_wise_details = get_student_data_sem_wise(roll)


    subject_names = semester_wise_details['subject_names']
    subject_codes = semester_wise_details['subject_codes']
    student_marks = semester_wise_details['student_marks']
    print(subject_names)
    print(subject_codes)
    x_data = subject_names
    y_data = student_marks
    plot_div = plot(
        dict(
            data = [ Scatter(x=x_data, y=y_data,
                        mode='lines+markers+text', name='marks_vs_subject',
                        opacity=0.9, marker_color='green')],
            layout = Layout(
                    title='<b>Marks Vs Subject</b>',
                    xaxis=dict(
                            title="<b>Subjects</b>",
                            linecolor = "black",
                            linewidth = 0.5,
                            mirror = True),
                    yaxis=dict(
                        title="<b>Obtained Marks</b>",
                        linecolor = "black",
                        linewidth = 0.5,
                        mirror = True),
                     
                    )
             ),  
        output_type='div')
    return render(request, "school/student_marks_vs_subject_graph.html", context={'plot_div': plot_div})



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_vs_semester_graph(request):

    studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    roll = studentdata[0].roll
    semester_wise_details = get_student_data_sem_wise(roll)

    sem_marks_obtained_dict = semester_wise_details['sem_marks_obtained_dict']
    sem_marks_total_dict = semester_wise_details['sem_marks_total_dict']
    semesters_name = list(sem_marks_obtained_dict.keys())

    sum_obtained_marks_list = []
    sum_total_marks_dict = {}
    sum_obtained_marks_dict = {}
    sum_total_marks_list = []

    for val in sem_marks_obtained_dict: 
        print('')
        print('VAL', val)
        sum_m = 0

        for mark in sem_marks_obtained_dict[val]: 
            sum_m += int(mark) 
        print('SUM',sum_m)
        print('')
        sum_obtained_marks_dict[val] = sum_m
        sum_obtained_marks_list.append(sum_m) 

    for val in sem_marks_total_dict: 
        sum_m = 0

        for mark in sem_marks_total_dict[val]: 
            sum_m +=int(mark) 
        sum_total_marks_dict[val] = sum_m
        sum_total_marks_list.append(sum_m) 
  

    i=0
    sem_total_obtained_dict = {}
    for sem in semesters_name:
        val = []
        val.append(sum_obtained_marks_list[i])
        val.append(sum_total_marks_list[i])
        percent = sum_obtained_marks_list[i]/sum_total_marks_list[i]*100
        val.append(round(percent,2))
        i += 1
        sem_total_obtained_dict[sem] = val
 

    x_data = semesters_name
    y1_data = sum_obtained_marks_list
    y2_data = sum_total_marks_list
    plot_div = plot(
        dict(
            data = [ Scatter(x=x_data, y=y1_data,
                          mode='lines+markers+text', name='obtained marks',
                        opacity=1, marker_color='green'),
                     Scatter(x=x_data, y=y2_data,
                          mode='lines+markers+text', name='total marks',
                        opacity=0.6, marker_color='orange')],
            layout = Layout(
                    
                    title='<b>Total Marks in Each Semester</b>',
                    xaxis=dict(
                        title="<b>Semester</b>",
                        tickmode = 'linear',
                        dtick = 1,
                        range=[1,8],
                        linecolor = "black",
                        linewidth = 0.5,
                        mirror = True),
                    yaxis=dict(
                        title="<b>Total Marks</b>", 
                        linecolor = "black",
                        linewidth = 0.5,
                        mirror = True),
                     
                    )
             ),  
        output_type='div')

    context={
        "sem_total_obtained_dict": sem_total_obtained_dict,
        "plot_div":plot_div
    }
    return render(request, "school/student_marks_vs_semester_graph.html", context)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_cpi_spi(request):

    studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    roll = studentdata[0].roll
    semester_wise_details = get_student_data_sem_wise(roll)

    sem_gp_dict = semester_wise_details['sem_gp_dict']
    sem_credit_dict = semester_wise_details['sem_credit_dict']
    semesters = semester_wise_details['semesters']
    sem_marks_obtained_dict = semester_wise_details['sem_marks_obtained_dict']

    semesters_name = list(sem_marks_obtained_dict.keys())
    sum_marks = 0
    sum_array = []
    for val in sem_marks_obtained_dict: 
        for mark in sem_marks_obtained_dict[val]: 
            sum_marks +=int(mark) 
        sum_array.append(sum) 
    
    marks_sum = sum_array

    sem_wise_n = {}
    sem_wise_d = {}
    sem_wise_spi = {}
    sem_wise_cpi = {}
    sem_wise_cpi_spi = {}
    total_n = 0
    total_d = 0
    for sem in sem_gp_dict:
        gps = sem_gp_dict[sem]
        gps = list(map(int, gps))
        credits = sem_credit_dict[sem]
        credits = list(map(int, credits))
        n = [a*b for a,b in zip(gps,credits)]
        d = sum(credits)
        sem_wise_d[sem] = d
        sem_wise_n[sem] = sum(n)
        spi = sum(n)/d
        spi = round(spi, 2)
        total_n = total_n+sum(n)
        total_d = total_d+d
        cpi = total_n/total_d
        cpi = round(cpi,2)
        sem_wise_spi[int(sem)] = spi
        sem_wise_cpi[int(sem)] = total_n/total_d
        sem_wise_cpi_spi[int(sem)] = [spi, cpi]

    

    x_data = list(sem_wise_cpi_spi.keys())
    y1_data = list(sem_wise_cpi.values())
    y2_data = list(sem_wise_spi.values())
    
    plot_div = plot(
        dict(
            data = [ Scatter(x=x_data, y=y1_data,
                          mode='lines+markers+text', name='cpi',
                        opacity=0.9, marker_color='green'),
                    Scatter(x=x_data, y=y2_data,
                      mode='lines+markers+text', name='spi',
                    opacity=0.9, marker_color='orange')],
            layout = Layout(
                    
                    title='<b>CPI V/S SPI</b>',
                    xaxis=dict(
                        title="<b>Semester</b>",
                        tickmode = 'linear',
                        dtick = 1,
                        range=[1,8],
                        linecolor = "black",
                        linewidth = 0.5,
                        mirror = True),
                        
                    yaxis=dict(
                        title="<b>Points</b>",
                        dtick = 0.5,
                        linecolor = "black",
                        linewidth = 0.5,
                        mirror = True
                      ),
                     
                    )
             ),  
        output_type='div')

    print('x_data', x_data)
    print('y1_data', y1_data)
    print('y2_data', y2_data)
    
    print('sem_wise_n', sem_wise_n)
    print('sem_wise_d', sem_wise_d)
    print('sem_wise_spi', sem_wise_spi)
    print('sem_wise_cpi', sem_wise_cpi)
    print('sem_wise_cpi_spi', sem_wise_cpi_spi)
    print('total_d', total_d)
    print('total_n', total_n)

    context = {
        "sem_wise_cpi_spi": sem_wise_cpi_spi,
        'plot_div': plot_div 
    }
    return render(request, "school/student_cpi_spi.html",context)




# for about us and contact us
def aboutus_view(request):
    return render(request,'school/aboutus.html')

def about_developers_view(request): 
    return render(request,'school/about_developers_view.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['wapka1503@gmail.com'], fail_silently = False)
            return render(request, 'school/contactussuccess.html')
    return render(request, 'school/contactus.html', {'form':sub})




#helper fcuntion

def get_student_data_sem_wise(roll):
    academic_details = models.Academics.objects.all().filter(roll = roll)

    student_marks = []
    student_gps = []
    subject_credits = []
    subject_codes = []
    subject_names = []
    subject_total_marks = []
    semesters = []

    # FROM ACADEMIC DETAILS MODEL
    for academic_detail in academic_details:
        student_marks.append(academic_detail.obtained_marks)
        student_gps.append(academic_detail.obtained_gp)
        subject_codes.append(academic_detail.subject_code)

    # FROM SUBJECT MODEL
    for code in subject_codes:
        subject_names.append(models.Subject.objects.get(subject_code = code).subject_name)
        semesters.append(models.Subject.objects.get(subject_code = code).semester)
        subject_credits.append(models.Subject.objects.get(subject_code = code).total_credits)
        subject_total_marks.append(models.Subject.objects.get(subject_code = code).subject_total_marks)

    sem_marks_obtained_dict = {}
    i = 0
    for s in semesters: 
        if s not in sem_marks_obtained_dict: 
            sem_marks_obtained_dict[s] = [] 
        sem_marks_obtained_dict[s].append(student_marks[i]) 
        i += 1 

    sem_marks_total_dict = {}
    i = 0
    for s in semesters: 
        if s not in sem_marks_total_dict: 
            sem_marks_total_dict[s] = [] 
        sem_marks_total_dict[s].append(subject_total_marks[i]) 
        i += 1 
        
    sem_gp_dict = {}
    i = 0
    for s in semesters: 
        if s not in sem_gp_dict: 
            sem_gp_dict[s] = [] 
        sem_gp_dict[s].append(student_gps[i]) 
        i += 1 

    sem_credit_dict = {}
    i = 0
    for s in semesters: 
        if s not in sem_credit_dict: 
            sem_credit_dict[s] = [] 
        sem_credit_dict[s].append(subject_credits[i]) 
        i += 1 

    semesters_name = list(sem_marks_obtained_dict.keys())
    sum = 0
    sum_array = []
    for val in sem_marks_obtained_dict: 
        for mark in sem_marks_obtained_dict[val]: 
            sum +=int(mark) 
        sum_array.append(sum) 
    
    marks_sum = sum_array

    print('student_marks ',student_marks)
    print('student_gps ',student_gps)
    print('subject_codes ',subject_codes)
    print('subject_total_marks ',subject_total_marks)
    print('semesters  ',semesters )
    print('sem_marks_obtained_dict', sem_marks_obtained_dict)
    print('sem_marks_total_dict', sem_marks_total_dict)
    print('sem_gp_dict', sem_gp_dict)
    print('sem_credit_dict', sem_credit_dict)

    return {
        "student_marks":student_marks,
        'student_gps':student_gps,
        'subject_codes':subject_codes,
        'subject_names':subject_names,
        'sem_marks_total_dict':sem_marks_total_dict,
        'semesters':semesters,
        'sem_marks_obtained_dict': sem_marks_obtained_dict,
        'sem_gp_dict': sem_gp_dict,
        'sem_credit_dict': sem_credit_dict
    }






 # return HttpResponse( "contact  Page")
    
# to be deleted as i am not sure
# def student_academic_add_result_table(request, url, Subjects):
#     studentdata=models.StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
#     roll = studentdata[0].roll
#     print("Subjects", Subjects)
#     print('REQUEST',request )
#     print("INSIDE ELSE")

#     if(request.method == "POST"):
#         marks_list = request.POST.getlist('marks')
#         gp_list = request.POST.getlist('gp')
#         i = 0
#         for subject in Subjects:
#             print('roll =', roll, 'subject_code =', subject.subject_code, 'obtained_marks =', marks_list[i], 'obtained_gp =', gp_list[i])
#             academics = models.Academics(roll = roll, subject_code = subject.subject_code, obtained_marks = marks_list[i], obtained_gp = gp_list[i])
#             i += 1
#             academics.save()

#     # print('semestereee', semester)
#     context={
#         "sem":[1,2,3,4,5,6,7,8],
#         "pr":pr,
#         "subjects":Subjects,
#     } 
#     return render(request,url,context)




# ADD AT LINE 645
        # if(request.POST['semester']):
        #     print("INSIDE IF")
        #     form = form(request.POST)
        #     print('after form', form)
        #     semester = request.POST['semester']
        #     print('semester',semester)
        
        #     Subjects = models.Subject.objects.all().filter(semester = semester) 
            
        #     context={
        #         "sem":[1,2,3,4,5,6,7,8],
        #         "pr":pr,
        #         "subjects":Subjects,
        #         "form": form
        #     } 
        #     print(' CONTEXT ',context)
        #     getRequest = request.method
        #     student_academic_add_result_table(request,'school/student_academics_add_result.html',Subjects )
        #     # return render(request,'school/student_academics_add_result.html',context)



