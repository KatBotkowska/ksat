# Generated by Django 3.0.4 on 2020-04-25 19:52

import autoslug.fields
from django.db import migrations
from budget.models import Contract

def migrate_data_forward(apps, schema_editor):
    for instance in Contract.objects.all():
        print("Generating slug for %s"%instance)
        instance.save() # Will trigger slug update

def migrate_data_backward(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_auto_20200423_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='number', unique=True),
        ),
        migrations.RunPython(
            migrate_data_forward,
            migrate_data_backward,
        ),
    ]
