from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, FormView
from django.views.generic.base import View, TemplateView

from .forms import AddTaskForm, AddArticlesToTaskForm, AddArticlesToTaskFormSet #, EditTaskForm

from .models import Articles, Task, Contractor, Contract, FinancialDocument, \
    TaskArticles, ContractArticle, FinDocumentArticle



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


class AddTaskView(FormView):
    pass
    # fields = '__all__'
    # model = Task
    form_class = AddTaskForm
    template_name = 'budget/add_task.html'
    success_url = reverse_lazy('budget:tasks')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()
        #success_url = reverse_lazy('budget:task_add_articles', task.id)
        return HttpResponseRedirect(self.success_url)

class AddArticlesToTaskView(CreateView):
    model = TaskArticles
    form_class = AddArticlesToTaskForm
    template_name = 'budget/add_articles_to_task.html'
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('budget:task_details')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['task'] = self.kwargs.get('task_id')
        ctx['formset'] = AddArticlesToTaskFormSet(queryset=Articles.objects.none())
        return ctx

    def get_initial(self):
        self.initial.update({'task_id': self.kwargs['task_id']})
        return super().get_initial()

    def post(self, request, *args, **kwargs):
        formset = AddArticlesToTaskFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.task = Task.objects.get(id = self.initial.get('task_id'))
        #articles = formset.save(commit=False)
        #articles.save()
            instance.save()
        self.success_url = reverse('budget:task_details', kwargs={'task_id': self.kwargs.get('task_id')})
        return HttpResponseRedirect(self.success_url)


class EditTaskView(UpdateView):
    pass
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
