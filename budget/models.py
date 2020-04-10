from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    pass


class Articles(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=126)
    financement_choices = [
        (0, 'BWD'),
        (8, 'DOT'),
        (9, 'BWD-WKLAD WLASNY')
    ]
    financement = models.IntegerField(choices=financement_choices)

    class Meta:
        verbose_name = 'article'

    def total_number(self):
        return f'{str(self.number) + str(self.financement)}'

    def __str__(self):
        return f'{self.total_number()}, {self.name}'


class Task(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=256)
    unit = models.SmallIntegerField()
    section = models.SmallIntegerField()
    article = models.ManyToManyField(Articles, through='TaskArticles')

    def __str__(self):
        return f'Title {self.title}, unit {self.unit}, section {self.section}'

    def get_absolute_url(self):
        return reverse('budget:task_details', kwargs={'task_id': self.pk})

    def task_value(self):
        value = TaskArticles.objects.filter(task=self).aggregate(total=Sum('value'))['total']
        if value:
            return round(value, 2)
        return 0

    def engagement(self):
        contracts = Contract.objects.filter(task=self)
        engagement = 0
        for contract in contracts:
            engagement += contract.contract_value()
        return round(engagement, 2)

    def performance(self):
        contracts = Contract.objects.filter(task=self)
        performance = 0
        for contract in contracts:
            performance += contract.contract_performance()
        return round(performance, 2)


class Meta:
    default_related_name = 'task'
    ordering = ('title',)
    verbose_name = 'task'


class TaskArticles(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=0, default=0, max_digits=11)

    class Meta:
        default_related_name = 'task_articles'
        ordering = ('task',)
        verbose_name = 'task articles'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.article_id is not None:
            super().save(force_insert, force_update, using, update_fields)


class Contractor(models.Model):
    name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    num = models.SmallIntegerField(blank=True)

    def get_absolute_url(self):
        return reverse('budget:contractor_details', kwargs={'contractor_id': self.pk})

    def __str__(self):
        return f'{self.name} {self.last_name}'

    def contracts(self):
        return Contract.objects.filter(contractor=self)

    def contracts_value(self):
        contracts_value = 0
        for contract in Contract.objects.filter(contractor=self):
            contracts_value += contract.contract_value()
        return round(contracts_value, 2)

    def contracts_performance(self):
        contracts_performance = 0
        for contract in Contract.objects.filter(contractor=self):
            contracts_performance += contract.contract_performance()
        return round(contracts_performance, 2)

    class Meta:
        default_related_name = 'contractors'
        ordering = ('last_name',)
        verbose_name = 'contractor'


class Contract(models.Model):
    number = models.CharField(max_length=128)
    date = models.DateField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='contracts', related_query_name='contract')
    contractor = models.ForeignKey(Contractor, default=None, on_delete=models.CASCADE, related_name='contracts',
                                   related_query_name='contract')
    article = models.ManyToManyField(Articles, through='ContractArticle')

    def __str__(self):
        return f'N: {self.number}, date {self.date}, contractor {self.contractor}'

    def get_absolute_url(self):
        return reverse('budget:contract_details', kwargs={'contract_id': self.pk})

    def contract_value(self):
        value = ContractArticle.objects.filter(contract=self).aggregate(total=Sum('value'))['total']
        if value:
            return round(value, 2)
        return 0

    def contract_performance(self):
        fin_docs = FinancialDocument.objects.filter(contract=self)
        performance = 0
        for fin_doc in fin_docs:
            # import pdb; pdb.set_trace()
            performance += fin_doc.fin_doc_value()
        return round(performance, 2)

    class Meta:
        default_related_name = 'contract'
        ordering = ('number', 'contractor')
        verbose_name = 'contract'


class ContractArticle(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    contract_article = models.ForeignKey(Articles, on_delete=models.CASCADE, blank=True )
    value = models.DecimalField(decimal_places=2, max_digits=11, default=0)

    class Meta:
        default_related_name = 'contract_articles'
        ordering = ('contract',)
        verbose_name = 'contract articles'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.contract_article_id is not None:
            super().save(force_insert, force_update, using, update_fields)


class FinancialDocument(models.Model):
    # task = models.ForeignKey(Task, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='fds', related_query_name='fd')
    contractor = models.ForeignKey(Contractor, default=None, on_delete=models.CASCADE, related_name='fds',
                                   related_query_name='fd')
    number = models.CharField(max_length=64, default=None)
    date = models.DateField()
    payment_date1 = models.DateField(blank=True, null=True)
    payment_date2 = models.DateField(blank=True, null=True)
    article = models.ManyToManyField(Articles, through='FinDocumentArticle')

    def get_absolute_url(self):
        return reverse('budget:findoc_details', kwargs={'findoc_id': self.pk})

    def fin_doc_value(self):
        value = FinDocumentArticle.objects.filter(fin_doc=self).aggregate(total=Sum('value'))['total']
        if value:
            return round(value, 2)
        return 0

    def __str__(self):
        return f'{self.number} from {self.date}'

    class Meta:
        default_related_name = 'fds'
        verbose_name = 'finacial_doc'


class FinDocumentArticle(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    fin_doc = models.ForeignKey(FinancialDocument, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=11, default=0)

    def fin_doc_value(self, fin_doc):
        return self.objects.filter(fin_doc=fin_doc).aggregate(total=Sum('value'), output_field=models.DecimalField(
            decimal_places=2))
