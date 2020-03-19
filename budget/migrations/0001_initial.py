# Generated by Django 3.0.4 on 2020-03-19 15:47

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art3038', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art3039', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4118', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4119', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4128', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4129', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4178', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4179', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4218', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4219', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4308', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4309', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4388', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4389', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4398', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4399', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4418', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4419', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4428', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4429', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4518', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4519', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4618', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4619', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art6068', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art6069', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('number', models.CharField(max_length=128)),
                ('date', models.DateField()),
            ],
            options={
                'verbose_name': 'contract',
                'ordering': ('number',),
                'default_related_name': 'contract',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art3038', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art3039', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4118', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4119', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4128', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4129', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4178', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4179', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4218', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4219', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4308', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4309', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4388', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4389', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4398', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4399', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4418', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4419', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4428', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4429', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4518', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4519', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4618', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4619', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art6068', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art6069', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('title', models.CharField(max_length=128, unique=True)),
                ('description', models.CharField(max_length=256)),
                ('unit', models.SmallIntegerField()),
                ('section', models.SmallIntegerField()),
            ],
            options={
                'verbose_name': 'task',
                'ordering': ('title',),
                'default_related_name': 'task',
            },
        ),
        migrations.CreateModel(
            name='FinancialDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art3038', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art3039', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4118', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4119', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4128', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4129', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4178', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4179', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4218', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4219', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4308', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4309', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4388', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4389', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4398', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4399', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4418', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4419', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4428', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4429', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4518', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4519', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4618', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art4619', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art6068', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('art6069', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('payment_date1', models.DateField(blank=True)),
                ('payment_date2', models.DateField(blank=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fds', related_query_name='fd', to='budget.Contract')),
            ],
            options={
                'verbose_name': 'finacial_doc',
                'default_related_name': 'fds',
            },
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('_id', models.SmallIntegerField(blank=True)),
                ('contracts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractors', related_query_name='contractor', to='budget.Contract')),
            ],
            options={
                'verbose_name': 'contractor',
                'ordering': ('last_name',),
                'default_related_name': 'contractors',
            },
        ),
        migrations.AddField(
            model_name='contract',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', related_query_name='contract', to='budget.Task'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
