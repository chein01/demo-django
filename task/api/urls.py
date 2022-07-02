from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from task.api.views import TaskListView, TaskDetailView, TaskCompleteView

urlpatterns = [

    path("", TaskListView.as_view(), name="Get List Task"),
    path("<int:pk>", TaskDetailView.as_view(), name="Delete, assign Task"),
    path("complete/<int:pk>", TaskCompleteView.as_view(), name="Complete Task"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
