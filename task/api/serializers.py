from rest_framework import serializers
from task.models import Task


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class TaskAssignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["user"]


class TaskDetailSerializer(TaskListSerializer):

    pass


class TaskCompleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["status"]
