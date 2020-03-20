from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, FormView
from django.views.generic.base import View, TemplateView

from .forms import AddTaskForm

from .models import Articles, Task, Contractor, Contract, FinancialDocument


# Create your views here.

class IndexView(TemplateView):
    template_name = 'budget/index.html'


class TasksView(ListView):
    model = Task
    template_name = 'budget/tasks.html'
    context_object_name = 'tasks'


class TaskDetailsView(DetailView):
    model = Task
    template_name = 'budget/task.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'


class AddTaskView(FormView):
    # fields = '__all__'
    # model = Task
    form_class = AddTaskForm
    template_name = 'budget/add_task.html'
    success_url = reverse_lazy('budget:tasks')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()
        return HttpResponseRedirect(self.success_url)


class EditTaskView(UpdateView):
    pass


class DeleteTaskView(DeleteView):
    pass


class ContractsView(ListView):
    pass


class ContractDetailsView(DetailView):
    pass


class AddContractView(CreateView):
    pass


class EditContractView(UpdateView):
    pass


class DeleteContractView(DeleteView):
    pass
