from django.contrib import admin
from Questions.models import Question, Answer, Forum
# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Forum)