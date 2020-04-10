from django import template
from django.db.models import Sum

from budget.models import Task, TaskArticles, Contract, ContractArticle, Articles

register = template.Library()

@register.simple_tag
def task_article_engagement(article, task):
    engagement = 0
    contracts = Contract.objects.filter(task=task)
    for contract in contracts:
        contract_article_engagement = ContractArticle.objects.filter(contract=contract,
                            contract_article=article).aggregate(total=Sum('value'))['total']
        if contract_article_engagement is not None:
            engagement += contract_article_engagement
    return round(engagement, 2)
