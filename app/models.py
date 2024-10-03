from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
   
    email = models.EmailField(unique=True)
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'





class Teacher(CustomUser):
    age=models.IntegerField(default=0)
    mobile=models.IntegerField()
    image=models.ImageField(upload_to='photos/teachers')
    certificas=models.CharField(max_length=300)
   
    

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'


class Student(CustomUser):
    age=models.IntegerField(default=0)
    mobile=models.IntegerField()
    image=models.ImageField(upload_to='photos/students')
    Academic_stage=models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        
        

    
 
    
    
class Questionset(models.Model):
    title=models.CharField(max_length=100)
    Limit_of_success=models.DecimalField(max_digits=5,decimal_places=2)
    Number_of_successful=models.IntegerField(default=0)
    Number_of_failures=models.IntegerField(default=0)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    
          
class Question(models.Model):
    content=models.TextField(max_length=1000)
    grade=models.DecimalField(max_digits=5,decimal_places=2)
    questionset=models.ForeignKey(Questionset,on_delete=models.CASCADE)
      
    
class Answer(models.Model):
    is_true=models.BooleanField(default=False)
    content=models.TextField(max_length=1000)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
       
class Exams_Results(models.Model):
    name_questionset=models.CharField(max_length=100)
    is_succeed=models.BooleanField(default=False)
    grade=models.DecimalField(max_digits=5,max_length=5,decimal_places=2)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    
    
class Exam(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    start=models.DateTimeField(auto_now_add=True)
    end=models.DateTimeField()
    questionset=models.ForeignKey(Questionset,on_delete=models.CASCADE)