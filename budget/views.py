from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, FormView
from django.views.generic.base import View, TemplateView

from .forms import AddTaskForm, AddArticlesToTaskForm, AddArticlesToTaskFormSet, EditArticlesInTaskForm, \
    EditArticlesToTaskFormSet, EditTaskForm, AddContractForm, AddArticlesToContractForm, \
    EditContractForm, EditArticlesInContractForm, EditArticlesToContractFormSet, AddFinancialDocForm, \
    AddArticlesToFinDocForm, AddArticlesToFinDocFormSet, EditFinDocForm, EditArticlesInFinDocForm, \
    EditArticlesToFinDocFormSet

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
    form_class = AddTaskForm
    template_name = 'budget/add_task.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()
        self.success_url = reverse('budget:task_add_articles', kwargs={'task_id': task.pk})
        return HttpResponseRedirect(self.success_url)


# add articles to task
class AddArticlesToTaskView(FormView):
    template_name = 'budget/add_articles_to_task.html'
    pk_url_kwarg = 'task_id'
    success_url = ''

    def get_task(self):
        task_id = self.kwargs.get('task_id')
        return Task.objects.get(id=task_id)

    def get_form_class(self):
        return formset_factory(AddArticlesToTaskForm, extra = 6)

    def get_success_url(self):
        return reverse('budget:task_details', kwargs= {'task_id': self.kwargs.get('task_id')})

    def form_valid(self, form):
        for single_form in form:
            instance = single_form.save(commit=False)
            instance.task = self.get_task()
            instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['task'] = self.get_task()
        return ctx


class EditArticlesInTaskView(UpdateView):
    model = TaskArticles
    # form_class = EditArticlesInTaskForm
    template_name = 'budget/task_edit_articles.html'
    pk_url_kwarg = 'task_id'
    success_url = ''

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['task'] = Task.objects.get(pk=self.kwargs.get('task_id'))
        ctx['form'] = EditArticlesToTaskFormSet(queryset=
                                            TaskArticles.objects.filter(task=Task.objects.get(pk=self.kwargs.get('task_id'))))
        return ctx

    # def get_initial(self):
    #     self.initial.update({'task_id': self.kwargs['task_id']})
    #     return super().get_initial()

    # def post(self, request, *args, **kwargs):
    #     formset = EditArticlesToTaskFormSet(request.POST)
    #     if formset.is_valid():
    #         return self.form_valid(formset)
    def get_task(self):
        task_id = self.kwargs.get('task_id')
        return Task.objects.get(id=task_id)

    def get_form_class(self):
        EditArticlesToTaskFormSet =formset_factory(EditArticlesInTaskForm, extra = 6)
        return EditArticlesToTaskFormSet

    def get_success_url(self):
        return reverse('budget:task_details', kwargs= {'task_id': self.kwargs.get('task_id')})

    def form_valid(self, form):
        for single_form in form:
            instance = single_form.save(commit=False)
            instance.task = self.get_task()
            instance.save()
        return super().form_valid(form)


class EditTaskView(UpdateView):
    model = Task
    form_class = EditTaskForm
    template_name = 'budget/edit_task.html'
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('budget:task_details')

    def get_success_url(self):
        return self.object.get_absolute_url()


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


class AddContractView(FormView):
    form_class = AddContractForm
    template_name = 'budget/add_contract.html'
    success_url = reverse_lazy('budget:contract_add_articles')

    def form_valid(self, form):
        contract = form.save(commit=False)
        contract.save()
        self.success_url = reverse('budget:contract_add_articles', kwargs={'contract_id': contract.pk})
        return HttpResponseRedirect(self.success_url)


class AddArticlesToContractView(FormView):

    template_name = 'budget/add_articles_to_contract.html'
    pk_url_kwarg = 'contract_id'
    success_url = ""

    def get_contract(self):
        id = self.kwargs.get('contract_id')
        return Contract.objects.get(id=id)

    def get_form_class(self):
        contract = self.get_contract()
        #amount = contract.task.article.all().count()
        return formset_factory(AddArticlesToContractForm, extra=0)

    def get_success_url(self):
        return reverse('budget:contract_details', kwargs={'contract_id': self.kwargs.get('contract_id')})

    def form_valid(self, form):
        for item in form:
            ca = item.save(commit=False)
            ca.save()
        return super().form_valid(form)

    def get_initial(self):
        contract = self.get_contract()
        amount = contract.task.article.all().count()
        return amount*[{'contract': contract}]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['contract'] = self.get_contract()
        return ctx

class EditArticlesInContractView(UpdateView):
    model = ContractArticle
    form_class = EditArticlesInContractForm
    template_name = 'budget/contract_edit_articles.html'
    pk_url_kwarg = 'contract_id'

    # def get_queryset(self):
    #     contract = Contract.objects.get(id=self.kwargs.get('contract_id'))
    #     #import pdb; pdb.set_trace()
    #     return ContractArticle.objects.filter(contract=contract)
    # # success_url = reverse_lazy('budget:contract_details')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ctx['task_id'] = self.kwargs.get('task_id')
        contract = Contract.objects.get(pk=self.kwargs.get('contract_id'))
        ctx['contract'] = contract
        ctx['formset'] = EditArticlesToContractFormSet(initial={'contract': contract})
        return ctx

    # def get_initial(self):
    #     self.initial.update({'contract_id': self.kwargs['contract_id']})
    #     return super().get_initial()

    def post(self, request, *args, **kwargs):
        formset = EditArticlesToContractFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            # import pdb; pdb.set_trace()
            instance.contract = Contract.objects.get(pk=self.kwargs.get('contract_id'))
            instance.save()
        self.success_url = reverse('budget:contract_details', kwargs={'contract_id': self.kwargs.get('contract_id')})
        return HttpResponseRedirect(self.success_url)


class EditContractView(UpdateView):
    model = Contract
    form_class = EditContractForm
    template_name = 'budget/edit_contract.html'
    pk_url_kwarg = 'contract_id'

    def get_success_url(self):
        return self.object.get_absolute_url()


class DeleteContractView(DeleteView):
    model = Contract
    template_name = 'budget/delete_contract.html'
    pk_url_kwarg = 'contract_id'
    success_url = reverse_lazy('budget:contracts')


# VIEWS FOR CONTRACTOR

class ContractorView(ListView):
    model = Contractor
    template_name = 'budget/contractors.html'
    context_object_name = 'contractors'


class ContractorDetailsView(DetailView):
    model = Contractor
    template_name = 'budget/contractor.html'
    context_object_name = 'contractor'
    pk_url_kwarg = 'contractor_id'


class AddContractorView(CreateView):
    model = Contractor
    fields = '__all__'
    template_name = 'budget/add_contractor.html'
    success_url = reverse_lazy('budget:contractors')


class EditContractorView(UpdateView):
    model = Contractor
    fields = '__all__'
    pk_url_kwarg = 'contractor_id'
    template_name = 'budget/edit_contractor.html'

    # success_url = reverse_lazy('budget:contractor_details')

    def get_success_url(self):
        return self.object.get_absolute_url()


class DeleteContractorView(DeleteView):
    model = Contractor
    template_name = 'budget/delete_contractor.html'
    pk_url_kwarg = 'contractor_id'
    success_url = reverse_lazy('budget:contractors')


# VIEWS FOR FINANCIAL DOCUMENTS

class FinancialDocContractorView(ListView):
    model = FinancialDocument
    template_name = 'budget/contractor_findocs.html'
    context_object_name = 'findocs'

    def get_queryset(self):
        contractor = Contractor.objects.get(pk=self.kwargs.get('contractor_id'))
        fin_docs = FinancialDocument.objects.filter(contractor=contractor).order_by('contract', 'contract__task')
        return fin_docs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['contractor'] = Contractor.objects.get(pk=self.kwargs.get('contractor_id'))
        return ctx


class FinancialDocContractView(ListView):
    model = FinancialDocument
    template_name = 'budget/contract_findocs.html'
    context_object_name = 'findocs'

    def get_queryset(self):
        contract = Contract.objects.get(pk=self.kwargs.get('contract_id'))
        fin_docs = FinancialDocument.objects.filter(contract=contract).order_by('contractor', 'contract__task')
        return fin_docs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['contract'] = Contract.objects.get(pk=self.kwargs.get('contract_id'))
        return ctx


class FinancialDocTaskView(ListView):
    model = FinancialDocument
    template_name = 'budget/task_findocs.html'
    context_object_name = 'findocs'

    def get_queryset(self):
        task = Task.objects.get(pk=self.kwargs.get('task_id'))
        contracts = Contract.objects.filter(task=task)
        fin_docs = FinancialDocument.objects.filter(contract__task=task).order_by('contract')
        return fin_docs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['task'] = Task.objects.get(pk=self.kwargs.get('task_id'))
        return ctx


class FinancialDocDetailsView(DetailView):
    model = FinancialDocument
    template_name = 'budget/findoc.html'
    context_object_name = 'findoc'
    pk_url_kwarg = 'findoc_id'


class AddFinancialDocView(FormView):
    form_class = AddFinancialDocForm
    template_name = 'budget/add_findoc.html'
    success_url = reverse_lazy('budget:findoc_add_articles')

    def form_valid(self, form):
        findoc = form.save(commit=False)
        findoc.save()
        self.success_url = reverse('budget:findoc_add_articles', kwargs={'findoc_id': findoc.pk})
        return HttpResponseRedirect(self.success_url)


class AddArticlesToFinDocView(CreateView):
    model = FinDocumentArticle
    form_class = AddArticlesToFinDocForm
    template_name = 'budget/add_articles_to_findoc.html'
    pk_url_kwarg = 'findoc_id'
    success_url = reverse_lazy('budget:findoc_details')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ctx['task_id'] = self.kwargs.get('task_id')
        ctx['formset'] = AddArticlesToFinDocFormSet(queryset=FinancialDocument.objects.none())
        ctx['findoc'] = FinancialDocument.objects.get(pk=self.kwargs.get('findoc_id'))
        return ctx

    def get_initial(self):
        self.initial.update({'findoc_id': self.kwargs['findoc_id']})
        return super().get_initial()

    def post(self, request, *args, **kwargs):
        formset = AddArticlesToFinDocFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.fin_doc = FinancialDocument.objects.get(id=self.initial.get('findoc_id'))  #####instance>???
            instance.save()
        self.success_url = reverse('budget:findoc_details', kwargs={'findoc_id': self.kwargs.get('findoc_id')})
        # import pdb;
        # pdb.set_trace()
        return HttpResponseRedirect(self.success_url)


class EditFinancialDocView(UpdateView):
    model = FinancialDocument
    form_class = EditFinDocForm
    pk_url_kwarg = 'findoc_id'
    template_name = 'budget/edit_findoc.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class EditArticlesInFinDocView(FormView):
    model = FinDocumentArticle
    form_class = EditArticlesInFinDocForm
    template_name = 'budget/findoc_edit_articles.html'
    pk_url_kwarg = 'findoc_id'
    success_url = reverse_lazy('budget:findoc_details')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['findoc'] = FinancialDocument.objects.get(pk=self.kwargs.get('findoc_id'))
        ctx['formset'] = EditArticlesToFinDocFormSet(queryset=FinDocumentArticle.objects.filter(fin_doc=ctx['findoc']))
        return ctx

    def get_initial(self):
        self.initial.update({'findoc_id': self.kwargs['findoc_id']})
        return super().get_initial()

    def post(self, request, *args, **kwargs):
        formset = EditArticlesToFinDocFormSet(request.POST)
        for form in formset:
            if form.is_valid():
                form.save()

    def form_valid(self, formset):
        instances = formset.save(commit=False)
        for instance in instances:
            # import pdb; pdb.set_trace()
            instance.fin_doc = FinancialDocument.objects.get(pk=self.kwargs.get('findoc_id'))
            instance.save()
        self.success_url = reverse('budget:findoc_details', kwargs={'findoc_id': self.kwargs.get('findoc_id')})
        return HttpResponseRedirect(self.success_url)


class DeleteFinancialDocView(DeleteView):
    model = FinancialDocument
    template_name = 'budget/delete_findoc.html'
    pk_url_kwarg = 'findoc_id'

    def get_success_url(self):
        findoc = FinancialDocument.objects.get(pk=self.kwargs.get('findoc_id'))
        return reverse('budget:contract-findocs', kwargs={'contract_id': findoc.contract.id})
