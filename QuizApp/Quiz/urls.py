from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
    path('', views.home,name='home'),
    path('accounts/register', views.Register,name='Register'),
    path('user_profile', views.user_profile,name='user_profile'),
    path('user_profile', views.user_profile,name='user_profile'),
    path('del_user', views.del_user,name='del_user'),
    path('result', views.result,name='result'),
    path('quiz', views.quiz,name='quiz'),
    path('ourinfo', views.ourinfo,name='ourinfo'),
    path('submit_answer/<int:quest_id>', views.submit_answer,name='submit_answer'),

]

