from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Task
from rest_framework.exceptions import NotFound


# Create your views here.


@api_view(["GET"])
def apiOverview(request):
    api_urls = {
        "List": "/task-list/",
        "Detail View": "/task-detail/<str:pk>/",
        "Create": "/task-create/",
        "Update": "/task-update/<str:pk>/",
        "Delete": "/task-delete/<str:pk>/",
    }
    return Response(api_urls)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def taskList(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def taskDetail(request, pk):
    try:
        task = Task.objects.get(id=pk, user=request.user)
    except Task.DoesNotExist:
        raise NotFound(detail="Task not found or not accessible by this user")

    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def taskUpdate(request, pk):
    try:
        task = Task.objects.get(id=pk, user=request.user)
    except Task.DoesNotExist:
        raise NotFound(detail="Task not found or not accessible by this user")

    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def taskCreate(request):
    data = request.data
    data["user"] = request.user.id

    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def taskDelete(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        raise NotFound(detail="Task not found")

    if task.user != request.user:
        return Response(
            {"detail": "You do not have permission to delete this task."}, status=403
        )

    task.delete()

    return Response("Task deleted successfully")
