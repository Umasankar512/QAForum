from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.template import RequestContext
from Questions.models import Question, Answer, ListField, Forum
from datetime import datetime
from django.contrib.auth.models import User
# Create your views here.

#class AskQuestion(ModelForm):

     #class Meta:
          #model = Question
          #fields = ('question_tag', 'question_text')
          #widgets = {
               #'question_tag': Textarea(attrs={'rows': '1', 'cols': '75'}),
               #'question_text': Textarea(attrs={'rows': '8', 'cols': '75'}),
          #}

def view_question(request, forumname, qno='0'):
     user = None
     message = ''
     if request.user.is_authenticated():
          user = request.user.username
     submitted = False
     ans = None
     print forumname
     question = Question.objects.get(id=qno)
     if request.method == 'POST':
          if request.POST['submit'] == 'Post':
               ans = request.POST.copy()
               if ans['answer'] != '':
                    answer = Answer()
                    answer.answer_text = ans['answer']
                    answer.answer_by = ans['user']
                    answer.likes = answer.dislikes = 0
                    answer.save()
                    question.answer.add(answer)
                    submitted = True
               else:
                    message = "Please Enter some Answer"
     forum = Forum.objects.all()
     return render_to_response('Questions/view_question.html', {'forum': forum, 'user': user,'question': question, 'ans_sub': submitted, 'ans': ans, 'message': message, 'forum_name': forumname}, context_instance=RequestContext(request))


def index(request):
     loggedin = False
     username = None
     if request.user.is_authenticated():
          loggedin = True
          username = request.user.username
     forum = Forum.objects.all()
     #return render_to_response('Questions/all.html', {'forum': forum, 'islogin': loggedin, 'username': username})
     return HttpResponseRedirect("/view/C")

def view_forum(request, forumname=''):
     success = False
     loggedin = False
     username = None     
     ques = None
     forum = Forum.objects.all()
     fnames_list = [f.forum_name for f in forum]
     if forumname in fnames_list:
          success = True
          ques = Question.objects.filter(forum_name=forumname)
     if request.user.is_authenticated():
          loggedin = True
          username = request.user.username
     return render_to_response('Questions/view_forum.html', {'forum': forum, 'success': success, 'questions': ques, 'forumname': forumname, 'isloggedin': loggedin, 'username': username})

def ask_question(request, fname):
     message = "Please fill both Input boxex to Post a new Question"
     success = False
     forum = Forum.objects.all()
     print fname
     if request.user.is_authenticated():
          if request.method == 'POST':
               if request.POST['submit'] == 'POST':
                    pdict = request.POST.copy()
                    user_prof = User.objects.get(username = request.user.username)
                    new_question = Question()
                    if pdict['question_title'] != "" and pdict['question_content'] != "":
                         print pdict['question_content']
                         new_question.question_tag = pdict['question_title']
                         new_question.question_text = pdict['question_content']
                         new_question.asked_by = user_prof.username
                         new_question.forum_name = fname
                         new_question.save()
                         message = "Question Posted Successfully"
                         success = True
                    return render_to_response("Questions/ask_question.html", {'forum': forum, 'msg': message, 'success': success, 'forum_name': fname}, context_instance=RequestContext(request))
          else:
               return render_to_response("Questions/ask_question.html", {'forum': forum, 'msg': message, 'success': success, 'forum_name': fname}, context_instance=RequestContext(request))
     else:
          return HttpResponseRedirect("/account/login")

def like_ans(request, aid, flag, qid, fname):
     answer = Answer.objects.get(id=aid)
     print aid, flag, qid
     if flag == "1":
          users = answer.like_by_whom
          if not request.user.username in users:
               print "Liked"
               answer.like_by_whom.append(request.user.username)
               answer.likes += 1
               answer.save()
     else:
          users = answer.dislike_by_whom
          print users
          if not request.user.username in users:
               print "Disliked"
               answer.dislike_by_whom.append(request.user.username)
               answer.dislikes += 1
               answer.save()
               print request.user.username
     return HttpResponseRedirect("/view/%s/%s" % (fname, qid))