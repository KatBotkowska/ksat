from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, FormView
from django.views.generic.base import View, TemplateView

#from .forms import AddTaskForm, EditTaskForm

from .models import Articles, Task, Contractor, Contract, FinancialDocument




# class IndexView(TemplateView): #przeniesione do  URLS PATTERNS BEZ WIDOKU TUTAJ,
#     template_name = 'budget/index.html'


# VIEWS FOR TASKS

class TasksView(ListView):
    model = Task
    template_name = 'budget/tasks.html'
    context_object_name = 'tasks'


class TaskDetailsView(DetailView):
    model = Task
    template_name = 'budget/task.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'


# class AddTaskView(FormView):
#     # fields = '__all__'
#     # model = Task
#     form_class = AddTaskForm
#     template_name = 'budget/add_task.html'
#     success_url = reverse_lazy('budget:tasks')
#
#     def form_valid(self, form):
#         task = form.save(commit=False)
#         task.save()
#         return HttpResponseRedirect(self.success_url)
#
#
# class EditTaskView(UpdateView):
#     model = Task
#     form_class = EditTaskForm
#     template_name = 'budget/edit_task.html'
#     pk_url_kwarg = 'task_id'
#     success_url = reverse_lazy('budget:task_details')
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()
#

class DeleteTaskView(DeleteView):
    model = Task
    template_name = 'budget/delete_task.html'
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('budget:tasks')


# VIEWS FOR CONTRACTS

class ContractsView(ListView):
    model = Contract
    template_name = 'budget/contracts.html'
    context_object_name = 'contracts'


class ContractDetailsView(DetailView):
    model = Contract
    template_name = 'budget/contract.html'
    pk_url_kwarg = 'contract_id'
    context_object_name = 'contract'


class AddContractView(CreateView):
    pass


class EditContractView(UpdateView):
    pass


class DeleteContractView(DeleteView):
    pass


# VIEWS FOR CONTRACTOR

class ContractorView(ListView):
    pass


class ContractorDetailsView(DetailView):
    pass


class AddContractorView(CreateView):
    pass


class EditContractorView(UpdateView):
    pass


class DeleteContractorView(DeleteView):
    pass


# VIEWS FOR FINANCIAL DOCUMENTS

class FinancialDocView(ListView):
    pass


class FinancialDocDetailsView(DetailView):
    pass


class AddFinancialDocView(CreateView):
    pass


class EditFinancialDocView(UpdateView):
    pass


class DeleteFinancialDocView(DeleteView):
    pass
