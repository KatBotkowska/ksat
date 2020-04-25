from  django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'budget'

urlpatterns = [
    #path('', views.IndexView.as_view(), name='index'), - zamiast tego to niżej
    path('', TemplateView.as_view(template_name='budget/index.html'), name = 'index'),
    #TASK
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('task/<slug:task_slug>', views.TaskDetailsView.as_view(), name='task_details'),
    path('task_add/', views.AddTaskView.as_view(), name='add_task'),
    path('<slug:task_slug>/add_articles_to_task', views.AddArticlesToTaskView.as_view(), name='task_add_articles'),
    path('<slug:task_slug>/edit_articles_in_task', views.EditArticlesInTaskView.as_view(), name='task_edit_articles'),
    path('edit_task/<slug:task_slug>', views.EditTaskView.as_view(), name='edit_task'),
    path('delete_task/<slug:task_slug>', views.DeleteTaskView.as_view(), name='delete_task'),
    #CONTRACT
    path('contracts/', views.ContractsView.as_view(), name='contracts'),
    path('contract/<slug:contract_slug>', views.ContractDetailsView.as_view(), name='contract_details'),
    path('add_contract/', views.AddContractView.as_view(), name='add_contract'),
    path('add_articles_to_contract/<slug:contract_slug>', views.AddArticlesToContractView.as_view(), name='contract_add_articles'),
    path('edit_articles_in_contract/<slug:contract_slug>', views.EditArticlesInContractView.as_view(), name='contract_edit_articles'),
    path('edit_contract/<slug:contract_slug>', views.EditContractView.as_view(), name='edit_contract'),
    path('delete_contract/<slug:contract_slug>', views.DeleteContractView.as_view(), name='delete_contract'),
    #CONTRACTORS
    path('contractors/', views.ContractorView.as_view(), name='contractors'),
    path('contractor/<slug:contractor_slug>', views.ContractorDetailsView.as_view(), name='contractor_details'),
    path('add_contractor/', views.AddContractorView.as_view(), name='add_contractor'),
    path('edit_contractor/<slug:contractor_slug>', views.EditContractorView.as_view(), name='edit_contractor'),
    path('delete_contractor/<slug:contractor_slug>', views.DeleteContractorView.as_view(), name='delete_contractor'),
    #FINANCIAL DOCUMENTS
    path('documents/conractor/<slug:contractor_slug>/docs', views.FinancialDocContractorView.as_view(), name ='contractor-findocs'),
    path('documents/conract/<slug:contract_slug>/docs', views.FinancialDocContractView.as_view(), name ='contract-findocs'),
    path('documents/task/<slug:task_slug>/docs', views.FinancialDocTaskView.as_view(), name ='task-findocs'),
    path('document/<slug:findoc_slug>', views.FinancialDocDetailsView.as_view(), name='findoc_details'),
    path('add_findoc', views.AddFinancialDocView.as_view(), name='add_findoc'),
    path('add_articles_to_findoc/<slug:findoc_slug>', views.AddArticlesToFinDocView.as_view(), name='findoc_add_articles'),
    path('edit_document/<slug:findoc_slug>', views.EditFinancialDocView.as_view(), name='edit_doc'),
    path('edit_articles_in_findoc/<slug:findoc_slug>/', views.EditArticlesInFinDocView.as_view(), name='findoc_edit_articles'),
    path('delete_document/<slug:findoc_slug>', views.DeleteFinancialDocView.as_view(), name='delete_doc'),
    #USERS
    path('user_register', views.UserRegistrationView.as_view(), name='user_register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('reset_password', views.ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_done', views.ResetPasswordDone.as_view(), name='reset_password_done'),
]