from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from .models import User, Articles, Task, TaskArticles, Contract, ContractArticle, Contractor, FinancialDocument, FinDocumentArticle

admin.site.register(User, UserAdmin)
admin.site.register(Permission)
admin.site.empty_value_display = '(None)'

@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'financement']
    list_filter = ['number']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit', 'section', 'slug']
    list_filter = ['title']


@admin.register(TaskArticles)
class TaskArticlesAdmin(admin.ModelAdmin):
    list_display = ['article', 'task', 'value']
    list_filter = ['task','article']


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['number', 'contractor', 'id', 'slug']
    list_filter = ['number', 'contractor']


@admin.register(ContractArticle)
class ContractArticleAdmin(admin.ModelAdmin):
    list_display = ['contract', 'contract_article', 'value']
    list_filter = ['contract', 'contract_article']

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'slug']
    list_filter = ['last_name', 'num', 'slug']

@admin.register(FinancialDocument)
class FinancialDocumentAdmin(admin.ModelAdmin):
    list_display = ['contractor', 'number', 'date']
    list_filter = ['contractor', 'number']

@admin.register(FinDocumentArticle)
class FinDocumentArticleAdmin(admin.ModelAdmin):
    list_display = ['article', 'fin_doc', 'value']
    list_filter = ['article', 'fin_doc']