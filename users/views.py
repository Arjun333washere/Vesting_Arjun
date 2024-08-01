#from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views import View
# Create your views here.


def login_view(request):
    if request.method == 'POST':#POST WHEN WE SEND DATA FROM THE USER ( clicking sign in)
        login_form = AuthenticationForm(request=request,data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            pass
    #GET = when user comes to login page using GET req so we GET the form
    elif request.method == 'GET':
        login_form = AuthenticationForm()
    return render(request,'views/login.html',{'login_form': login_form})

@login_required
def home_view(request):
    return render(request,"views/home.html")




class RegisterView(View):
    def get(self,request):
        register_form = UserCreationForm()
        return render(request,"views/register.html",{'register_form':register_form})

    def post(self,request):
        register_form = UserCreationForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            login(request,user)
            return redirect('home')
        else:
            print("eroor while registering")
            return render(request, 'views/register.html', {'register_form': register_form})
            #messages.error(request,f'An error occured trying to register')









""" def register_view(request):
    register_form = UserCreationForm()
    return render(request,"views/register.html",{'register_form':register_form})

def registerPost_view(request):
    register_form = UserCreationForm(data=request.POST)
    if register_form.is_valid():
        user = register_form.save()
        user.refresh_from_db()
        login(request,user)
        return redirect('home')
    else:
        print("eroor in registgering")
        return render(request,"views/register.html",{'register_form':register_form}) """


