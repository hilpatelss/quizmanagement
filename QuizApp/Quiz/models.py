from django.db import models
from django.contrib.auth.models import User

 #Create your models here.
class questions(models.Model):
    
    question=models.TextField()
    opt_1=models.CharField(max_length=200)
    opt_2=models.CharField(max_length=200)
    opt_3=models.CharField(max_length=200)
    opt_4=models.CharField(max_length=200)
    right_answer=models.CharField(max_length=200)
    


    class Meta:
        verbose_name_plural='Questions'
    
    
    
class user_credentials(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    username=models.CharField(max_length=10, unique=True)
    email=models.EmailField()
    inst_code=models.CharField(max_length=200)
    password=models.CharField(max_length=100)
   
    
       
    
    def __str__(self):
        return self.username
    class Meta:
        verbose_name_plural='User Credentials'
class UserSubmittedAnswer(models.Model):    
    question=models.ForeignKey(questions,on_delete=models.CASCADE,null=True)    
    user=models.ForeignKey(User,on_delete=models.CASCADE)    
    submitted_answer=models.CharField(max_length=200)          
    class Meta:        
        verbose_name_plural='User Submitted Answers'

class attempt(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    attempttime=models.DateTimeField(auto_now_add=True)
    class Meta:        
        verbose_name_plural='Attempt'
    
class score(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="",null=True,blank=True)
    total_questions=models.IntegerField()
    total_skipped=models.IntegerField()
    total_attempted=models.IntegerField()
    right_answers=models.IntegerField()
    percentage=models.IntegerField()
    class Meta:        
        verbose_name_plural='Score'
    
    