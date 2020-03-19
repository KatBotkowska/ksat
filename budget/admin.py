from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Articles, Task, Contract, Contractor, FinancialDocument

admin.site.register(User, UserAdmin)
admin.site.empty_value_display = '(None)'

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit', 'section', 'value', ]
    list_filter = ['title']

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['number', 'contractor', 'value']
    list_filter = ['number', 'contractor']

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name']
    list_filter = ['last_name', '_id']

@admin.register(FinancialDocument)
class FinancialDocumentAdmin(admin.ModelAdmin):
    list_display = ['contractor', 'number', 'date', 'value']
    list_filter = ['contractor', 'number']
