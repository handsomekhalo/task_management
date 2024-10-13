from django.shortcuts import render

# Create your views here.
def create_tasks(request):
    """User login function with api."""

    if request.method == "GET":
        return render(request, 'registration/login.html')