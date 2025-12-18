from django.urls import path

from .views import CreateTaskView, TaskDetailView, TaskListView

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("task_create/", CreateTaskView.as_view(), name="task_create"),
    path("<int:pk>", TaskDetailView.as_view(), name="task_detail"),
]
