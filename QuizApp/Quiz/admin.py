from django.contrib import admin
from . import models
 #Register your models here.
admin.site.register(models.questions)
admin.site.register(models.user_credentials)
class scoreAdmin(admin.ModelAdmin):
    list_display=['user','percentage']
admin.site.register(models.score,scoreAdmin)
class UserSubmittedAnswerAdmin(admin.ModelAdmin):
    list_display=['id','question','user','submitted_answer']
admin.site.register(models.UserSubmittedAnswer,UserSubmittedAnswerAdmin)
class attemptAdmin(admin.ModelAdmin):
    list_display=['user','attempttime']
admin.site.register(models.attempt,attemptAdmin)

