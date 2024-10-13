from django.shortcuts import render

# Create your views here.
# Create your views here.
def login_view(request):
    """User login function with api."""

    if request.method == "GET":
        return render(request, 'index.html')
