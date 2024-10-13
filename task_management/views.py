from audioop import reverse
import json
from django.http import JsonResponse
from django.shortcuts import render
import requests
from django.urls import reverse_lazy
from system_management.general_func_classes import api_connection, host_url



def get_data_on_success(response_data):
    status = response_data.get('status')
    if status == 'success':
        data = response_data.get('data')
    else:
        data = []
    return data

# Create your views here.
def create_task(request):
    """Create task functiona;ity."""

    if request.method == 'POST':
        token = request.session.get('token')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Token {token}"
        }

        payload = json.dumps({
            'title': title,
            'description': description,
            'due_date': due_date,
        })

        url = f"{host_url(request)}{reverse_lazy('create_task_api')}"

        response_data = requests.post(url, headers=headers, data=payload, timeout=10)

        if response_data.status_code == 201:  # Check for Created status
            return JsonResponse({'status': 'success', 'data': response_data.json()})  # Send back the task data if needed
        else:
            return JsonResponse({'error': 'Error creating task', 'details': response_data.json()}, status=400)

def get_all_tasks(request):
    """User login function with api."""

    if request.method == "GET":

        token = request.session.get('token')

        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Token {token}"
        }

        url = f"{host_url(request)}{reverse_lazy('get_all_task_api')}"  # Replace with the correct URL


        all_tasks_response = api_connection(method="GET", url=url, headers=headers, data={})
        all_tasks = get_data_on_success(all_tasks_response)

        context = {
            'all_tasks': all_tasks,
        }
        
        return render(request, 'index.html', context)