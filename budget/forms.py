from django import forms
from django.forms import ModelForm, Textarea
from . models import Task, Contract, Contractor, FinancialDocument

# article_fields = (
#         'art3038',
#         'art3039',
#         'art4118',
#         'art4119',
#         'art4128',
#         'art4129',
#         'art4178',
#         'art4179',
#         'art4218',
#         'art4219',
#         'art4308',
#         'art4309',
#         'art4388',
#         'art4389',
#         'art4398',
#         'art4399',
#         'art4418',
#         'art4419',
#         'art4428',
#         'art4518',
#         'art4519',
#         'art4618',
#         'art4619',
#         'art6068',
#         'art6069'
# )
#fields description for each article
articles_fields = {
    'art3038': ('for persons'),
    'art3039': ('for persons'),
    'art4118': ('for persons'),
    'art4119': ('for persons'),
    'art4128': ('for persons'),
    'art4129': ('for persons'),
    'art4178': ('for persons'),
    'art4179': ('for persons'),
    'art4218': ('for persons'),
    'art4219': ('for persons'),
    'art4308': ('for persons'),
    'art4309': ('for persons'),
    'art4388': ('for persons'),
    'art4389': ('for persons'),
    'art4398': ('for persons'),
    'art4399': ('for persons'),
    'art4418': ('for persons'),
    'art4419': ('for persons'),
    'art4428': ('for persons'),
    'art4518': ('for persons'),
    'art4519': ('for persons'),
    'art4618': ('for persons'),
    'art4619': ('for persons'),
    'art6068': ('for persons'),
    'art6069': ('for persons'),
}
class AddTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'unit', 'section') + tuple(articles_fields.keys())
        widgets = {
            'description': Textarea(attrs={'cols':80, 'rows': 5}),
        }
        help_texts = articles_fields

class EditTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'unit', 'section') + tuple(articles_fields.keys())
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
        }


