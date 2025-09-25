from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Publicacion, Categoria, Comentario
from .forms import ComentarioForm, PublicacionForm


class ListaPublicaciones(ListView):
    """
    Vista para listar todas las publicaciones publicadas.
    """
    model = Publicacion
    template_name = 'blog/index.html'
    context_object_name = 'publicaciones'
    paginate_by = 6
    
    def get_queryset(self):
        return Publicacion.objects.filter(
            estado='publicado',
            fecha_publicacion__lte=timezone.now()
        ).select_related('autor', 'categoria').prefetch_related('tags')


class DetallePublicacion(DetailView):
    """
    Vista para mostrar el detalle de una publicación.
    """
    model = Publicacion
    template_name = 'blog/post_detail.html'
    context_object_name = 'publicacion'
    
    def get_queryset(self):
        return Publicacion.objects.filter(
            estado='publicado',
            fecha_publicacion__lte=timezone.now()
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_comentario'] = ComentarioForm()
        context['comentarios'] = self.object.comentarios.filter(activo=True)
        return context


class PublicacionesPorCategoria(ListView):
    """
    Vista para filtrar publicaciones por categoría.
    """
    model = Publicacion
    template_name = 'blog/publicaciones_por_categoria.html'
    context_object_name = 'publicaciones'
    paginate_by = 6
    
    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        return Publicacion.objects.filter(
            categoria=self.categoria,
            estado='publicado',
            fecha_publicacion__lte=timezone.now()
        ).select_related('autor', 'categoria')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        return context


class BuscarPublicaciones(ListView):
    """
    Vista para buscar publicaciones.
    """
    model = Publicacion
    template_name = 'blog/buscar_publicaciones.html'
    context_object_name = 'publicaciones'
    paginate_by = 6
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Publicacion.objects.filter(
                Q(titulo__icontains=query) |
                Q(contenido__icontains=query) |
                Q(resumen__icontains=query),
                estado='publicado',
                fecha_publicacion__lte=timezone.now()
            ).select_related('autor', 'categoria').distinct()
        return Publicacion.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


# class CrearPublicacion(LoginRequiredMixin, CreateView):
#     """
#     Vista para crear una nueva publicación.
#     """
#     model = Publicacion
#     form_class = PublicacionForm
#     template_name = 'blog/post_form.html'
    
#     def form_valid(self, form):
#         form.instance.autor = self.request.user
#         messages.success(self.request, 'Publicación creada exitosamente.')
#         return super().form_valid(form)


# class EditarPublicacion(LoginRequiredMixin, UpdateView):
#     """
#     Vista para editar una publicación existente.
#     """
#     model = Publicacion
#     form_class = PublicacionForm
#     template_name = 'blog/post_form.html'
    
#     def form_valid(self, form):
#         messages.success(self.request, 'Publicación actualizada exitosamente.')
#         return super().form_valid(form)
    
#     def get_queryset(self):
#         return Publicacion.objects.filter(autor=self.request.user)


def agregar_comentario(request, pk):
    """
    Vista para agregar un comentario a una publicación.
    """
    publicacion = get_object_or_404(
        Publicacion, 
        pk=pk, 
        estado='publicado'
    )
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.publicacion = publicacion
            comentario.autor = request.user
            comentario.save()
            messages.success(request, 'Comentario agregado exitosamente.')
            return redirect('blog:post_detalle', slug=publicacion.slug)

    return redirect('blog:post_detalle', slug=publicacion.slug)


def sobreMi(request):
    """
    Vista para la página "Sobre mí".
    """
    return render(request, 'blog/sobre.html' )