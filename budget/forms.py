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
#TODO walidacja do zrobienia
    # def clean(self):
    #     cleaned_data = super().clean()
    #     #task = cleaned_data.get('task')
    #     article = cleaned_data.get('article')
    #     value = cleaned_data.get('value')
    #     if article is not None:
    #         #nowy plan na paragrafie< zaangażowanie na paragr
    #         article_engagement = ContractArticle.objects.filter(contract_article=article,
    #                             contract__in=Contract.objects.filter(task=self.task)).aggregate(total=Sum('value'))['total']
    #         print(article, article_engagement)
    #         if article_engagement == None:
    #             article_engagement = 0
    #         #article_engagement = article_engagement
    #         if value < article_engagement:
    #             raise forms.ValidationError(f'na paragrafie jest zaangazowanie {article_engagement} wieksze niz nowy plan')
    #     return self.cleaned_data

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
            #self.fields['contract'].queryset = Contract.objects.filter(id=contract.id)
            #self.fields['contract'].empty_label = None

    def clean(self):
        cleaned_data = super().clean()
        contract = self.initial.get('contract')
        task = contract.task
        #task = cleaned_data.get('contract').task
        article = cleaned_data.get('contract_article')
        if article is not None:
            #wartosc umowy na paragr>plan na paragrafie - zaangażowanie na paragr
            article_engagement = ContractArticle.objects.filter(contract_article=article, contract__in=Contract.objects.filter(task=task)).aggregate(total=Sum('value'))['total']
            if article_engagement == None:
                article_engagement = 0
            article_engagement = article_engagement
            amount_to_engage = TaskArticles.objects.get(task=task, article=article).value - article_engagement
            if self.cleaned_data.get('value') > amount_to_engage:
                raise forms.ValidationError(f'wartosc umowy na paragrafie wieksza niz wartosc wolnych srodkow  zadania na paragrafie, na paragrafie zostało {amount_to_engage} wolne')
        return self.cleaned_data

    class Meta:
        model = ContractArticle
        #fields = ('contract_article', 'value', 'contract')
        fields = ('contract_article', 'value')

class EditArticlesInContractForm(ModelForm):
    class Meta:
        model = ContractArticle
        fields = ('contract_article', 'value')


EditArticlesToContractFormSet = modelformset_factory(ContractArticle, fields=('contract_article', 'value'), extra=4)


class EditContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ('number', 'date', 'task', 'contractor')

    def clean(self):
        cleaned_data = super().clean()
        original_task = Task.objects.get(id=self.initial.get('task'))
        task = cleaned_data.get('task')
        if original_task != task:
            task_articles = TaskArticles.objects.filter(task=task)
            contract_articles = ContractArticle.objects.filter(contract__contractor=cleaned_data.get('contractor'))
            for article in [contract_article.contract_article for contract_article in contract_articles]:
                if article not in [task_article.article for task_article in task_articles]:
                    raise forms.ValidationError(f'paragrafy na umowie nie grają z nowym zadaniem, sprawdz czy jest plan na zadaniu')
                else:
                    task_article_engagement = ContractArticle.objects.filter(contract_article=article,
                                        contract__in=Contract.objects.filter(
                                                            task=task)).aggregate(total=Sum('value'))['total']
                    if task_article_engagement == None:
                        task_article_engagement = 0
                    #task_article_engagement = task_article_engagement
                    amount_to_engage = TaskArticles.objects.get(task=task, article=article).value - task_article_engagement
                    if ContractArticle.objects.get(contract_article=article).value > amount_to_engage:
                        raise forms.ValidationError(
                            f'wartosc umowy na paragrafie {article} nowego zadania wieksza niz wartosc wolnych srodkow  zadania na paragrafie, na paragrafie zostało {amount_to_engage} wolne')
            return self.cleaned_data

# Forms for financial documents
class AddFinancialDocForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        contract_id = self.initial.get('contract_id')
        if contract_id is not None:
            self.fields['contract'].queryset = Contract.objects.filter(id=contract_id)
            self.fields['contract'].empty_label = None
    class Meta:
        model = FinancialDocument
        fields = ('contract', 'number', 'date', 'payment_date1', 'payment_date2')

    def clean(self):
        cleaned_data = super().clean()
        ##walidacja dat
        contract_date = cleaned_data.get('contract').date
        date = cleaned_data.get('date')
        payment_date1 = cleaned_data.get('payment_date1')
        payment_date2 = cleaned_data.get('payment_date2')
        if date<contract_date:
            raise forms.ValidationError(f'Data dokumentu {date} nie moze byc wczesniejsza niz data umowy {contract_date}')
        if payment_date1<date:
            raise forms.ValidationError(f'Data platności {payment_date1} nie moze byc wczesniejsza niz data dokumentu {date}')
        if (payment_date2 and payment_date2<date):
            raise forms.ValidationError(f'Data platności {payment_date2} nie moze byc wczesniejsza niz data dokumentu {date}')
        return self.cleaned_data


class AddArticlesToFinDocForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        findoc = self.initial.get('findoc')
        if findoc is not None:
            self.fields['article'].queryset = findoc.contract.article.all()
            self.empty_permitted = True

    def clean(self):
        cleaned_data = super().clean()
        findoc = self.initial.get('findoc')
        contract = findoc.contract
        article = cleaned_data.get('article')
        if article is not None:
            #wartosc findoc na paragr!>umowa na paragrafie - inne findoc na paragr
            article_performance = FinDocumentArticle.objects.filter(article=article, fin_doc__in=FinancialDocument.objects.filter(contract=contract)).aggregate(total=Sum('value'))['total']
            if article_performance == None:
                article_performance = 0
            amount = ContractArticle.objects.get(contract=contract, contract_article=article).value - article_performance
            if self.cleaned_data.get('value') > amount:
                raise forms.ValidationError(f'wartosc findoc na paragrafie wieksza niz wartosc wolnych srodkow  umowy na paragrafie, na paragrafie zostało {amount} wolne')
        return self.cleaned_data


    class Meta:
        model = FinDocumentArticle
        fields = ('article', 'value')


AddArticlesToFinDocFormSet = modelformset_factory(FinDocumentArticle, fields=('article', 'value'), extra=6)


class EditFinDocForm(ModelForm):
    class Meta:
        model = FinancialDocument
        fields = ('contract',  'number', 'date', 'payment_date1', 'payment_date2')

    def clean(self):
        cleaned_data = super().clean()
        ##walidacja dat
        date = cleaned_data.get('date')
        payment_date1 = cleaned_data.get('payment_date1')
        payment_date2 = cleaned_data.get('payment_date2')
        if payment_date1<date:
            raise forms.ValidationError(f'Data platności {payment_date1} nie moze byc wczesniejsza niz data dokumentu {date}')
        if (payment_date2 and payment_date2<date):
            raise forms.ValidationError(f'Data platności {payment_date2} nie moze byc wczesniejsza niz data dokumentu {date}')
        #walidacja zmiany umowy czy paragrafy pasują
        original_contract = Contract.objects.get(id=self.initial.get('contract'))
        contract = cleaned_data.get('contract')
        if original_contract != contract:
            contract_articles = ContractArticle.objects.filter(contract=contract)
            findoc_articles = FinDocumentArticle.objects.filter(fin_doc = self.instance)
            for article in [findoc_article.article for findoc_article in findoc_articles]:
                if article not in [contract_article.contract_article for contract_article in contract_articles]:
                    raise forms.ValidationError(
                        f'paragrafy na dokumencie nie grają z nową umową, sprawdz paragrafy umowy')
                else:
                    contract_article_performance = FinDocumentArticle.objects.filter(article=article,
                                                fin_doc__in=FinancialDocument.objects.filter(
                                                contract=contract)).aggregate(total=Sum('value'))['total']
                    if contract_article_performance == None:
                        contract_article_performance = 0
                    amount = ContractArticle.objects.get(contract=contract, contract_article=article).value - contract_article_performance

                    if FinDocumentArticle.objects.get(article=article, fin_doc=self.instance).value > amount:
                        raise forms.ValidationError(
                            f'wartosc dokumentu na paragrafie {article} nowej umowy wieksza niz wartosc wolnych srodkow  '
                            f'umowy na paragrafie, na paragrafie zostało {amount} wolne')
        return self.cleaned_data

class EditArticlesInFinDocForm(ModelForm):
    class Meta:
        model = FinDocumentArticle
        fields = ('article', 'value')


EditArticlesToFinDocFormSet = modelformset_factory(FinDocumentArticle, fields=('article', 'value'), extra=0)
