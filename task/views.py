from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from .forms import CommentForm, CreateTaskForm, TaskFilterForm
from .mixins import UserIsAuthorMixin, UserIsOwnerMixin
from .models import Comment, Like, Task


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()  # Додаємо порожню форму коментаря в контекст
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect("task_detail", pk=comment.task.pk)
        else:
            # Випадок невалідної форми
            pass


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


class CommentUpdateView(LoginRequiredMixin, UserIsAuthorMixin, UpdateView):
    model = Comment
    fields = ["content"]
    template_name = "task/comment_update.html"

    # def form_valid(self, form):
    #     comment = self.get_object()
    #     if comment.author != self.request.user:
    #         raise PermissionDenied("Ви не можете редагувати цей коментар!")
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"pk": self.object.task.pk})


class CommentDeleteView(LoginRequiredMixin, UserIsAuthorMixin, DeleteView):
    model = Comment
    template_name = "task/comment_delete.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"pk": self.object.task.pk})


class CommentLikeToggle(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        like_qs = Like.objects.filter(comment=comment, user=request.user)
        if like_qs.exists():
            like_qs.delete()
        else:
            Like.objects.create(comment=comment, user=request.user)
        return HttpResponseRedirect(comment.get_absolute_url())


class CustomLoginView(LoginView):
    template_name = "task/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "login"


class RegisterView(CreateView):
    template_name = "task/register.html"
    form_class = UserCreationForm

    def form_valid(self, form: BaseModelForm):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("login"))
