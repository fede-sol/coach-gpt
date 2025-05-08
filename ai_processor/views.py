from email import message
from openai import OpenAI
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import logging


logger = logging.getLogger('chat_gpt')


class ChatGPTService:
    @staticmethod
    def query_chatgpt(user_message: str, model: str = "gpt-3.5-turbo", max_tokens: int = 150, temperature: float = 0.7) -> dict:
        """
        Consulta la API de OpenAI con un mensaje de usuario.
        Reutilizable en otras partes del monolito.
        
        Args:
            user_message (str): Mensaje del usuario.
            model (str): Modelo de OpenAI (default: gpt-3.5-turbo).
            max_tokens (int): Máximo de tokens en la respuesta.
            temperature (float): Controla la creatividad.
        
        Returns:
            dict: {'response': 'texto'} o {'error': 'mensaje'}.
        """
        if not user_message.strip():
            return {"error": "El mensaje no puede estar vacío"}
        
        try:

            # Primer consulta con contexto.
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=[
                    {"role": "user",
                      "content": "Eres un coach profesional, especializado tanto en el ámbito empresarial como personal." +
                                    "Tu propósito principal es ayudar a los usuarios a identificar, abordar y superar desafíos, mejorar su rendimiento, alcanzar sus objetivos y fomentar su bienestar."+
                                    "Actúa siempre con un enfoque centrado en el usuario y sus necesidades específicas. Escucha activamente (simulando la comprensión del contexto) y haz preguntas clave para clarificar si es necesario, pero prioriza la concisión y la practicidad, especialmente si el contexto sugiere que el usuario necesita consejo rápido." +
                                    "Ofrece guidance, perspectivas, herramientas prácticas y pasos accionables que el usuario pueda implementar de inmediato." +
                                    "Sé empático, alentador, constructivo y mantén siempre un tono de confianza y confidencialidad. Fomenta la reflexión pero también la acción." +
                                    "Adapta la profundidad de tu respuesta a la urgencia y el estilo del usuario; prepárate para dar consejos rápidos y directos cuando la situación lo requiera (como antes de una presentación), o explorar más a fondo si el usuario indica que desea una conversación más extensa." +
                                    "Tu rol es de apoyo y guía para el desarrollo y el afrontamiento de situaciones específicas en la vida profesional y personal del usuario."+
                                    f"{user_message}"}
                ]
            )

            
            return {"response": completion.choices[0].message.content}
        
        except OpenAI.error.AuthenticationError:
            return {"error": "Error de autenticación con OpenAI"}
        except OpenAI.error.RateLimitError:
            return {"error": "Límite de cuota alcanzado"}
        except Exception as e:
            return {"error": f"Error: {str(e)}"}

@csrf_exempt
def chat_api_view(request):
    """
    Endpoint API para consultar ChatGPT.
    
    POST /api/chat/
    Body: {"message": "texto"}
    Respuesta: {"response": "texto"} o {"error": "mensaje"}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        result = ChatGPTService.query_chatgpt(user_message)
        
        if 'response' in result:
            return JsonResponse({'response': result['response']}, status=200)
        return JsonResponse({'error': result['error']}, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error del servidor: {str(e)}'}, status=500)