from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Task
from .forms import TaskForm
from django.utils import timezone

def home(request):
    return render(request, "home.html")

#CRUD
@login_required
def tasks(request):
    current_tasks = Task.objects.filter(user = request.user, complete_date__isnull = True).order_by("-create_date")
    complete_tasks = Task.objects.filter(user = request.user, complete_date__isnull = False).order_by("-create_date")
    return render(request,"tasks.html",{"current_tasks":current_tasks,"complete_tasks":complete_tasks})

@login_required
def task_details(request, taskID):
    task = get_object_or_404(Task, pk = taskID, user = request.user)
    if request.method == "GET":
        form = TaskForm(instance=task)
        return render(request,"task_details.html",{"form":form,"task":task})
    else:
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task.save()
            return redirect("tasks")
        else:
            form = TaskForm(instance=task)
            message = "Something went wrong! Please try again!"
            return render(request,"task_details.html",{"form":form,"task":task})

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html",{"form":TaskForm()})
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("home")
        else:
            message = "Something went wrong. Please try again!"
            return render(request, "create_task.html",{"form":TaskForm(),"message":message})

@login_required
def complete_task(request, taskID):
    task = get_object_or_404(Task, user=request.user, pk=taskID)
    now = timezone.now()
    task.complete_date = now
    task.save()
    return redirect("tasks")

@login_required
def delete_task(request, taskID):
    task = get_object_or_404(Task, user=request.user, pk=taskID)
    task.delete()
    return redirect("tasks")








#auth
def register(request):
    if request.method=="GET":
        return render(request, "register.html",{"form":UserCreationForm()})
    else:
        if request.POST.get("password1") == request.POST.get("password2"):
            username = request.POST.get("username")
            password = request.POST.get("password1")
            try:
                user = User.objects.create_user(username=username,password=password)
            except IntegrityError:
                message = "This username is already taken. Please try again!"
                return render(request, "register.html",{"form":UserCreationForm(),"message":message})
            else:
                user.save()
                return redirect("home")
        else:
            message = "Password doesn't match. Try again!"
            return render(request, "register.html",{"form":UserCreationForm(),"message":message})

def login_user(request):
    if request.method == "GET":
        return render(request,"login_user.html",{"form":AuthenticationForm()})
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            message = "Wrong credentials. Try again!"
            return render(request,"login_user.html",{"form":AuthenticationForm(),"message":message})

def logout_user(request):
    logout(request)
    return redirect("home")