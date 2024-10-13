from django.urls import path
from task_management import views



urlpatterns = [
        path('create_task/',views.create_task,name='create_task'),
        path('get_all_tasks/',views.get_all_tasks,name='get_all_tasks'),
]