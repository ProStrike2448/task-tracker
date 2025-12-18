from django.forms import DateTimeInput, ModelForm

from .models import Task


class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "desc", "priority", "due_to", "creator"]
        widgets = {"due_to": DateTimeInput(attrs={"type": "datetime-local"})}
