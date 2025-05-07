import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatbot_api_view(request):
    """
    Endpoint API para el módulo chatbot.
    
    POST /api/chatbot/
    Body: {"message": "texto"}
    Respuesta: {"response": "Mensaje de respuesta fijo"}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message.strip():
            return JsonResponse({'error': 'El mensaje no puede estar vacío'}, status=400)
        
        # Respuesta hardcodeada
        response = "Mensaje de respuesta fijo"
        return JsonResponse({'response': response}, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error del servidor: {str(e)}'}, status=500)