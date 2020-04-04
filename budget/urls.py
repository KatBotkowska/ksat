from  django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'budget'

urlpatterns = [
    #path('', views.IndexView.as_view(), name='index'), - zamiast tego to niżej
    path('', TemplateView.as_view(template_name='budget/index.html'), name = 'index'),
    #TASK
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('task/<int:task_id>', views.TaskDetailsView.as_view(), name='task_details'),
    path('task_add/', views.AddTaskView.as_view(), name='add_task'),
    path('<int:task_id>/add_articles_to_task', views.AddArticlesToTaskView.as_view(), name='task_add_articles'),
    path('<int:task_id>/edit_articles_in_task', views.EditArticlesInTaskView.as_view(), name='task_edit_articles'),
    path('edit_task/<int:task_id>', views.EditTaskView.as_view(), name='edit_task'),
    path('delete_task/<int:task_id>', views.DeleteTaskView.as_view(), name='delete_task'),
    #CONTRACT
    path('contracts/', views.ContractsView.as_view(), name='contracts'),
    path('contract/<int:contract_id>', views.ContractDetailsView.as_view(), name='contract_details'),
    path('add_contract/', views.AddContractView.as_view(), name='add_contract'), #TODO moze dodawac umowe do konkretnego zadania: task/<int:task_id>/add_contract
    path('<int:contract_id>/add_articles_to_contract', views.AddArticlesToContractView.as_view(), name='contract_add_articles'),
    path('<int:contract_id>/edit_articles_in_contract', views.EditArticlesInContractView.as_view(), name='contract_edit_articles'),
    path('edit_contract/<int:contract_id>', views.EditContractView.as_view(), name='edit_contract'),
    path('delete_contract/<int:contract_id>', views.DeleteContractView.as_view(), name='delete_contract'),
    #CONTRACTORS
    path('contractors/', views.ContractorView.as_view(), name='contractors'),
    path('contractor/<int:contractor_id>', views.ContractorDetailsView.as_view(), name='contractor_details'),
    path('add_contractor/', views.AddContractorView.as_view(), name='add_contractor'),
    path('edit_contractor/<int:contractor_id>', views.EditContractorView.as_view(), name='edit_contractor'),
    path('delete_contractor/<int:contractor_id>', views.DeleteContractorView.as_view(), name='delete_contractor'),
    #FINANCIAL DOCUMENTS
    path('documents/conractor/<int:contractor_id>/docs', views.FinancialDocContractorView.as_view(), name ='contractor-findocs'),
    path('documents/conract/<int:contract_id>/docs', views.FinancialDocContractView.as_view(), name ='contract-findocs'),
    path('documents/task/<int:task_id>/docs', views.FinancialDocTaskView.as_view(), name ='task-findocs'),
    path('document/<int:findoc_id>', views.FinancialDocDetailsView.as_view(), name='findoc_details'),#TODO <'<int:contract_id>/<int:fd_id>'/'
    path('add_findoc', views.AddFinancialDocView.as_view(), name='add_findoc'), #the same
    path('<int:findoc_id>/add_articles_to_findoc', views.AddArticlesToFinDocView.as_view(), name='findoc_add_articles'),
    path('edit_document/<int:findoc_id>', views.EditFinancialDocView.as_view(), name='edit_doc'),
    path('<int:findoc_id>/edit_articles_in_findoc', views.EditArticlesInFinDocView.as_view(), name='findoc_edit_articles'),
    path('delete_document/<int:findoc_id>', views.DeleteFinancialDocView.as_view(), name='delete_doc'),
]