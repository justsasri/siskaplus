from django.urls import path
from django.shortcuts import render


def index_view(request):
    context = {
        'contextual': False,
        'page_title': 'Django materials',
        'buttons': [
            {'label': 'Favorite', 'url': '#', 'icon': 'favorite'},
            {'label': 'Search', 'url': '#', 'icon': 'search'},
        ]
    }
    return render(request, 'materials/index.html', context=context)


def inspect_view(request):
    context = {
        'contextual': True,
        'page_title': 'Contextual page',
        'buttons': [
            {'label': 'Share', 'url': '#', 'icon': 'share'},
            {'label': 'Delete', 'url': '#', 'icon': 'delete'}
        ]
    }
    return render(request, 'materials/index.html', context=context)

urlpatterns = [
    path('', index_view, name='material_index'),
    path('contextual/', inspect_view, name='material_inspect')
]
