# Generated by Django 3.0.4 on 2020-04-01 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_populate'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractArticles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=11)),
            ],
            options={
                'verbose_name': 'contract articles',
                'ordering': ('contract',),
                'default_related_name': 'contract_articles',
            },
        ),
        migrations.RenameModel(
            old_name='FinDocumentArticle',
            new_name='FinDocumentArticles',
        ),
        migrations.AlterModelOptions(
            name='contract',
            options={'default_related_name': 'contract', 'ordering': ('number', 'contractor'), 'verbose_name': 'contract'},
        ),
        migrations.AlterModelOptions(
            name='taskarticles',
            options={'default_related_name': 'task_articles', 'ordering': ('task',), 'verbose_name': 'task articles'},
        ),
        migrations.AlterField(
            model_name='taskarticles',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_articles', to='budget.Articles'),
        ),
        migrations.AlterField(
            model_name='taskarticles',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_articles', to='budget.Task'),
        ),
        migrations.DeleteModel(
            name='ContractArticle',
        ),
        migrations.AddField(
            model_name='contractarticles',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_articles', to='budget.Contract'),
        ),
        migrations.AddField(
            model_name='contractarticles',
            name='contract_article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_articles', to='budget.Articles'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='article',
            field=models.ManyToManyField(related_name='contract', through='budget.ContractArticles', to='budget.Articles'),
        ),
    ]
