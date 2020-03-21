from  django.urls import path
from . import views

app_name = 'budget'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('task/<int:task_id>', views.TaskDetailsView.as_view(), name='task_details'),
    path('task_add/', views.AddTaskView.as_view(), name='add_task'),
    path('edit_task/<int:task_id>', views.EditTaskView.as_view(), name='edit_task'),
    path('delete_task/<int:task_id>', views.DeleteTaskView.as_view(), name='delete_task'),
    path('contracts/', views.ContractsView.as_view(), name='contracts'),
    path('contract/<int:contract_id>', views.ContractDetailsView.as_view(), name='contract_details'),
    path('add_contract/', views.AddContractView.as_view(), name='add_contract'),
    path('edit_contract/<int:contract_id>', views.EditContractView.as_view(), name='edit_contract'),
    path('delete_contract/<int:contract_id>', views.DeleteContractView.as_view(), name='delete_contract'),
    path('contractors/', views.ContractorView.as_view(), name='contractors'),
    path('contractor/<int:contractor_id>', views.ContractorDetailsView.as_view(), name='contractor_details'),
    path('add_contractor/', views.AddContractorView.as_view(), name='add_contractor'),
    path('edit_contractor/<int:contractor_id>', views.EditContractorView.as_view(), name='edit_contractor'),
    path('delete_contractor/<int:contractor_id>', views.DeleteContractorView.as_view(), name='delete_contractor'),
    path('documents/', views.FinancialDocView.as_view(), name='docs'),
    path('document/<int:fd_id>', views.FinancialDocDetailsView.as_view(), name='doc_details'),
    path('add_document/', views.AddFinancialDocView.as_view(), name='add_doc'),
    path('edit_document/<int:fd_id>', views.EditFinancialDocView.as_view(), name='edit_doc'),
    path('delete_document/<int:fd_id>', views.DeleteFinancialDocView.as_view(), name='delete_doc'),
]