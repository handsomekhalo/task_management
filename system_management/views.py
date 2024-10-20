from django.shortcuts import render
from task_management.views import get_all_tasks


# Create your views here.
# Create your views here.
def login_view(request):
    """User login function with api."""

    if request.method == "GET":

    
        # return render(request, 'index.html')
        return get_all_tasks(request)
