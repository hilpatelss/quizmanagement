from django.shortcuts import render,redirect
from django.contrib import messages
from Quiz.models import questions
from Quiz.models import user_credentials
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from . import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    user=request.user

    return render(request,'home.html',{'user':user})

    
def user_profile(request):
    user=request.user
    score=models.score.objects.filter()
    return render(request,'user.html',{'user':user,'score':score})

def loginuser(request):
    
    if request.method=='POST':
        
        username=request.POST('username')
        password=request.POST('password')
        
        user=authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home.html')
        else:
            messages.success(request,"Invalid Email or Password")
            return render('login.html')
    return render(request,'registration/login.html')
def Register(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        inst_code=request.POST.get('it_code')
        password=request.POST.get('password')
        user= User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        user.save()
        return redirect('login')
        
    return render(request,'registration/register.html')

from datetime import timedelta
@login_required
def quiz(request):
    question=questions.objects.filter().order_by('id').first()
    lastattempt=None
    futuretime=None
    hourslimit=24
    countattempt=models.attempt.objects.filter(user=request.user).count()
    if countattempt == 0 :
        models.attempt.objects.create(user=request.user)
    else:
        lastattempt=models.attempt.objects.filter(user=request.user).order_by('-id').first()
        futuretime=lastattempt.attempttime + timedelta(hours=hourslimit)
        if lastattempt and lastattempt.attempttime < futuretime:
            return render(request,'home.html')
        else:
            models.attempt.objects.create(user=request.user)
    return render(request,'test.html',{'question':question,'lastattempt':futuretime})

@login_required
def submit_answer(request,quest_id):
    if request.method=='POST':
        
        question=questions.objects.filter(id__gt=quest_id).order_by('id').exclude(id=quest_id).first()
        
        if 'skip' in request.POST:
            if question :
                quest=models.questions.objects.get(id=quest_id)
                user=request.user
                answer='Not Submitted'
                models.UserSubmittedAnswer.objects.create(user=user,question=quest,submitted_answer=answer)
                return render(request,'test.html',{'question':question})
            else:
                quest=models.questions.objects.get(id=quest_id)
                user=request.user
                answer='Not Submitted'
                models.UserSubmittedAnswer.objects.create(user=user,question=quest,submitted_answer=answer)
        else:
            quest=models.questions.objects.get(id=quest_id)
            
            user=request.user
            answer=request.POST['answer']
            models.UserSubmittedAnswer.objects.create(user=user,question=quest,submitted_answer=answer)
        if question:
            return render(request,'test.html',{'question':question})
        else:
            result=models.UserSubmittedAnswer.objects.filter(user=request.user)
            total_questions=result.count()
            skipped=models.UserSubmittedAnswer.objects.filter(user=request.user,submitted_answer='Not Submitted').count()
            attempted=models.UserSubmittedAnswer.objects.filter(user=request.user).exclude(submitted_answer='Not Submitted').count()
            rightAns=0
            percentage=0
            for row in result:
                if row.submitted_answer == row.question.right_answer:
                    rightAns+=1
            percentage=round((rightAns*100)/result.count(),2)
            models.score.objects.create(user=user,total_questions=total_questions,total_skipped=skipped,total_attempted=attempted,right_answers=rightAns,percentage=percentage)
            return render(request,'result.html',{'result':result,'total_skipped':skipped,'attempted':attempted,'rightAns':rightAns,'percentage':percentage})
            
    else:
        return HttpResponse('Method not Allowed!!')
    
@login_required
def result(request):
    result=models.UserSubmittedAnswer.objects.filter(user=request.user)
    skipped=models.UserSubmittedAnswer.objects.filter(user=request.user,submitted_answer='Not Submitted').count()
    attempted=models.UserSubmittedAnswer.objects.filter(user=request.user).exclude(submitted_answer='Not Submitted').count()
    rightAns=0
    percentage=0
    for row in result:
        if row.submitted_answer == row.question.right_answer:
            rightAns+=1
    percentage=round((rightAns*100)/result.count(),2)
    lastattempt=None
    futuretime=None
    hourslimit=24
    countattempt=models.attempt.objects.filter(user=request.user).count()
    if countattempt == 0 :
        models.attempt.objects.create(user=request.user)
    else:
        lastattempt=models.attempt.objects.filter(user=request.user).order_by('-id').first()
        futuretime=lastattempt.attempttime + timedelta(hours=hourslimit)
        if lastattempt and lastattempt.attempttime < futuretime:
            return render(request,'result.html',{'result':result,'total_skipped':skipped,'attempted':attempted,'rightAns':rightAns,'percentage':percentage})
            
        else:
            models.UserSubmittedAnswer.objects.filter().delete()
    
    return render(request,'result.html',{'result':result,'total_skipped':skipped,'attempted':attempted,'rightAns':rightAns,'percentage':percentage})


def ourinfo(request):
    return render(request,'admin.html')

def del_user(request): 
        
        u = request.user
        u.delete()
        return redirect('home')
 
    