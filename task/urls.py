from django.urls import path

from .views import (
    CreateTaskView,
    TaskCompleteView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("task_create/", CreateTaskView.as_view(), name="task_create"),
    path("<int:pk>", TaskDetailView.as_view(), name="task_detail"),
    path("<int:pk>/complete", TaskCompleteView.as_view(), name="task_complete"),
    path("<int:pk>/update", TaskUpdateView.as_view(), name="task_update"),
    path("<int:pk>/delete", TaskDeleteView.as_view(), name="task_delete"),
]
