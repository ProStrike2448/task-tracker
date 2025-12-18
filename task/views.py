from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CreateTaskForm
from .models import Task


# Create your views here.
class CreateTaskView(CreateView):
    form_class = CreateTaskForm
    template_name = "task/task_create.html"
    success_url = reverse_lazy("task_list")


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "task/task_list.html"


class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "task/task_detail.html"
