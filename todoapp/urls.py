from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/", views.tasks, name="tasks"),
    path("create-task/", views.create_task, name="create_task"),
    path("tasks/<int:taskID>", views.task_details, name="task_details"),
    path("tasks/<int:taskID>/complete", views.complete_task, name="complete_task"),
    path("tasks/<int:taskID>/delete", views.delete_task, name="delete_task"),

    #auth
    path("register/", views.register, name="register"),
    path("log/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
]
