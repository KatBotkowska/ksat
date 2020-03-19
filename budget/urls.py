from  django.urls import path
from . import views

app_name = 'budget'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('task/<int:task_id>', views.TaskDetailsView.as_view(), name='task_details'),
    path('task_add/', views.AddTaskView.as_view(), name='add_task'),
]