from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TeacherExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    joindate=models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=40)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name




sem=[('one','one'),('two','two'),('three','three'),
('four','four'),('five','five'),('six','six'),('seven','seven'),('eight','eight')]
class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll = models.CharField(max_length=12)
    mobile = models.CharField(max_length=12,null=True)
    cl= models.CharField(max_length=10,choices=sem,default='one')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name



class Attendance(models.Model):
    roll=models.CharField(max_length=12,null=True)
    date=models.DateField()
    cl=models.CharField(max_length=10)
    present_status = models.CharField(max_length=10)
    def __str__(self):
        return self.roll+" "+self.date
    


class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='school')
    message=models.CharField(max_length=500)
    def __str__(self):
        return self.message
    

class Subject(models.Model):
    subject_code = models.CharField(max_length=11, null=False, primary_key=True)
    subject_name = models.CharField(max_length=80, null=False)
    semester = models.CharField(max_length=2, null=False)
    total_credits = models.CharField(max_length=2, null=False)
    subject_total_marks = models.CharField(max_length=3, null=False, default="120")
    
    def __str__(self):
        return self.subject_code+" "+self.subject_name
    

class Academics(models.Model):
    roll = models.CharField(max_length=12, null = False)
    subject_code = models.CharField(max_length=11, null=False)
    obtained_marks = models.CharField(max_length=4, null=False, default="")
    obtained_gp = models.CharField(max_length=2, null=False)
     
    def __str__(self):
        return self.roll+" "+self.subject_code
    
