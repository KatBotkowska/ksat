# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations
from budget.models import Articles
def populate(apps, schema_editor):
    Articles.objects.create(number=303, name = 'Różne wydatki na rzecz osób fizycznych', financement=8)
    Articles.objects.create(number=303, name='Różne wydatki na rzecz osób fizycznych', financement=9)
    Articles.objects.create(number=417, name='Wynagrodzenia bezosobowe', financement=8)
    Articles.objects.create(number=417, name='Wynagrodzenia bezosobowe', financement=9)
    Articles.objects.create(number=421, name='Zakup materiałów i wyposażenia', financement=8)
    Articles.objects.create(number=421, name='Zakup materiałów i wyposażenia', financement=9)
    Articles.objects.create(number=430, name='Zakup usług pozostałych', financement=8)
    Articles.objects.create(number=430, name='Zakup usług pozostałych', financement=9)
    Articles.objects.create(number=438, name='Zakup usług obejmujących tłumaczenia', financement=8)
    Articles.objects.create(number=438, name='Zakup usług obejmujących tłumaczenia', financement=9)
    Articles.objects.create(number=439, name='Zakup usług obejmujących wykonanie ekspertyz, analiz i opinii',
                            financement=8)
    Articles.objects.create(number=439, name='Zakup usług obejmujących wykonanie ekspertyz, analiz i opinii',
                            financement=9)
    Articles.objects.create(number=441, name='Podróże służbowe krajowe',
                            financement=8)
    Articles.objects.create(number=441, name='Podróże służbowe krajowe',
                            financement=9)
    Articles.objects.create(number=442, name='Podróże służbowe zagraniczne',
                            financement=8)
    Articles.objects.create(number=442, name='Podróże służbowe zagraniczne',
                            financement=9)
    Articles.objects.create(number=451, name='Opłaty na rzecz budżetu państwa',
                            financement=8)
    Articles.objects.create(number=451, name='Opłaty na rzecz budżetu państwa',
                            financement=9)
    Articles.objects.create(number=461, name='Koszty postępowania sądowego i prokuratorskiego',
                            financement=8)
    Articles.objects.create(number=461, name='Koszty postępowania sądowego i prokuratorskiego',
                            financement=9)
    Articles.objects.create(number=606, name='Wydatki na zakupy inwestycyjne jednostek budżetowych',
                            financement=8)
    Articles.objects.create(number=606, name='Wydatki na zakupy inwestycyjne jednostek budżetowych',
                            financement=9)


class Migration(migrations.Migration):
    dependencies = [
        ('budget', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(populate),
    ]