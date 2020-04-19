import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.forms import formset_factory, modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, FormView
from django.views.generic.base import View, TemplateView
from ipware import get_client_ip

from .forms import AddTaskForm, AddArticlesToTaskForm, AddArticlesToTaskFormSet, EditArticlesInTaskForm, \
    EditArticlesInTaskFormSet, EditTaskForm, AddContractForm, AddArticlesToContractForm, \
    EditContractForm, EditArticlesInContractForm, EditArticlesInContractFormSet, AddFinancialDocForm, \
    AddArticlesToFinDocForm, AddArticlesToFinDocFormSet, EditFinDocForm, EditArticlesInFinDocForm, \
    EditArticlesInFinDocFormSet, UserForm

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

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        task_id = Task.objects.get(id=self.kwargs.get('task_id')).id
        response.set_cookie('task_id', task_id, max_age=30)
        return response


class AddTaskView(PermissionRequiredMixin,FormView):
    permission_required = 'budget.add_task'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to add task'
    form_class = AddTaskForm
    template_name = 'budget/add_task.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()
        self.success_url = reverse('budget:task_add_articles', kwargs={'task_id': task.pk})
        return HttpResponseRedirect(self.success_url)


# add articles to task
class AddArticlesToTaskView(PermissionRequiredMixin, FormView):
    permission_required = 'budget.add_taskarticles'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to add articles to task'
    template_name = 'budget/add_articles_to_task.html'
    pk_url_kwarg = 'task_id'
    success_url = ''

    def get_task(self):
        task_id = self.kwargs.get('task_id')
        return Task.objects.get(id=task_id)

    def get_form_class(self):
        return formset_factory(AddArticlesToTaskForm, extra=6)

    def get_success_url(self):
        return reverse('budget:task_details', kwargs={'task_id': self.kwargs.get('task_id')})

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


class EditArticlesInTaskView(PermissionRequiredMixin, UpdateView):
    permission_required = 'budget.change_taskarticles'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to edit articles to task'
    model = TaskArticles
    form_class = EditArticlesInTaskForm
    template_name = 'budget/task_edit_articles.html'
    pk_url_kwarg = 'task_id'
    success_url = ''

    def get_object(self, queryset=None):
        return self.get_task()

    def get_queryset(self):
        return TaskArticles.objects.filter(task=self.get_task())

    def get_task(self):
        task_id = self.kwargs.get('task_id')
        return Task.objects.get(id=task_id)

    def get_success_url(self):
        return reverse('budget:task_details', kwargs={'task_id': self.kwargs.get('task_id')})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = EditArticlesInTaskFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        return self.form_invalid(request, formset)

    def form_invalid(self, request, formset):
        return render(request, self.template_name, {"formset": formset})

    def form_valid(self, form):
        for single_form in form:
            instance = single_form.save(commit=False)
            instance.task = self.get_task()
            instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['task'] = self.get_task()
        ctx['formset'] = EditArticlesInTaskFormSet(queryset=TaskArticles.objects.filter(task=self.get_task()))
        return ctx


class EditTaskView(PermissionRequiredMixin, UpdateView):
    permission_required = 'budget.change_task'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to edit task'
    model = Task
    form_class = EditTaskForm
    template_name = 'budget/edit_task.html'
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('budget:task_details')

    def get_success_url(self):
        return self.object.get_absolute_url()


class DeleteTaskView(PermissionRequiredMixin, DeleteView):
    permission_required = 'budget.delete_task'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to delete task'
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

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        contract_id = Contract.objects.get(id=self.kwargs.get('contract_id')).id
        response.set_cookie('contract', contract_id, max_age=30)
        return response


class AddContractView(PermissionRequiredMixin, FormView):
    permission_required = 'budget.add_contract'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to add contract'
    form_class = AddContractForm
    template_name = 'budget/add_contract.html'
    success_url = reverse_lazy('budget:contract_add_articles')

    def form_valid(self, form):
        contract = form.save(commit=False)
        contract.save()
        self.success_url = reverse('budget:contract_add_articles', kwargs={'contract_id': contract.pk})
        return HttpResponseRedirect(self.success_url)

    def get_initial(self):
        if 'task_id' in self.request.COOKIES:
            initial = super().get_initial()
            initial['task_id'] = int(self.request.COOKIES.get('task_id'))
            return initial


class AddArticlesToContractView(PermissionRequiredMixin, FormView):
    permission_required = 'budget.add_contractarticle'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to add articles to contract'
    template_name = 'budget/add_articles_to_contract.html'
    pk_url_kwarg = 'contract_id'
    success_url = ""

    def get_contract(self):
        contract_id = self.kwargs.get('contract_id')
        return Contract.objects.get(id=contract_id)

    def get_form_class(self):
        return formset_factory(AddArticlesToContractForm, extra=0)

    def get_success_url(self):
        return reverse('budget:contract_details', kwargs={'contract_id': self.kwargs.get('contract_id')})

    def form_valid(self, form):
        for single_form in form:
            instance = single_form.save(commit=False)
            instance.contract = self.get_contract()
            instance.save()
        return super().form_valid(form)

    def get_initial(self):
        contract = self.get_contract()
        amount = contract.task.article.all().count()
        return amount * [{'contract': contract}]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['contract'] = self.get_contract()
        return ctx


class EditArticlesInContractView(PermissionRequiredMixin, UpdateView):
    permission_required = 'budget.change_contractarticle'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to edit articles in contract'
    model = ContractArticle
    form_class = EditArticlesInContractForm
    template_name = 'budget/contract_edit_articles.html'
    pk_url_kwarg = 'contract_id'
    success_url = ''

    def get_object(self, queryset=None):
        return self.get_contract()

    def get_queryset(self):
        # contract = Contract.objects.get(pk=self.kwargs.get('contract_id'))
        # articles = ContractArticle.objects.filter(contract=contract)
        # return articles
        return ContractArticle.objects.filter(contract=self.get_contract())

    def get_contract(self):
        contract_id = int(self.kwargs.get('contract_id'))
        return Contract.objects.get(pk=contract_id)

    def get_success_url(self):
        return reverse('budget:contract_details', kwargs={'contract_id': self.kwargs.get('contract_id')})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = EditArticlesInContractFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        return self.form_invalid(request, formset)

    def form_invalid(self, request, formset):
        return render(request, self.template_name, {"formset": formset})

    def form_valid(self, form):
        for single_form in form:
            instance = single_form.save(commit=False)
            instance.contract = self.get_contract()
            instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['contract'] = self.get_contract()
        ctx['formset'] = EditArticlesInContractFormSet(queryset=ContractArticle.objects.filter(contract=
                                                                                               self.get_contract()))
        return ctx


class EditContractView(PermissionRequiredMixin, UpdateView):
    permission_required = 'budget.change_contract'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to edit contract'
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

class ContractorView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('budget:login')
    model = Contractor
    template_name = 'budget/contractors.html'
    context_object_name = 'contractors'


class ContractorDetailsView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('budget:login')
    model = Contractor
    template_name = 'budget/contractor.html'
    context_object_name = 'contractor'
    pk_url_kwarg = 'contractor_id'


class AddContractorView(PermissionRequiredMixin, CreateView):
    permission_required = 'budget.add_contractor'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to add contractor'
    model = Contractor
    fields = '__all__'
    template_name = 'budget/add_contractor.html'
    success_url = reverse_lazy('budget:contractors')


class EditContractorView(PermissionRequiredMixin, UpdateView):
    permission_required = 'budget.change_contractor'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to edit contractor'
    model = Contractor
    fields = '__all__'
    pk_url_kwarg = 'contractor_id'
    template_name = 'budget/edit_contractor.html'

    # success_url = reverse_lazy('budget:contractor_details')

    def get_success_url(self):
        return self.object.get_absolute_url()


class DeleteContractorView(PermissionRequiredMixin, DeleteView):
    permission_required = 'budget.delete_contractor'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to delete contractor'
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


class AddFinancialDocView(PermissionRequiredMixin, FormView):
    permission_required = 'budget.add_financialdocument'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to add findoc'
    form_class = AddFinancialDocForm
    template_name = 'budget/add_findoc.html'
    success_url = reverse_lazy('budget:findoc_add_articles')

    def get_initial(self):
        if 'contract' in self.request.COOKIES:
            initial = super().get_initial()
            initial['contract_id'] = int(self.request.COOKIES.get('contract'))
            return initial

    def form_valid(self, form):
        findoc = form.save(commit=False)
        findoc.contractor = form.cleaned_data['contract'].contractor
        findoc.save()
        self.success_url = reverse('budget:findoc_add_articles', kwargs={'findoc_id': findoc.pk})
        return HttpResponseRedirect(self.success_url)


class AddArticlesToFinDocView(PermissionRequiredMixin, FormView):
    permission_required = 'budget.add_findocumentarticle'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to add articles to findoc'
    # model = FinDocumentArticle
    # form_class = AddArticlesToFinDocForm
    template_name = 'budget/add_articles_to_findoc.html'
    pk_url_kwarg = 'findoc_id'
    success_url = ''

    def get_findoc(self):
        findoc_id = self.kwargs.get('findoc_id')
        return FinancialDocument.objects.get(id=findoc_id)

    def get_form_class(self):
        return formset_factory(AddArticlesToFinDocForm, extra=0)

    def get_success_url(self):
        return reverse('budget:findoc_details', kwargs={'findoc_id': self.kwargs.get('findoc_id')})

    def form_valid(self, form):
        for single_form in form:
            instance = single_form.save(commit=False)
            instance.fin_doc = self.get_findoc()
            instance.save()
        return super().form_valid(form)

    def get_initial(self):
        findoc = self.get_findoc()
        amount = findoc.contract.article.all().count()
        return amount * [{'findoc': findoc}]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['findoc'] = self.get_findoc()
        return ctx


class EditFinancialDocView(PermissionRequiredMixin, UpdateView):
    permission_required = 'budget.change_financialdocument'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to edit findoc'
    model = FinancialDocument
    form_class = EditFinDocForm
    pk_url_kwarg = 'findoc_id'
    template_name = 'budget/edit_findoc.html'

    def form_valid(self, form):
        findoc = form.save(commit=False)
        findoc.contractor = form.cleaned_data['contract'].contractor
        findoc.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class EditArticlesInFinDocView(PermissionRequiredMixin, UpdateView):
    permission_required = 'budget.change_findocumentarticle'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to edit articles in findoc'
    model = FinDocumentArticle
    form_class = EditArticlesInFinDocForm
    template_name = 'budget/findoc_edit_articles.html'
    pk_url_kwarg = 'findoc_id'
    success_url = ""

    def get_object(self, queryset=None):
        return self.get_findoc()

    # def get_queryset(self):
    #     return FinDocumentArticle.objects.filter(fin_doc=self.get_findoc())

    def get_findoc(self):
        findoc_id = self.kwargs.get('findoc_id')
        return FinancialDocument.objects.get(pk=findoc_id)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['findoc'] = FinancialDocument.objects.get(pk=self.kwargs.get('findoc_id'))
        ctx['formset'] = EditArticlesInFinDocFormSet(queryset=FinDocumentArticle.objects.filter(fin_doc=
                                                                                        self.get_findoc()))
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = EditArticlesInFinDocFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        return self.form_invalid(request, formset)

    def form_valid(self, form):
        for single_form in form:
            # import pdb; pdb.set_trace()
            instance = single_form.save(commit=False)
            instance.fin_doc = self.get_findoc()
            instance.save()
        return super().form_valid(form)

    def form_invalid(self, request, formset):
        return render(request, self.template_name, {"formset": formset})

    def get_success_url(self):
        return reverse('budget:findoc_details', kwargs={'findoc_id': self.kwargs.get('findoc_id')})


class DeleteFinancialDocView(PermissionRequiredMixin, DeleteView):
    permission_required = 'budget.delete_financialdocument'
    raise_exception = False
    login_url = reverse_lazy('budget:login')
    permission_denied_message = 'You dont\'t have permission to delete findoc'
    model = FinancialDocument
    template_name = 'budget/delete_findoc.html'
    pk_url_kwarg = 'findoc_id'

    def get_success_url(self):
        findoc = FinancialDocument.objects.get(pk=self.kwargs.get('findoc_id'))
        return reverse('budget:contract-findocs', kwargs={'contract_id': findoc.contract.id})

#Views for create user, login
class UserRegistrationView(View):
    form_class = UserForm
    fields = '__all__'
    template_name = "budget/registration_form.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('budget:index')
        return render(request, self.template_name, {'form': form})

def _validate_recaptcha(token, ip):
    pass


class LoginView(LoginView):
    template_name = 'budget/login.html'

    def get_success_url(self):
        if 'next' in self.request.POST:
            return self.request.POST.get('next')
        self.success_url = reverse('budget:index')
        return self.success_url


    def get_form_valid(self, form):
        request_body = self.request.POST
        if not request_body:
            return None

        recaptcha_token = request_body['g-recaptcha-response']
        ip_addr, _ = get_client_ip(self.request)
        if not _validate_recaptcha(recaptcha_token, ip_addr):
            return redirect('budget:login')
        return super().form_valid(form)


class LogoutView(LogoutView):
    template_name = 'budget/logout.html'


class ResetPasswordView(LoginRequiredMixin, PasswordChangeView):
    login_url = '/budget:login/'
    template_name = 'budget/password_change.html'
    success_url = reverse_lazy('budget:reset_password_done')
    permission_denied_message = 'brak uprawnień do strony'

class ResetPasswordDone(PasswordChangeDoneView):
    template_name = 'budget/reset_password_done.html'