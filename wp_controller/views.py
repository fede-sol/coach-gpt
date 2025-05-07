from rest_framework.views import APIView
from rest_framework.response import Response
from .services import send_message

class ReceiveMessage(APIView):
    def post(self, request):
        data = request.data

        if data.get("event") == "message":
            payload = data.get("payload", {})

            # Extraer el número de teléfono del campo "from"
            from_field = payload.get("from", "")
            phone_number = from_field.split("@")[0] if "@" in from_field else ""

            # Extraer el mensaje del campo "body"
            message = payload.get("body", "")

            print(f"Número: {phone_number}, Mensaje: {message}")

            send_message(phone_recipient=phone_number, message=message)

        return Response({"message": "Hello, World!"})

