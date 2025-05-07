from openai import OpenAI
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

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
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=[
                    {"role": "user", "content": "write a haiku about ai"}
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