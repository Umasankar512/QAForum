from django.conf.urls import url, pattern

urlpatterns = ('Questions.views',
		url(r'^$', view_question),
)
