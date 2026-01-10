from django.urls import path

from .views import (
    CommentDeleteView,
    CommentLikeToggle,
    CommentUpdateView,
    CreateTaskView,
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
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
    path("comment/edit/<int:pk>/", CommentUpdateView.as_view(), name="comment_update"),
    path("comment/delete/<int:pk>/", CommentDeleteView.as_view(), name="comment_delete"),
    path("comment/like/<int:pk>/", CommentLikeToggle.as_view(), name="comment-like-toggle"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
