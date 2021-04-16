from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from django.contrib import messages
from .models import *


def index(request):
    return render(request, "login.html")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/main')
        return redirect('/main')
    messages.error(request, "Invalid login")
    return redirect("/main")


def register(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        messages.error(request, "email is already in use", extra_tags="email")
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    this_user = User.objects.create(email=request.POST['email'], firstn=request.POST['firstn'],namesuf=request.POST['namesuf'], username=request.POST['username'], password=pw_hash)
    request.session['user_id'] = this_user.id
    return redirect("/")


def main(request):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "main.html", context)


def logout(request):
    del request.session['user_id']
    return redirect('/')


def return_m(request):
    return redirect("/main")