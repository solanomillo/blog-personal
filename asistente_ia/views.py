"""
Vistas del asistente virtual Luc integradas con Gemini API.
"""

import re
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .gemini import get_asistente_virtual, SALUDO_INICIAL
from .utils import (
    obtener_blog,
    obtener_blog_por_categoria,
    obtener_ultimas_publicaciones,
)

# Diccionario temporal para chats por usuario
# En producción se recomienda usar Redis o base de datos
chats = {}


def _consultar_gemini(prompt: str) -> str:
    """
    Realiza la llamada al asistente virtual Luc (Gemini)
    y devuelve el texto procesado.
    """
    asistente = get_asistente_virtual()
    respuesta = asistente.generate_content(prompt)
    return respuesta.text.strip()


@csrf_exempt
def chat_api(request):
    """
    API del chat para interactuar con Luc.
    Maneja mensajes del usuario y responde
    utilizando el modelo de Gemini.
    """
    try:
        # Obtener ID de sesión único
        user_id = (
            request.session.session_key
            or request.session.save()
            or request.session.session_key
        )
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
            n = re.search(r"\d+", user_message)
            cantidad = int(n.group()) if n else 3
            blog_contexto = obtener_ultimas_publicaciones(n=cantidad)

        # --- Detectar si pide publicaciones por categoría ---
        elif "categoria" in user_message or "publicaciones de" in user_message:
            palabras = (
                user_message.replace("categoria", "")
                .replace("publicaciones de", "")
                .strip()
            )
            if palabras:
                blog_contexto = obtener_blog_por_categoria(palabras)

        # --- Si no especifica nada, mostrar todo el blog ---
        if not blog_contexto:
            blog_contexto = obtener_blog()

        # Construcción del prompt para Gemini
        prompt = (
            f"Contexto del blog:\n{blog_contexto}\n\n"
            "Historial de conversación:\n"
        )
        for m in historial:
            role = "Usuario" if m["role"] == "user" else "Luc"
            prompt += f"{role}: {m['content']}\n"
        prompt += "Luc:"

        # Llamada al modelo Gemini encapsulada
        texto = _consultar_gemini(prompt)

        # Limpiar texto y adaptarlo a salida estilo chat
        texto_html = "<br>".join(
            [line.strip() for line in texto.split("\n") if line.strip()]
        )

        # Guardar respuesta del bot en historial
        historial.append({"role": "assistant", "content": texto})

        return JsonResponse({"respuesta": texto_html})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse(
            {"respuesta": f"Lo siento, hubo un error procesando tu solicitud: {e}"}
        )
