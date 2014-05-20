from django.db import models
from django.contrib.auth.models import User
import ast
# Create your models here.

class ListField(models.TextField):
	__metaclass__ = models.SubfieldBase
	
	def __init__(self, *args, **kwargs):
		super(ListField, self).__init__(*args, **kwargs)
		
	def to_python(self, value):
		if not value:
			value = []
		if isinstance(value, list):
			return value
		return ast.literal_eval(value)
	def get_prep_lookup(self, value):
		if value is None:
			return value
		return unicode(value)
	def value_to_string(self, obj):
		value = self._get_val_from_obj(obj)
		return self.get_db_prep_value(value)

class Answer(models.Model):
	answer_text = models.CharField(max_length=500)
	answer_by = models.CharField(max_length=25)
	when = models.DateTimeField(auto_now_add=True)
	likes = models.DecimalField(max_digits=5,decimal_places=0)
	dislikes = models.DecimalField(max_digits=5,decimal_places=0)
	like_by_whom = ListField()
	dislike_by_whom = ListField()
	def __unicode__(self):
		return self.answer_text

class Forum(models.Model):
	forum_name = models.CharField(max_length=75)

	def __unicode__(self):
		return self.forum_name

class Question(models.Model):
	question_tag = models.CharField(max_length=75)
	question_text = models.CharField(max_length=500)
	asked_by = models.CharField(max_length=20)
	when = models.DateTimeField(auto_now_add=True)
	forum_name = models.CharField(max_length=75)
	answer = models.ManyToManyField(Answer, blank=True)

	def __unicode__(self):
		return "%s -- %s" % (self.question_tag, self.when)