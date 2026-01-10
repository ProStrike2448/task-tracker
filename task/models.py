from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["due_to", "priority"]
        verbose_name = "task"
        verbose_name_plural = "tasks"


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to="comments_media/", blank=True, null=True)

    def get_absolute_url(self):
        return self.task.get_absolute_url()


class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_comments")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "user")  # Забезпечує унікальність лайків
