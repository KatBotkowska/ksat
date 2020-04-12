from django import template
from django.db.models import Sum

from budget.models import Task, TaskArticles, Contract, ContractArticle, Articles, \
    FinancialDocument, FinDocumentArticle

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


@register.simple_tag
def task_article_performance(article, task):
    performance = 0
    contracts = Contract.objects.filter(task=task)
    for contract in contracts:
        contract_article_performance = FinDocumentArticle.objects.filter(article=article,
                        fin_doc__contract=contract).aggregate(total=Sum('value'))['total']
        if contract_article_performance is not None:
            performance += contract_article_performance
    return round(performance, 2)

@register.simple_tag
def contract_article_performance(article, contract):
    performance = 0
    findocs = FinancialDocument.objects.filter(contract=contract)
    for findoc in findocs:
        findoc_article_performance = FinDocumentArticle.objects.filter(article=article,
                            fin_doc = findoc).aggregate(total=Sum('value'))['total']
        if findoc_article_performance is not None:
            performance += findoc_article_performance
    return round(performance, 2)