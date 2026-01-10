from django.forms import ChoiceField, DateTimeInput, FileInput, Form, ModelForm, Select

from .models import Comment, Task


class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "desc", "status", "priority", "due_to"]
        widgets = {"due_to": DateTimeInput(attrs={"type": "datetime-local"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class TaskFilterForm(Form):
    STATUS_CHOICES = [
        ("", "Всі"),
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    status = ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=Select(attrs={"class": "form-select"}),
        label="Статус",
    )


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "media"]
        widgets = {"media": FileInput()}
