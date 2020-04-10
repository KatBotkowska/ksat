from django import forms
from django.db.models import Sum
from django.forms import ModelForm, Textarea, formset_factory, BaseFormSet
from django.forms.models import modelformset_factory
from .models import Articles, Task, Contract, Contractor, FinancialDocument, TaskArticles, ContractArticle, \
    FinDocumentArticle


# Forms for Task
class AddTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'unit', 'section')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
        }


class AddArticlesToTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        task = self.initial.get('task')
        if task is not None:
            self.fields['contract_article'].queryset = Articles.objects.get.all()

    class Meta:
        model = TaskArticles
        fields = ('article', 'value')


AddArticlesToTaskFormSet = modelformset_factory(TaskArticles, fields=('article', 'value'), extra=8)


class EditArticlesInTaskForm(ModelForm):
    class Meta:
        model = TaskArticles
        fields = ('article', 'value')


EditArticlesToTaskFormSet = modelformset_factory(TaskArticles, fields=('article', 'value'), extra=4)


class EditTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'unit', 'section')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
        }


# Forms for Contract
class AddContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ('number', 'date', 'task', 'contractor')

        # article = forms.ModelMultipleChoiceField(queryset=Articles.objects.all()) #TODO zobaczyc czy sie tak da



class AddArticlesToContractForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        contract = self.initial.get('contract')
        if contract is not None:
            self.fields['contract_article'].queryset = contract.task.article.all()
            self.fields['contract'].queryset = Contract.objects.filter(id=contract.id)
            self.fields['contract'].empty_label = None

    def clean(self):
        cleaned_data = super().clean()
        task = cleaned_data.get('contract').task
        article = cleaned_data.get('contract_article')
        if article is not None:
            #wartosc umowy na paragr>plan na paragrafie - zaangażowanie na paragr
            article_engagement = ContractArticle.objects.filter(contract_article=article, contract__in=Contract.objects.filter(task=task)).aggregate(total=Sum('value'))['total']
            if article_engagement == None:
                article_engagement = 0
            article_engagement = article_engagement
            amount_to_engage = TaskArticles.objects.get(task=task, article=article).value - article_engagement
            print(article_engagement)
            if self.cleaned_data.get('value') > amount_to_engage:
                raise forms.ValidationError(f'wartosc umowy na paragrafie wieksza niz wartosc wolnych srodkow  zadania na paragrafie, na paragrafie zostało {amount_to_engage} wolne')
        return self.cleaned_data

    class Meta:
        model = ContractArticle
        fields = ('contract_article', 'value', 'contract')


class EditArticlesInContractForm(ModelForm):
    class Meta:
        model = ContractArticle
        fields = ('contract_article', 'value')


EditArticlesToContractFormSet = modelformset_factory(ContractArticle, fields=('contract_article', 'value'), extra=0)


class EditContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ('number', 'date', 'task', 'contractor')


# Forms for financial documents
class AddFinancialDocForm(ModelForm):
    class Meta:
        model = FinancialDocument
        fields = ('contract', 'contractor', 'number', 'date', 'payment_date1', 'payment_date2')


class AddArticlesToFinDocForm(ModelForm):
    def __init__(self, *args, **kwargs):
        findoc_id = kwargs.pop('initial')['findoc_id']
        super().__init__(*args, **kwargs)
        # self.fields['contract'].queryset = Contract.objects.filter(id=contract_id) #musi być filter, a nie get

    class Meta:
        model = FinDocumentArticle
        fields = ('article', 'value')


AddArticlesToFinDocFormSet = modelformset_factory(FinDocumentArticle, fields=('article', 'value'), extra=6)


class EditFinDocForm(ModelForm):
    class Meta:
        model = FinancialDocument
        fields = ('contract', 'contractor', 'number', 'date', 'payment_date1', 'payment_date2')


class EditArticlesInFinDocForm(ModelForm):
    class Meta:
        model = FinDocumentArticle
        fields = ('article', 'value')


EditArticlesToFinDocFormSet = modelformset_factory(FinDocumentArticle, fields=('article', 'value'), extra=6)
