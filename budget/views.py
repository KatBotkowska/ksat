from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.views.generic.base import View, TemplateView

from . models import Articles, Task, Contractor, Contract, FinancialDocument

# Create your views here.

class IndexView(TemplateView):
    template_name = 'budget/index.html'

class TasksView(ListView):
    model = Task
    template_name ='budget/tasks.html'
    context_object_name = 'tasks'

class TaskDetailsView(DetailView):
    pass

class AddTaskView(CreateView):
    pass

class DeleteTaskView(DeleteView):
    pass