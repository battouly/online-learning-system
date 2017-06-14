from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


# Create your views here.
from billing.models import Transaction
from notifications.models import Notification

from .forms import LoginForm, RegisterForm
from .models import MyUser


def sendSimpleEmail(request,emailto):
   res = send_mail("Salut!", "Comment tu vas?", "paul@polo.com", [emailto])
   return HttpResponse('%s'%res)

@login_required
def account_home(request):
	notifications = Notification.objects.get_recent_for_user(request.user, 6)
	transactions = Transaction.objects.get_recent_for_user(request.user, 3)
	context = {
		"notifications": notifications,
		"transactions": transactions
	}

	return render(request, "accounts/account_home.html", context)



def auth_logout(request):
	logout(request)
	return HttpResponseRedirect('/')
 


def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		print username, password
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			if next_url is not None:
				return HttpResponseRedirect(next_url)
			return HttpResponseRedirect("/")
	action_url = reverse("login")
	title = "Login"
	submit_btn = title
	submit_btn_class = "btn-success btn-block"
	extra_form_link = "Upgrade your account today <a href='%s'>here</a>!" %(reverse("account_upgrade"))
	context = {
		"form": form,
		"action_url": action_url,
		"title": title,
		"submit_btn": submit_btn,
		"submit_btn_class": submit_btn_class,
		"extra_form_link":extra_form_link
		}
	return render(request, "accounts/account_login_register.html", context)
	

def auth_register(request):
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password2']
		#MyUser.objects.create_user(username=username, email=email, password=password)
		new_user = MyUser()
		new_user.username = username
		new_user.email = email
		#new_user.password = password #WRONG
		new_user.set_password(password) #RIGHT
		new_user.save()

	action_url = reverse("register")
	title = "Register"
	submit_btn = "Create an account"

	context = {
		"form": form,
		"action_url": action_url,
		"title": title,
		"submit_btn": submit_btn
		}
	return render(request, "accounts/account_login_register.html", context)



from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )
from django.shortcuts import render, redirect

def login_view(request):
    print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Login"
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")
    return render(request, "posts/form.html", {"form":form, "title": title})


def register_view(request):
    print(request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Register"
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "posts/form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")