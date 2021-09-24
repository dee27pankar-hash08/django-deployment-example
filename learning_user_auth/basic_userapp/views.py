from django.shortcuts import render
from basic_userapp.forms import UserForm,UserInformationForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
# A LOT OF CODING FOR WORKING WITH USERS AND AUTHORIZATION HAPPENS IN THE VIEWS.PY FILE
#BASIC IDEA IS THAT WE CHECK IF THERRE IS A POST REQUEST AND THEN PERFORM SOME SORT OF ACTION BASED OFF THAT INFORMATION
#FIGURING OUT TH ERGISTRATION VIEWS IS AN EXTENTION OF WHAT WE LEARN ABOUT WHEN DISCUSSING DJANGO FORMS MAKE SURE TO REWIEW THAT CONTENT IF  NOT REMEMBERING

def index(request):
    return render(request,'basic_userapp/index.html')

@login_required
def appreciate(request):
    return HttpResponse("THANKYOU FOR LOGGING IN,YOU'RE AWESOME!")


@login_required
def user_logout(request):
    logout(request)#REVISE THIS PART
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserInformationForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)#this is setting the password as the hash
            user.save()

            profile = profile_form.save(commit=False)# SETTING UP THE ONE2ONE RELATIONSHIP DEFINED IN MODELS.PY
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserInformationForm()
    return render(request, 'basic_userapp/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered,})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")


        else:
            print("SOmeone Tried to Login And Failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")

    else:
        return render(request,'basic_userapp/login.html',{})
