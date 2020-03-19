from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    pass


class Articles(models.Model):
    art3038 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art3039 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4118 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4119 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4128 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4129 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4178 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4179 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4218 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4219 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4308 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4309 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4388 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4389 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4398 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4399 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4418 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4419 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4428 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4429 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4518 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4519 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4618 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art4619 = models.DecimalField(max_digits=10, decimal_places=2, default=0,  blank=True, null=True)
    art6068 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    art6069 = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = 'article'

    def value(self):    #TODO
        return 1
        # return self.art3038 + self.art3039 + self.art4118 + self.art4119 + self.art4128 + self.art4129 + self.art4178 + \
        #        self.art4218 + self.art4219 + self.art4308 + self.art4309 + self.art4388 + self.art4389 + self.art4398 + \
        #        self.art4399 + self.art4418 + self.art4419 + self.art4428 + self.art4429 + self.art4518 + self.art4519 + \
        #        self.art4618 + self.art4619 + self.art6068 + self.art6069


class Task(Articles):
    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=256)
    unit = models.SmallIntegerField()
    section = models.SmallIntegerField()

    def __str__(self):
        return f'Title {self.title}, unit {self.unit}, section {self.section}'

    def get_absolute_url(self):
        return reverse('budget:task_details', kwargs={'task_id': self.pk})

    class Meta:
        default_related_name = 'task'
        ordering = ('title',)
        verbose_name = 'task'

class Contractor(models.Model):
    name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    _id = models.SmallIntegerField(blank=True)
    #contracts = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='contractors', related_query_name='contractor')

    def get_absolute_url(self):
        return reverse('budget:contractor_details', kwargs={'contractor_id': self.pk})

    def __str__(self):
        return f'{self.name} {self.last_name}'

    class Meta:
        default_related_name = 'contractors'
        ordering = ('last_name',)
        verbose_name = 'contractor'

class Contract(Articles):
    number = models.CharField(max_length=128)
    date = models.DateField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='contracts', related_query_name='contract')
    contractor = models.ForeignKey(Contractor, default=None, on_delete=models.CASCADE, related_name='contracts', related_query_name='contract')

    def __str__(self):
        return f'number {self.number}, date {self.date}'

    def get_absolute_url(self):
        return reverse('budget:contract_details', kwargs={'contract_id': self.pk})

    class Meta:
        default_related_name = 'contract'
        ordering = ('number',)
        verbose_name = 'contract'

class FinancialDocument(Articles):
    # task = models.ForeignKey(Task, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='fds', related_query_name='fd')
    contractor = models.ForeignKey(Contractor, default=None, on_delete=models.CASCADE, related_name='fds', related_query_name='fd')
    number = models.CharField(max_length=64, default=None)
    date = models.DateField()
    payment_date1 = models.DateField(blank=True, null=True)
    payment_date2 = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('budget:fd_details', kwargs={'fd_id': self.pk})

    class Meta:
        default_related_name = 'fds'
        verbose_name = 'finacial_doc'