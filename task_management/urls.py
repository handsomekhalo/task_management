from django.urls import path
from task_management import views



urlpatterns = [
        path('create_tasks/', views.create_tasks, name='create_tasks'),


]