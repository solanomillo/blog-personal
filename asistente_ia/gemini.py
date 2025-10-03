"""
Módulo para configurar e inicializar el asistente virtual Luc 
basado en Gemini API.
"""

import google.generativeai as genai
from django.conf import settings

# Constantes
SALUDO_INICIAL = (
    "Hola, soy Luc, tu asistente virtual del blog. "
    "¿Quieres explorar las categorías o ver las últimas publicaciones? 🚀"
)


def get_asistente_virtual():
    """
    Inicializa y devuelve el modelo generativo de Gemini
    configurado con las instrucciones personalizadas para Luc.
    """
    genai.configure(api_key=settings.GEMINI_API_KEY)

    return genai.GenerativeModel(
        model_name=settings.GEMINI_MODELO_FLASH,
        system_instruction=(
            "Te llamas Luc, eres un asistente virtual de un blog personal. "
            "Tu rol es ayudar a los visitantes con información sobre categorías, publicaciones, autores, "
            "fechas de publicación, resúmenes y comentarios. "
            "Cuando te pregunten por publicaciones, consulta la base de datos del blog. "
            "Responde de manera clara, natural y amable, sin usar asteriscos ni símbolos innecesarios. "
            "Cuando enumeres publicaciones solo muestra 3 (las más recientes), con su título, resumen, fecha y enlace. "
            "Cuando muestres categorías incluye su enlace.\n"
            "Ejemplo:\n"
            "- Publicación 1: resumen breve (fecha) → enlace\n"
            "- Publicación 2: resumen breve (fecha) → enlace\n"
            "- Publicación 3: resumen breve (fecha) → enlace\n"
        )
    )
