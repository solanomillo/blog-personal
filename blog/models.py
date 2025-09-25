from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class Categoria(models.Model):
    """
    Modelo para categorizar las publicaciones del blog.
    """
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('posts_por_categoria', args=[self.slug])


class Publicacion(models.Model):
    """
    Modelo principal para las publicaciones del blog.
    """
    ESTADO_OPCIONES = [
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
    ]
    
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='fecha_publicacion')
    autor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='publicaciones_blog'
    )
    contenido = RichTextField()
    resumen = models.TextField(max_length=500, blank=True)
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        related_name='publicaciones'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(
        max_length=10, 
        choices=ESTADO_OPCIONES, 
        default='borrador'
    )
    imagen_destacada = models.ImageField(
        upload_to='imagenes', 
        blank=True,
    )
    tags = TaggableManager()
    
    class Meta:
        verbose_name = 'publicación'
        verbose_name_plural = 'publicaciones'
        ordering = ['-fecha_publicacion']
        indexes = [
            models.Index(fields=['-fecha_publicacion', 'estado']),
        ]
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('post_detalle', args=[
            self.fecha_publicacion.year,
            self.fecha_publicacion.month,
            self.fecha_publicacion.day,
            self.slug
        ])
    
    @property
    def es_publicado(self):
        return self.estado == 'publicado'


class Comentario(models.Model):
    """
    Modelo para los comentarios de las publicaciones.
    """
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comentarios_blog'
    )
    contenido = models.TextField(max_length=1000)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'
        ordering = ['fecha_creacion']
    
    def __str__(self):
        return f'Comentario de {self.autor} en {self.publicacion}'
