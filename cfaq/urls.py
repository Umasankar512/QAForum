from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cfaq.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('Questions.views',
                url(r'^view/(?P<forumname>\w+)/(?P<qno>\d+)/$', 'view_question'),
                url(r'^view/(?P<forumname>\w+)/$', 'view_forum'),
                url(r'^$', 'index'),
                url(r'^ask/(?P<fname>\w+)$', 'ask_question'),
                url(r'^(?P<aid>\d+)/(?P<flag>\d+)/(?P<qid>\d+)/(?P<fname>\w+)/$', 'like_ans'),
)

urlpatterns += patterns('Account.views',
                url(r'^account/login', 'login'),
                url(r'^account/auth', 'auth_view'),
                url(r'^account/loggedin', 'loggedin'),
                url(r'^account/logout', 'logout'),
                url(r'^account/invalid', 'invalid'),
                url(r'^account/register', 'register'),
                url(r'^account/success', 'register_success'),
                url(r'^account/confirm/(?P<activation_key>\w+)/$', 'confirm'),
)
