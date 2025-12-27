from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from .forms import CreateTaskForm, TaskFilterForm
from .mixins import UserIsOwnerMixin
from .models import Task


# Create your views here.
class CreateTaskView(LoginRequiredMixin, CreateView):
    form_class = CreateTaskForm
    template_name = "task/task_create.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form: BaseModelForm):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "task/task_list.html"

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        status = self.request.GET.get("status", "")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)
        return context


class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "task/task_detail.html"


class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs):
        task = self.get_object()
        task.status = "done"
        task.save()
        return HttpResponseRedirect((reverse_lazy("task_list")))

    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(Task, pk=task_id)


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm
    template_name = "task/task_update.html"
    success_url = reverse_lazy("task_list")


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = "task/task_delete_confirmation.html"
    success_url = reverse_lazy("task_list")
