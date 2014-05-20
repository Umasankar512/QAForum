import datetime, random, sha
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django import forms
from django.forms import ModelForm, TextInput, PasswordInput
from Account.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from Questions.models import Forum
# Create your views here.



def isValidUsername(uname):
    try:
        User.objects.get(username=uname)
    except User.DoesNotExist:
        return 1
    return 0

    

def login(request):
    forum = Forum.objects.all()
    c = {}
    c.update(csrf(request))
    c['forum'] = forum
    return render_to_response('Account/login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    
    user = auth.authenticate(username=username, password=password)
    
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/account/invalid")
    
    
def loggedin(request):
    return HttpResponseRedirect("/")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/account/login")

def invalid(request):
    forum = Forum.objects.all()
    return render_to_response("Account/invalid_login.html", {'forum': forum})

def user_enters_data_or_not(data):
    if data['username'] == '' or data['password'] == '' or data['confirm'] == '' or data['email_id'] == '':
        return 1
    return 0

def register(request):
    forum = Forum.objects.all()
    message = "User registration"
    if request.method == 'POST':
        if request.POST['submit'] == 'Register':
            userobj = request.POST.copy()
            if user_enters_data_or_not(request.POST.copy()):
                message = 'Please enter data in all fields'
                return render_to_response("Account/register.html", {'message': message, 'forum': forum})
            if isValidUsername(userobj['username']):
                if userobj['password'] == userobj['confirm']:
                    new_user = User.objects.create_user(username=userobj['username'], email=userobj['email_id'], 
                                                   password=userobj['password'])
                    new_user.save()
                    
                    salt = sha.new(str(random.random())).hexdigest()[:5]
                    ak = sha.new(str(salt+userobj['username'])).hexdigest()
                    k_expires = datetime.datetime.today() + datetime.timedelta(2)
                    new_profile = UserProfile(user=new_user, is_active=False, activation_key=ak, key_expires=k_expires)
                    new_profile.save()
                    
                    #email_subject = 'Please confirm your registration'
                    #email_body = "Hello, %s, and thanks for signing up for an account in cfaq.herokuapp.com!!\nTO activate your account, click this link within 48 hours http://cfaq.herokuapp.com/account/confirm/%s" % (userobj['username'], ak)
                    
                    #send_mail(email_subject, email_body, 'admin@cfaq.herokuapp.com', [userobj['email_id']])
                    
                    return HttpResponseRedirect("/account/success")
                else:
                    message = 'Passwords do not match.. Please re-enter again'
            else:
                message = 'Username Already Exist.. Choose another name'
    args = {}
    args.update(csrf(request))
    args['message'] = message
    args['forum'] = forum
    return render_to_response("Account/register.html", args)


def register_success(request):
    forum = Forum.objects.all()
    return render_to_response("Account/register_success.html", {'forum': forum})

def confirm(request, activation_key):
    if request.user.is_authenticated():
        return render_to_response("/", {'user': user})
    user_profile = get_object_or_404(UserProfile, activation_key = activation_key)
    
    if user_profile.key_expires < datetime.datetime.today():
        user_profile = UserProfile.objects.get(activation_key=activation_key)
        user_profile.delete()
        return render_to_response("Account/confirm.html", {'expired': True})
    user_Account = user_profile.user
    user_Account.is_active = True
    user_Account.save()
    return render_to_response('Account/confirm.html', {'success': True})