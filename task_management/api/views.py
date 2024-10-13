"""
case management api views containing all the api functions
The following api is stored here:
    *`view list of all clients`
    *`get_client_dropdowns_api`
"""
from datetime import datetime, timezone
import json
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count,Sum
from django.db.models import Q
from django.db.models.functions import TruncMonth,Coalesce
from rest_framework.decorators import api_view

from task_management.api.serializers import GetAllTaskSerializer, GetSingleTaskSerializer, TaskSerializer, UpdateTaskSerializer
from task_management.models import Task


@api_view(['POST'])
def create_task_api(request):
    """
    Create a new task.

    :param request:
        Django request parameter.
    :return:
        Created task or error.
    """
    if request.method == "POST":
        body = request.data
        serializer = TaskSerializer(data=body)
        
        if serializer.is_valid():
            task = Task.objects.create(
                title=serializer.validated_data.get("title"),
                description=serializer.validated_data.get("description"),
                due_date=serializer.validated_data.get("due_date"),
     
            )

            response_data = {
                "status": "success",
                "message": "Task created successfully.",
                "task": TaskSerializer(task).data,
                "task_id": task.id
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def get_all_task_api(request):
    all_tasks = Task.objects.all()
    serializer_data = GetAllTaskSerializer(all_tasks, many=True).data

    return Response(json.dumps(serializer_data), status=status.HTTP_200_OK)


@api_view(['GET'])
def get_task_by_id_api(request):
    """
    Retrieve a single task by its ID provided in the request body (if required for GET method).
    
    :param request: Django request parameter containing task_id in the request body.
    :return: JSON response with the task details or error.
    """
    if request.method == 'GET':
        try:
            body = json.loads(request.body)
            task_id = body.get('task_id')

            if not task_id:
                return Response({
                    'status': "error",
                    'message': "task_id is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get the task by ID
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                return Response({
                    'status': "error",
                    'message': "Task not found"
                }, status=status.HTTP_404_NOT_FOUND)

            # Serialize and return the task data
            single_task_serializer = GetSingleTaskSerializer(task)

            return Response(single_task_serializer.data, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response({
                'status': "error",
                'message': "Invalid JSON format"
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'status': "error",
            'message': "Invalid request method"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['PUT'])
def update_task_api(request):
    """
    Update a task by ID, with the task_id received from the request body.
    
    :param request: Django request parameter with task details in the body.
    :return: JSON response with the updated task data or error.
    """
    if request.method == 'PUT':
        # Extract task_id from the request body
        body = json.loads(request.body)
        task_id = body.get('task_id')

        # Check if task_id is provided
        if not task_id:
            return Response({"status": "error", "message": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Find the task by id
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        # Validate and update task data
        serializer = UpdateTaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Task updated successfully',
                'task': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_task_api(request):
    """
    Delete a task by ID, with the task_id received from the request body.

    :param request: Django request parameter with task_id in the body.
    :return: JSON response confirming deletion or error.
    """
    if request.method == 'DELETE':
        # Extract task_id from the request body
        body = json.loads(request.body)
        task_id = body.get('task_id')

        # Check if task_id is provided
        if not task_id:
            return Response({"status": "error", "message": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Find the task by id
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"status": "error", "message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the task
        task.delete()

        return Response({
            "status": "success",
            "message": f"Task with ID {task_id} deleted successfully"
        }, status=status.HTTP_200_OK)

    else:
        return Response({
            "status": "error",
            "message": "Invalid request method"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)