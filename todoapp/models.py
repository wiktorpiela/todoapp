from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    create_date = models.DateField(auto_now_add=True)
    complete_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}, {self.create_date}, {self.user}"
