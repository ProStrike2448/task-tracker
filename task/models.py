from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    title = models.CharField(max_length=256)
    desc = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    due_to = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["due_to", "priority"]
        verbose_name = "task"
        verbose_name_plural = "tasks"
