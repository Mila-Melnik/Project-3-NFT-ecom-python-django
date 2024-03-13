from django.shortcuts import redirect, render
from .models import Product, Profile
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms

def update_info(request):
	if request.user.is_authenticated:
		current_user = Profile.objects.get(user__id=request.user.id)
		form = UserInfoForm(request.POST or None, instance=current_user)
	
		if form.is_valid():
			form.save()
			messages.success(request, "Your info has been updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form})
	else:
		messages.success(request, "Log in to view the page!")
		return redirect('home')
   


def update_password(request):
   if request.user.is_authenticated:
      current_user = request.user
      if request.method == 'POST':   
         form = ChangePasswordForm(current_user, request.POST)
         if form.is_valid():
            form.save()
            messages.success(request, "Password has been updated, please log in")
            login(request, current_user)
            return redirect('update_user')
         else: 
            for error in list(form.errors.values()):
               messages.error(request, error)
               return redirect("update_password")
         
      else:
         form = ChangePasswordForm(current_user)
         return render(request, "update_password.html", {'form':form})
   else:
       messages.success(request, "Log in to view the page!")
       return redirect('home')




def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User has been updated!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "Log in to access the page!")
		return redirect('home')
     
    

  
def home(request):
  products = Product.objects.all()
  return render(request, 'home.html', {'products':products})


def about (request): 
  return render(request, 'about.html', {})


def login_user(request):
  if request.method == "POST": 
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)

      messages.success(request, ("You have been logged in"))
      return redirect('home')
    else:
     
     messages.success(request, ("Check your credentials"))
    return redirect('login')
  
  else: 
    return render(request, 'login.html', {})



def logout_user(request):
  logout(request)
  messages.success(request, ("You have been logged out"))
  return redirect('home')

def register_user(request):
   form = SignUpForm()
   if request.method == "POST":
     form = SignUpForm(request.POST)
     if form.is_valid():
       form.save()
       username = form.cleaned_data['username']
       password = form.cleaned_data['password1']
       user = authenticate(username=username, password=password)
       login(request, user)
       messages.success(request,("You have registered!"))
       return redirect('update_info')
     else: 
      messages.success(request, ("Try again"))
      return redirect('register')
   else:
      return render(request, 'register.html', {'form':form})
