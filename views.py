from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms


def home(request):
    return render(request, "authentication/index.html")


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Required. Enter a valid email address.")
    first_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your first name.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required. Enter your last name.")
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name', 'password1', 'password2']

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
      
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            user.first_name=first_name
            user.save()
            
            return redirect('signin')  
    else:
        form = CustomUserCreationForm()
       
    return render(request, 'authentication/signup.html', {'form': form})



def signin(request):


    if request.method=='POST':
      
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            first_name=user.first_name
            return render(request,"authentication/index.html", {"first_name":first_name})
        else:
            messages.error(request,"no account")
            return redirect('home')


    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully.")
    return redirect('home')