"""
Context processors para la aplicación del blog.
"""
from .models import Categoria


def categorias_recientes(request):
    """
    Procesador de contexto para incluir categorías en todas las templates.
    """
    return {
        'categorias_recientes': Categoria.objects.all()[:10]
    }