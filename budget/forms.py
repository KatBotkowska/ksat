from django import forms
from django.forms import ModelForm, Textarea, formset_factory
from django.forms.models import modelformset_factory
from .models import Articles, Task, Contract, Contractor, FinancialDocument, TaskArticles, ContractArticle, \
    FinDocumentArticle


#Forms for Task
class AddTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'unit', 'section')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
        }
        # article = forms.ModelMultipleChoiceField(queryset=Articles.objects.all()) #TODO zobaczyc czy sie tak da
        # help_texts = articles_fields


class AddArticlesToTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        task_id = kwargs.pop('initial')['task_id']
        super().__init__(*args, **kwargs)
        # self.fields['task'].queryset = Task.objects.filter(id=task_id) #musi być filter, a nie get

    class Meta:
        model = TaskArticles
        fields = ('article', 'value')


AddArticlesToTaskFormSet = modelformset_factory(TaskArticles, fields=('article', 'value'), extra=8)


class EditArticlesInTaskForm(ModelForm):
    class Meta:
        model = TaskArticles
        fields = ('article', 'value')


EditArticlesToTaskFormSet = modelformset_factory(TaskArticles, fields=('article', 'value'), extra=8)


class EditTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'unit', 'section')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
        }


#Forms for Contract
class AddContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ('number', 'date', 'task', 'contractor')


        # article = forms.ModelMultipleChoiceField(queryset=Articles.objects.all()) #TODO zobaczyc czy sie tak da

class AddArticlesToContractForm(ModelForm):
    def __init__(self, *args, **kwargs):
        contract_id = kwargs.pop('initial')['contract_id']
        super().__init__(*args, **kwargs)
        # self.fields['contract'].queryset = Contract.objects.filter(id=contract_id) #musi być filter, a nie get

    class Meta:
        model = ContractArticle
        fields = ('contract_article', 'value')

AddArticlesToContractFormSet = modelformset_factory(ContractArticle, fields=('contract_article', 'value'), extra=6)


class EditArticlesInContractForm(ModelForm):
    class Meta:
        model = ContractArticle
        fields = ('contract_article', 'value')


EditArticlesToContractFormSet = modelformset_factory(ContractArticle, fields=('contract_article', 'value'), extra=6)


class EditContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ('number', 'date', 'task', 'contractor')
