from django.contrib import admin

from .models import Categoria, Publicacion

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'estado', 'fecha_publicacion')
    list_filter = ('estado', 'categoria', 'fecha_publicacion', 'autor')
    search_fields = ('titulo', 'contenido', 'resumen')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'fecha_publicacion'
    ordering = ('-fecha_publicacion',)
    raw_id_fields = ('autor',)
    fieldsets = (
        (None, {
            'fields': ('titulo', 'slug', 'autor', 'categoria', 'estado')
        }),
        ('Contenido', {
            'fields': ('contenido', 'resumen', 'imagen_destacada')
        }),
        ('Fechas', {
            'fields': ('fecha_publicacion',)
        }),
    )
