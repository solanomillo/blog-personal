"""
URLs para la aplicación del blog.
"""
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.ListaPublicaciones.as_view(), name='inicio'),
    path(
        'publicacion/<slug:slug>/',
        views.DetallePublicacion.as_view(),
        name='post_detalle'
    ),
    path(
        'categoria/<slug:slug>/',
        views.PublicacionesPorCategoria.as_view(),
        name='posts_por_categoria'
    ),
    path('buscar/', views.BuscarPublicaciones.as_view(), name='buscar_publicaciones'),
    # path(
    #     'publicacion/nueva/',
    #     views.CrearPublicacion.as_view(),
    #     name='crear_publicacion'
    # ),
    # path(
    #     'publicacion/editar/<int:pk>/',
    #     views.EditarPublicacion.as_view(),
    #     name='editar_publicacion'
    # ),
    path(
        'publicacion/<int:pk>/comentario/',
        views.agregar_comentario,
        name='agregar_comentario'
    ),
    path('sobre-mi/', views.sobreMi, name='sobre_mi'),
]