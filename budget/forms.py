from django import forms
from django.forms import ModelForm, Textarea, formset_factory
from django.forms.models import modelformset_factory
from . models import Articles, Task, Contract, Contractor, FinancialDocument, TaskArticles, ContractArticle, FinDocumentArticle




class AddTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'unit', 'section')
        widgets = {
            'description': Textarea(attrs={'cols':80, 'rows': 5}),
        }
        #article = forms.ModelMultipleChoiceField(queryset=Articles.objects.all()) #TODO zobaczyc czy sie tak da
        #help_texts = articles_fields
class AddArticlesToTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        task_id = kwargs.pop('initial')['task_id']
        super().__init__(*args, **kwargs)
        #self.fields['task'].queryset = Task.objects.filter(id=task_id) #musi być filter, a nie get
    class Meta:
        model = TaskArticles
        fields = ('article', 'value')

AddArticlesToTaskFormSet = modelformset_factory(TaskArticles,fields = ('article', 'value'), extra=8)

class EditArticlesInTaskForm(ModelForm):
    class Meta:
        model = TaskArticles
        fields = ('article', 'value')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
         }
EditArticlesToTaskFormSet = modelformset_factory(TaskArticles,fields = ('article', 'value'), extra=8)

class EditTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'unit', 'section')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
        }


