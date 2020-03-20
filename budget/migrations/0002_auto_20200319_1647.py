# Generated by Django 3.0.4 on 2020-03-19 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractor',
            name='contracts',
        ),
        migrations.AddField(
            model_name='contract',
            name='contractor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='contracts', related_query_name='contract', to='budget.Contractor'),
        ),
        migrations.AddField(
            model_name='financialdocument',
            name='contractor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='fds', related_query_name='fd', to='budget.Contractor'),
        ),
        migrations.AddField(
            model_name='financialdocument',
            name='number',
            field=models.CharField(default=None, max_length=64),
        ),
    ]