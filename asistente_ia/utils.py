from blog.models import Categoria, Publicacion

def obtener_blog():
    categorias = Categoria.objects.prefetch_related("publicaciones").all()
    texto = "📚 Bienvenido al Blog:\n\n"
    for c in categorias:
        try:
            url_categoria = c.get_absolute_url()
        except:
            url_categoria = "#"
        texto += f"🔹 {c.nombre} → {url_categoria}\n"

        publicaciones = c.publicaciones.filter(estado='publicado')
        if publicaciones.exists():
            for p in publicaciones:
                fecha = p.fecha_publicacion.strftime("%d/%m/%Y") if p.fecha_publicacion else "Sin fecha"
                try:
                    url_post = p.get_absolute_url()
                except:
                    url_post = "#"
                texto += f"   📝 {p.titulo} ({fecha}) → {url_post}\n"
        else:
            texto += "   (No hay publicaciones en esta categoría)\n"
        texto += "\n"
    return texto

def obtener_blog_por_categoria(nombre_categoria):
    try:
        categoria = Categoria.objects.get(nombre__iexact=nombre_categoria)
        try:
            url_categoria = categoria.get_absolute_url()
        except:
            url_categoria = "#"

        publicaciones = categoria.publicaciones.filter(estado='publicado')
        texto = f"📂 Publicaciones en '{categoria.nombre}' → {url_categoria}:\n"
        if publicaciones.exists():
            for p in publicaciones:
                fecha = p.fecha_publicacion.strftime("%d/%m/%Y") if p.fecha_publicacion else "Sin fecha"
                try:
                    url_post = p.get_absolute_url()
                except:
                    url_post = "#"
                texto += f"📝 {p.titulo} ({fecha}) → {url_post}\n"
        else:
            texto += "(No hay publicaciones en esta categoría)\n"
        return texto
    except Categoria.DoesNotExist:
        return f"❌ No encontré la categoría '{nombre_categoria}'."

def obtener_ultimas_publicaciones(n=3):
    publicaciones = Publicacion.objects.filter(estado='publicado').order_by("-fecha_publicacion")[:n]
    texto = f"📰 Últimas {n} publicaciones:\n"
    if publicaciones.exists():
        for p in publicaciones:
            fecha = p.fecha_publicacion.strftime("%d/%m/%Y") if p.fecha_publicacion else "Sin fecha"
            try:
                url_post = p.get_absolute_url()
            except:
                url_post = "#"
            texto += f"📝 {p.titulo} ({fecha}) → {url_post} en {p.categoria.nombre}\n"
    else:
        texto += "(No hay publicaciones disponibles)\n"
    return texto
