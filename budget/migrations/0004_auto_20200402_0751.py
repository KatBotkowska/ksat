# Generated by Django 3.0.4 on 2020-04-02 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_auto_20200402_0749'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contractor',
            old_name='_id',
            new_name='num',
        ),
    ]
