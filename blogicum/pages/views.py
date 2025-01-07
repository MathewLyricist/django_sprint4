from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    """Возвращает страницу с описанием проекта."""
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Возвращает страницу с правилами."""
    template_name = 'pages/rules.html'


def csrf_failure(request, reason='') -> HttpResponse:
    """Рендер страницы для 403 ошибки."""
    template: str = 'pages/403csrf.html'
    return render(request, template, status=403)


def page_not_found(request, exception) -> HttpResponse:
    """Рендер страницы для 404 ошибки."""
    template: str = 'pages/404.html'
    return render(request, template, status=404)


def server_error(request, reason='') -> HttpResponse:
    """Рендер страницы для 500 ошибки."""
    template: str = 'pages/500.html'
    return render(request, template, status=500)
