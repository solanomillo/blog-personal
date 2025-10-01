from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .gemini import llm, SALUDO_INICIAL
from .utils import obtener_blog, obtener_blog_por_categoria, obtener_ultimas_publicaciones

# Diccionario temporal para chats por usuario
# En producción se recomienda usar Redis o base de datos
chats = {}

@csrf_exempt
def chat_api(request):
    try:
        # Obtener ID de sesión único
        user_id = request.session.session_key or request.session.save() or request.session.session_key
        user_message = request.GET.get("message", "").strip().lower()

        # Mensaje de saludo inicial
        if user_message == "__init__":
            return JsonResponse({"respuesta": SALUDO_INICIAL})

        # Recuperar o crear historial del usuario
        if user_id not in chats:
            chats[user_id] = []

        historial = chats[user_id]
        historial.append({"role": "user", "content": user_message})

        blog_contexto = None

        # --- Detectar si pide últimas publicaciones ---
        if "últimas" in user_message or "ultimas" in user_message:
            import re
            n = re.search(r"\d+", user_message)
            cantidad = int(n.group()) if n else 3
            blog_contexto = obtener_ultimas_publicaciones(n=cantidad)

        # --- Detectar si pide publicaciones por categoría ---
        elif "categoria" in user_message or "publicaciones de" in user_message:
            palabras = user_message.replace("categoria", "").replace("publicaciones de", "").strip()
            if palabras:
                blog_contexto = obtener_blog_por_categoria(palabras)

        # --- Si no especifica nada, mostrar todo el blog ---
        if not blog_contexto:
            blog_contexto = obtener_blog()

        # Construcción del prompt para Gemini
        prompt = f"Contexto del blog:\n{blog_contexto}\n\nHistorial de conversación:\n"
        for m in historial:
            role = "Usuario" if m["role"] == "user" else "Luc"
            prompt += f"{role}: {m['content']}\n"
        prompt += "Luc:"

        # Llamada al modelo Gemini
        respuesta = llm.generate_content(prompt)

        # Limpiar texto: eliminar asteriscos, mantener saltos de línea para chat
        texto = respuesta.text.replace("*", "").strip()
        texto_html = "<br>".join([line.strip() for line in texto.split("\n") if line.strip()])

        # Guardar respuesta del bot en historial
        historial.append({"role": "assistant", "content": texto})

        return JsonResponse({"respuesta": texto_html})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"respuesta": f"Lo siento, hubo un error procesando tu solicitud: {e}"})
