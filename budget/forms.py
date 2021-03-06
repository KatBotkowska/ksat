from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Sum
from django.forms import ModelForm, Textarea, formset_factory, BaseFormSet
from django.forms.models import modelformset_factory, BaseModelFormSet

from Ksat import settings
from .models import Articles, Task, Contract, Contractor, FinancialDocument, TaskArticles, ContractArticle, \
    FinDocumentArticle, User


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

    def clean(self):
        super().clean()
        data = self.cleaned_data
        article = self.cleaned_data.get('article')
        value = self.cleaned_data.get('value')
        if article is not None:
            # nowy plan na paragrafie< zaangażowanie na paragr
            article_engagement = ContractArticle.objects.filter(contract_article=article,
                                                                contract__in=Contract.objects.filter(
                                                                    task=self.instance.task)).aggregate(
                total=Sum('value'))['total']
            # print('zaangażowanie', article, article_engagement, 'nowa wartosc', value)
            if article_engagement == None:
                article_engagement = 0
            # article_engagement = article_engagement
            if value < article_engagement:
                print('uwaga', article_engagement, value, article)
                raise forms.ValidationError(
                    f'na paragrafie jest zaangazowanie {article_engagement} wieksze niz nowy plan')
            return self.cleaned_data

    class Meta:
        model = TaskArticles
        fields = ('article', 'value')


EditArticlesInTaskFormSet = modelformset_factory(TaskArticles, fields=('article', 'value'),
                                                 extra=0, form=EditArticlesInTaskForm)


class EditTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'unit', 'section')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
        }


# Forms for Contract
class AddContractForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        task_id = self.initial.get('task_id')
        if task_id is not None:
            self.fields['task'].queryset = Task.objects.filter(id=task_id)
            self.fields['task'].empty_label = None

    class Meta:
        model = Contract
        fields = ('number', 'date', 'task', 'contractor')


class AddArticlesToContractForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        contract = self.initial.get('contract')
        if contract is not None:
            self.fields['contract_article'].queryset = contract.task.article.all()
            # self.fields['contract'].queryset = Contract.objects.filter(id=contract.id)
            # self.fields['contract'].empty_label = None

    def clean(self):
        cleaned_data = super().clean()
        contract = self.initial.get('contract')
        task = contract.task
        # task = cleaned_data.get('contract').task
        article = cleaned_data.get('contract_article')
        if article is not None:
            # wartosc umowy na paragr>plan na paragrafie - zaangażowanie na paragr
            article_engagement = ContractArticle.objects.filter(contract_article=article,
                                                                contract__in=Contract.objects.filter(
                                                                    task=task)).aggregate(total=Sum('value'))['total']
            if article_engagement == None:
                article_engagement = 0
            article_engagement = article_engagement
            amount_to_engage = TaskArticles.objects.get(task=task, article=article).value - article_engagement
            if self.cleaned_data.get('value') > amount_to_engage:
                raise forms.ValidationError(
                    f'wartosc umowy na paragrafie wieksza niz wartosc wolnych srodkow  zadania na paragrafie, na paragrafie zostało {amount_to_engage} wolne')
        return self.cleaned_data

    class Meta:
        model = ContractArticle
        # fields = ('contract_article', 'value', 'contract')
        fields = ('contract_article', 'value')


class EditArticlesInContractForm(ModelForm):

    def clean(self):
        super().clean()
        data = self.cleaned_data
        article = self.cleaned_data.get('contract_article')
        value = self.cleaned_data.get('value')
        if article is not None:
            # nowy plan na paragrafie umowy!< wykonanie na paragr
            article_performance = FinDocumentArticle.objects.filter(article=article,
                                                                    fin_doc__in=FinancialDocument.objects.filter(
                                                                        contract=self.instance.contract)).aggregate(
                total=Sum('value'))['total']
            # print('zaangażowanie', article, article_engagement, 'nowa wartosc', value)
            if article_performance == None:
                article_performance = 0
            # article_engagement = article_engagement
            if value < article_performance:
                print('uwaga', article_performance, value, article)
                raise forms.ValidationError(
                    f'na paragrafie jest wykonanie {article_performance} wieksze niz nowa wartosc paragr {value}')
            # nowy plan na paragrafie !>plan na zadaniu -zaangażowanie dotychczasowe
            article_engagement = ContractArticle.objects.filter(contract_article=article).exclude(contract=
                                                                                                  self.instance.contract).aggregate(
                total=Sum('value'))['total']
            article_plan = TaskArticles.objects.filter(task=self.instance.contract.task,
                                                       article=article).aggregate(total=Sum('value'))['total']
            if article_plan == None:
                article_plan = 0
            if value > article_plan - article_performance:
                raise forms.ValidationError(f'na paragrafie zadania wolne środki {article_plan - article_performance}'
                                            f'mniejsze niż nowa wartośc umowy  na paragrafie: {value}')
            return self.cleaned_data

    class Meta:
        model = ContractArticle
        fields = ('contract_article', 'value')


EditArticlesInContractFormSet = modelformset_factory(ContractArticle, fields=('contract_article', 'value'),
                                                     form=EditArticlesInContractForm, extra=0)


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
                    raise forms.ValidationError(
                        f'paragrafy na umowie nie grają z nowym zadaniem, sprawdz czy jest plan na zadaniu')
                else:
                    task_article_engagement = ContractArticle.objects.filter(contract_article=article,
                                                                             contract__in=Contract.objects.filter(
                                                                                 task=task)).aggregate(
                        total=Sum('value'))['total']
                    if task_article_engagement == None:
                        task_article_engagement = 0
                    # task_article_engagement = task_article_engagement
                    amount_to_engage = TaskArticles.objects.get(task=task,
                                                                article=article).value - task_article_engagement
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
        if date < contract_date:
            raise forms.ValidationError(
                f'Data dokumentu {date} nie moze byc wczesniejsza niz data umowy {contract_date}')
        if payment_date1 < date:
            raise forms.ValidationError(
                f'Data platności {payment_date1} nie moze byc wczesniejsza niz data dokumentu {date}')
        if (payment_date2 and payment_date2 < date):
            raise forms.ValidationError(
                f'Data platności {payment_date2} nie moze byc wczesniejsza niz data dokumentu {date}')
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
            # wartosc findoc na paragr!>umowa na paragrafie - inne findoc na paragr
            article_performance = FinDocumentArticle.objects.filter(article=article,
                                                                    fin_doc__in=FinancialDocument.objects.filter(
                                                                        contract=contract)).aggregate(
                total=Sum('value'))['total']
            if article_performance == None:
                article_performance = 0
            amount = ContractArticle.objects.get(contract=contract,
                                                 contract_article=article).value - article_performance
            if self.cleaned_data.get('value') > amount:
                raise forms.ValidationError(
                    f'wartosc findoc na paragrafie wieksza niz wartosc wolnych srodkow  umowy na paragrafie, na paragrafie zostało {amount} wolne')
        return self.cleaned_data

    class Meta:
        model = FinDocumentArticle
        fields = ('article', 'value')


AddArticlesToFinDocFormSet = modelformset_factory(FinDocumentArticle, fields=('article', 'value'), extra=6)


class EditFinDocForm(ModelForm):
    class Meta:
        model = FinancialDocument
        fields = ('contract', 'number', 'date', 'payment_date1', 'payment_date2')

    def clean(self):
        cleaned_data = super().clean()
        ##walidacja dat
        date = cleaned_data.get('date')
        payment_date1 = cleaned_data.get('payment_date1')
        payment_date2 = cleaned_data.get('payment_date2')
        if payment_date1 < date:
            raise forms.ValidationError(
                f'Data platności {payment_date1} nie moze byc wczesniejsza niz data dokumentu {date}')
        if (payment_date2 and payment_date2 < date):
            raise forms.ValidationError(
                f'Data platności {payment_date2} nie moze byc wczesniejsza niz data dokumentu {date}')
        # walidacja zmiany umowy czy paragrafy pasują
        original_contract = Contract.objects.get(id=self.initial.get('contract'))
        contract = cleaned_data.get('contract')
        if original_contract != contract:
            contract_articles = ContractArticle.objects.filter(contract=contract)
            findoc_articles = FinDocumentArticle.objects.filter(fin_doc=self.instance)
            for article in [findoc_article.article for findoc_article in findoc_articles]:
                if article not in [contract_article.contract_article for contract_article in contract_articles]:
                    raise forms.ValidationError(
                        f'paragrafy na dokumencie nie grają z nową umową, sprawdz paragrafy umowy')
                else:
                    contract_article_performance = FinDocumentArticle.objects.filter(article=article,
                                                                                     fin_doc__in=FinancialDocument.objects.filter(
                                                                                         contract=contract)).aggregate(
                        total=Sum('value'))['total']
                    if contract_article_performance == None:
                        contract_article_performance = 0
                    amount = ContractArticle.objects.get(contract=contract,
                                                         contract_article=article).value - contract_article_performance

                    if FinDocumentArticle.objects.get(article=article, fin_doc=self.instance).value > amount:
                        raise forms.ValidationError(
                            f'wartosc dokumentu na paragrafie {article} nowej umowy wieksza niz wartosc wolnych srodkow  '
                            f'umowy na paragrafie, na paragrafie zostało {amount} wolne')
        return self.cleaned_data


class EditArticlesInFinDocForm(ModelForm):
    def clean(self):
        super().clean()
        data = self.cleaned_data
        article = self.cleaned_data.get('article')
        value = self.cleaned_data.get('value')
        if article is not None:
            # nowa wart findoc na par !> wart umowy na paragr-wykonanie na par
            article_performance = FinDocumentArticle.objects.filter(article=article,
                                                                    fin_doc__contract=self.instance.fin_doc.contract).exclude(
                fin_doc=self.instance.fin_doc).aggregate(total=Sum('value'))['total']
            article_contract = ContractArticle.objects.get(contract_article=article,
                                                           contract=self.instance.fin_doc.contract).value
            if article_performance == None:
                article_performance = 0

            if value > article_contract - article_performance:
                raise forms.ValidationError(
                    f'na paragrafie  umowy brak środków: wykonanie {article_performance} powiekszona o nową wartość {value} wieksze niz plan umowy {article_contract}')
            return self.cleaned_data

    class Meta:
        model = FinDocumentArticle
        fields = ('article', 'value')


EditArticlesInFinDocFormSet = modelformset_factory(FinDocumentArticle, fields=('article', 'value'),
                                                   extra=0, form=EditArticlesInFinDocForm)


#class for Users
class UserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    phone_number=forms.SlugField()
    name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    captcha = ReCaptchaField(
        public_key=settings.RECAPTCHA_SITE_KEY,
        private_key=settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        widget= ReCaptchaV2Checkbox(
            api_params={
                'hl': 'pl',
            }
        ),
        error_messages={
            'required': 'Attention please, chaptcha!!'
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'name', 'last_name', 'phone_number']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data['phone_number']
        user.name = self.cleaned_data["name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('Username already exists')

