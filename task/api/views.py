from rest_framework import generics
from base.api.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework import generics
from task.api.serializers import TaskCreateSerializer, TaskListSerializer, TaskAssignSerializer, TaskCompleteSerializer
from task.models import Task
from base.permissions import ClientAuthOnlyCreate, ManagerAuthDeleteAssign, EmployeeAuthDeleteComplete
from task.choices import COMPLETE


class TaskListView(ListModelMixin, CreateModelMixin, generics.ListCreateAPIView):

    permission_classes = (ClientAuthOnlyCreate,)
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer

    def get_serializer_class(self):
        return TaskCreateSerializer if self.request.method == "POST" else TaskListSerializer


class TaskDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (ManagerAuthDeleteAssign,)
    queryset = Task.objects.all()

    def get_serializer_class(self):
        return TaskAssignSerializer if self.request.method == "PUT" else TaskListSerializer


class TaskCompleteView(RetrieveModelMixin, UpdateModelMixin, generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (EmployeeAuthDeleteComplete,)
    queryset = Task.objects.all()
    serializer_class = TaskCompleteSerializer

    def get_credentials(self, request):
        return {"status": COMPLETE}
